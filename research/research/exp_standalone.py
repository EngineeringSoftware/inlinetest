import os
from pathlib import Path
from typing import List, Optional

import numpy as np
import seutil as su
from jsonargparse import CLI
from tqdm import tqdm

from research.exp import CmdResult, get_num_test_from_report, run_cmd_timed
from research.macros import Macros

logger = su.log.get_logger(__name__)


class StandaloneExperiments:
    def duplicate_inline_standalone(
        self, example_file: su.arg.RPath, count: int
    ) -> str:
        if not isinstance(example_file, Path):
            example_file = Path(example_file.abs_path)
        example = su.io.load(example_file, su.io.Fmt.txt)
        lines = example.splitlines()
        new_lines = []
        for line in lines:
            content = line.strip()
            if content.startswith("Here(") or content.startswith("new Here("):
                # duplicate here lines
                for i in range(count - 1):
                    new_lines.append(line)
            new_lines.append(line)
        return "\n".join(new_lines)

    def run(
        self,
        language: str,
        requests_file: su.arg.RPath,
        run_dir: su.arg.RPath,
        out_dir: Optional[su.arg.RPath] = None,
        rerun: int = 1,
        duplicating: int = 1,
        force: bool = False,
    ):
        self.config = {
            "language": language,
            "requests_file": os.path.relpath(requests_file, Path.cwd()),
            "rerun": rerun,
            "duplicating": duplicating,
            "hostname": os.uname()[1],
        }

        if out_dir is None:
            # automatically infer output directory
            out_name = "{hostname}-{rerun}-{duplicating}".format(**self.config)
            out_dir = Macros.results_dir / "exp" / "standalone" / language / out_name

        if out_dir.exists() and not force:
            raise ValueError(f"Output directory {out_dir} already exists")
        su.io.mkdir(out_dir, fresh=True)

        su.io.dump(out_dir / "config.yaml", self.config)

        # load requests (example names)
        examples = su.io.load(requests_file)

        # setup runtime env
        if language == "python":
            suffix = "py"
            which_conda = su.bash.run("which conda").stdout.strip()
            if len(which_conda) == 0:
                raise RuntimeError(f"Cannot detect conda environment!")
            env_arg = str(
                Path(which_conda).parent.parent / "etc" / "profile.d" / "conda.sh"
            )
        elif language == "java":
            suffix = "java"
            env_arg = f"{Macros.project_dir}/java/target/inlinetest-1.0.jar"
        else:
            raise ValueError(f"Unknown language {language}")

        # execute
        with tqdm(total=len(examples)) as pbar:
            with su.io.cd(run_dir):
                pbar.set_description("preparing env")
                su.bash.run("./prepare-env.sh", 0)

                pbar.set_description("running")
                for example in examples:
                    example_path = run_dir / f"{example}.{suffix}"
                    if not example_path.exists():
                        logger.warning(f"{example} not found")
                        pbar.update(1)
                        continue

                    # duplicating if needed
                    if duplicating > 1:
                        old_example = su.io.load(example_path, su.io.Fmt.txt)
                        new_example = self.duplicate_inline_standalone(
                            example_path, duplicating
                        )
                        su.io.dump(example_path, new_example, su.io.Fmt.txt)

                    runs = []
                    with su.io.cd(run_dir):
                        for i in range(rerun):
                            runs.append(
                                run_cmd_timed(f"./run-only.sh {env_arg} {example}")
                            )
                        if any(not r.success for r in runs):
                            logger.warning(f"{example} some runs failed")

                    if duplicating > 1:
                        # restore original example
                        su.io.dump(example_path, old_example, su.io.Fmt.txt)

                    # save results
                    su.io.dump(out_dir / f"{example}.json", runs)
                    pbar.update(1)

    def process_results(
        self,
        language: str,
        requests_file: su.arg.RPath,
        results_dirs: List[su.arg.RPath],
        out_dir: su.arg.RPath,
        warmup: int = 1,
    ):
        # load requests
        requests = su.io.load(requests_file)

        seen_dups = set()

        records = []
        for results_dir in results_dirs:
            # load the config file and do some sanity checks
            config = su.io.load(results_dir / "config.yaml")
            assert config["language"] == language
            assert config["rerun"] > warmup

            dup = config["duplicating"]
            assert dup not in seen_dups
            seen_dups.add(dup)

            # load each example's results
            for example in requests:
                record = {
                    "example": example,
                    "duplicating": dup,
                    "error": True,
                    "error-reason": "",
                    "time-list": [],
                    "time": -1,
                    "num-list": [],
                    "num": -1,
                }
                records.append(record)

                result_file = results_dir / f"{example}.json"
                if not result_file.exists():
                    record["error-reason"] = "result file missing"
                    continue
                result = su.io.load(result_file, clz=List[CmdResult])

                # process run results
                for cmd_res in result[warmup:]:
                    if not cmd_res.success:
                        continue
                    record["time-list"].append(cmd_res.time)
                    record["num-list"].append(
                        get_num_test_from_report(
                            cmd_res.stdout, cmd_res.stderr, language
                        )
                    )
                if len(record["time-list"]) == 0:
                    record["error-reason"] = "no successful runs"
                    continue

                record["time"] = np.mean(record["time-list"]).item()
                record["num"] = max(record["num-list"])

                record["error"] = False

        # save the results
        su.io.dump(out_dir / "results.json", records, su.io.Fmt.jsonPretty)

        # compute avreage results per duplicating
        records_avg = []
        for dup in sorted(seen_dups):
            records_this_dup = [
                r for r in records if r["duplicating"] == dup and not r["error"]
            ]
            record = {"duplicating": dup, "num-example": len(records_this_dup)}
            for x in ["time", "num"]:
                record[f"sum-{x}"] = np.sum([r[x] for r in records_this_dup]).item()
                record[f"avg-{x}"] = np.mean([r[x] for r in records_this_dup]).item()
            records_avg.append(record)

        # save the average results
        su.io.dump(out_dir / "results-avg.json", records_avg, su.io.Fmt.jsonPretty)


if __name__ == "__main__":
    su.log.setup(Macros.log_file, level_stderr=su.log.WARNING)
    CLI(StandaloneExperiments, as_positional=False)
