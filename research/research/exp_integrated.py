import copy
import dataclasses
import os
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import seutil as su
from jsonargparse import CLI
from tqdm import tqdm
from unidiff import PatchSet

from research.exp import (CmdResult, build_java_inlinetest,
                          get_num_test_from_report, run_cmd_timed)
from research.macros import Macros

logger = su.log.get_logger(__name__)


@dataclasses.dataclass
class IntegratedExpRequest:
    project: str
    examples: List[str]


@dataclasses.dataclass
class IntegratedExpResult:
    project: str = None
    revision: str = None
    metrics: Optional[dict] = None
    # experiments under the vanilla environment required by unit tests only
    prepare_env_vanilla: CmdResult = None
    build_vanilla: CmdResult = None
    tests_vanilla: List[CmdResult] = dataclasses.field(default_factory=list)
    # experiments under the vanilla environment + inline test installed
    prepare_env_inline: CmdResult = None
    build_inline: CmdResult = None
    tests_unit: List[CmdResult] = dataclasses.field(default_factory=list)
    tests_inline: List[CmdResult] = dataclasses.field(default_factory=list)


class IntegratedExperiments:
    def __init__(self):
        # shared across functions during run
        self.config: dict = None
        self.out_dir: Path = None
        self.scripts_dir: Path = None
        self.default_scripts_dir: Path = None
        self.patches_dir: Path = None
        self.patches_examples_dir: Path = None
        self.patches_projects_dir: Path = None
        self.name2proj: Dict[str, su.project.Project] = None
        self.arg1: str = "default"
        self.arg2: str = "default"

    def run(
        self,
        language: str,
        requests_file: su.arg.RPath,
        rerun: int = 1,
        duplicating: int = 1,
        timeout: int = 1_000,
        only_setup_env: bool = False,
        out_dir: Optional[su.arg.RPath] = None,
        projects_file: Optional[su.arg.RPath] = None,
        force: bool = False,
        scripts_dir: Optional[su.arg.RPath] = None,
        patches_dir: Optional[su.arg.RPath] = None,
        only: Optional[List[str]] = None,
    ):
        self.config = {
            "language": language,
            "requests_file": os.path.relpath(requests_file, Path.cwd()),
            "rerun": rerun,
            "duplicating": duplicating,
            "only_setup_env": only_setup_env,
            "timeout": timeout,
            "hostname": os.uname()[1],
        }

        if out_dir is None:
            # automatically infer output directory
            if only_setup_env or only is not None:
                out_name = "{hostname}-dev".format(**self.config)
            else:
                out_name = "{hostname}-{rerun}-{duplicating}".format(**self.config)
            out_dir = Macros.results_dir / "exp" / "integrated" / language / out_name

        if out_dir.exists() and not force:
            raise ValueError(f"Output directory {out_dir} already exists")
        su.io.mkdir(out_dir, fresh=True)
        self.out_dir = out_dir

        su.io.dump(out_dir / "config.yaml", self.config)

        # load requests
        requests = su.io.load(requests_file, clz=List[IntegratedExpRequest])
        su.io.dump(out_dir / "requests.yaml", requests)

        if only is not None:
            requests = [r for r in requests if r.project in only]

        # load projects specs
        if projects_file is None:
            projects_file = Macros.data_dir / "projects-used" / f"{language}.yaml"
        projects = su.io.load(projects_file, clz=List[su.project.Project])
        self.name2proj = {p.full_name: p for p in projects}

        # figure out which projects to run
        projects: List[su.project.Project] = []

        # figure out scripts and patches directories
        if scripts_dir is None:
            scripts_dir = Macros.data_dir / "scripts" / language
        self.scripts_dir = scripts_dir
        self.default_scripts_dir = scripts_dir / "default"
        if patches_dir is None:
            patches_dir = Macros.data_dir / "patches" / language
        self.patches_dir = patches_dir
        self.patches_examples_dir = patches_dir / "examples"
        self.patches_projects_dir = patches_dir / "projects"

        # prepare the language environment
        if language == "python":
            # arg1: path to conda setup script
            which_conda = su.bash.run("which conda | xargs readlink -f").stdout.strip()
            if len(which_conda) == 0:
                raise RuntimeError(f"Cannot detect conda environment!")
            self.arg1 = str(
                Path(which_conda).parent.parent / "etc" / "profile.d" / "conda.sh"
            )

            # arg2: path to inlinetest package
            self.arg2 = f"{Macros.project_dir}/python"
        if language == "java":
            # arg1: not needed

            # arg2: path to the inlinetest jar
            build_java_inlinetest()
            self.arg2 = f"{Macros.project_dir}/java/target/inlinetest-1.0.jar"

        # run the experiments
        with tqdm(total=len(requests)) as pbar:
            for request in requests:
                pbar.set_description(f"{request.project} starting")
                result = self.run_project(request, pbar)
                pbar.set_description(f"{request.project} finishing")
                if result is not None:
                    su.io.dump(out_dir / f"{request.project}.json", result)
                pbar.update(1)

    def run_project(
        self, request: IntegratedExpRequest, pbar: Optional[tqdm] = None
    ) -> Optional[IntegratedExpResult]:
        if request.project not in self.name2proj:
            logger.warning(f"Project {request.project} not found")
            return None

        project = self.name2proj[request.project]

        # find all scripts
        proj_scripts_dir = self.scripts_dir / request.project
        scripts = {}
        missing_script = False
        for action in [
            "prepare-env-vanilla",
            "prepare-env-inline",
            "build",
            "test-vanilla",
            "test-unit",
            "test-inline",
        ]:
            if (proj_scripts_dir / f"{action}.sh").exists():
                scripts[action] = proj_scripts_dir / f"{action}.sh"
            elif (self.default_scripts_dir / f"{action}.sh").exists():
                scripts[action] = self.default_scripts_dir / f"{action}.sh"
            else:
                logger.warning(
                    f"Project {request.project} aborted: missing {action} script"
                )
                missing_script = True
        if missing_script:
            return None

        # apply all patches
        patches = []
        for example in request.examples:
            example_patch_path = self.patches_examples_dir / f"{example}.patch"
            if example_patch_path.exists():
                if self.config["duplicating"] > 1:
                    # save the duplicated patch to results dir for inspection
                    duplicated_patch = self.duplicate_diff(
                        example_patch_path, self.config["duplicating"]
                    )
                    example_patch_path = self.out_dir / "patches" / f"{example}.patch"
                    su.io.dump(example_patch_path, duplicated_patch, su.io.Fmt.txt)
                patches.append(example_patch_path)
            else:
                logger.warning(
                    f"Project {request.project} has example {example}, but patch for that is missing"
                )

        if (self.patches_projects_dir / f"{request.project}.patch").exists():
            patches.append(self.patches_projects_dir / f"{request.project}.patch")
        logger.info(f"Project {request.project}: {len(patches)} patches to apply")
        patches = [str(x) for x in patches]

        exp_res = IntegratedExpResult(
            project=request.project, revision=project.data["revision"]
        )

        # clone
        if pbar is not None:
            pbar.set_description(f"{request.project} cloning")
        project.clone(Macros.downloads_dir / self.config["language"])

        with su.io.cd(project.dir):
            if pbar is not None:
                pbar.set_description(f"{request.project} preparing [vanilla]")

            # clean up any potential local change, and checkout
            su.bash.run("git clean -fddx", 0)
            project.checkout(project.data["revision"], forced=True)

            # prepare and build vanilla
            exp_res.prepare_env_vanilla = run_cmd_timed(
                f"{scripts['prepare-env-vanilla']} {self.arg1}",
                timeout=self.config["timeout"],
            )
            if not exp_res.prepare_env_vanilla.success:
                logger.warning(
                    f"Project {request.project} aborted: failed to prepare env [vanilla unit tests]"
                )
                return exp_res

            exp_res.build_vanilla = run_cmd_timed(
                f"{scripts['build']} {self.arg1}", timeout=self.config["timeout"]
            )
            if not exp_res.build_vanilla.success:
                logger.warning(
                    f"Project {request.project} aborted: failed to build [vanilla unit tests]"
                )
                return exp_res

            # test vanilla
            if not self.config["only_setup_env"]:
                for i in range(self.config["rerun"]):
                    if pbar is not None:
                        pbar.set_description(
                            f"{request.project} testing [vanilla unit tests] ({i + 1}/{self.config['rerun']})"
                        )
                    exp_res.tests_vanilla.append(
                        run_cmd_timed(
                            f"{scripts['test-vanilla']} {self.arg1}",
                            timeout=self.config["timeout"],
                        )
                    )
                    if not exp_res.tests_vanilla[-1].success:
                        logger.info(
                            f"{request.project} testing [vanilla unit tests] ({i + 1}/{self.config['rerun']}) failed: {exp_res.tests_vanilla[-1]}"
                        )
                if not all(x.success for x in exp_res.tests_vanilla):
                    logger.warning(
                        f"Project {request.project}: some tests failed [vanilla unit tests]"
                    )

            if pbar is not None:
                pbar.set_description(f"{request.project} preparing [inlinetest]")

            # clean up any potential local change, and checkout
            su.bash.run("git clean -fddx", 0)
            project.checkout(project.data["revision"], forced=True)

            # apply the patches to add inline tests
            rr = su.bash.run(f"git apply --ignore-whitespace -3 {' '.join(patches)}")
            if rr.returncode != 0:
                logger.warning(
                    f"Project {request.project} aborted: failed to apply patches\nSTDOUT:\n{rr.stdout}\nSTDERR:\n{rr.stderr}"
                )
                return exp_res

            # prepare and build w/ inline tests
            exp_res.prepare_env_inline = run_cmd_timed(
                f"{scripts['prepare-env-inline']} {self.arg1} {self.arg2}",
                timeout=self.config["timeout"],
            )
            if not exp_res.prepare_env_inline.success:
                logger.warning(
                    f"Project {request.project} aborted: failed to prepare env [inlinetest]"
                )
                return exp_res

            exp_res.build_inline = run_cmd_timed(
                f"{scripts['build']} {self.arg1}", timeout=self.config["timeout"]
            )
            if not exp_res.build_inline.success:
                logger.warning(
                    f"Project {request.project} aborted: failed to build [inlinetest]"
                )
                return exp_res

            # test w/ inline tests
            if not self.config["only_setup_env"]:
                for i in range(self.config["rerun"]):
                    if pbar is not None:
                        pbar.set_description(
                            f"{request.project} testing [inlinetest unit tests] ({i + 1}/{self.config['rerun']})"
                        )
                    # unit tests
                    exp_res.tests_unit.append(
                        run_cmd_timed(
                            f"{scripts['test-unit']} {self.arg1} {self.arg2}",
                            timeout=self.config["timeout"],
                        )
                    )
                    if not exp_res.tests_unit[-1].success:
                        logger.info(
                            f"{request.project} testing [inlinetest unit tests] ({i + 1}/{self.config['rerun']}) failed: {exp_res.tests_unit[-1]}"
                        )
                    if pbar is not None:
                        pbar.set_description(
                            f"{request.project} testing [inlinetest inline tests] ({i + 1}/{self.config['rerun']})"
                        )
                    # test, with inline test plugin loaded and enabled
                    exp_res.tests_inline.append(
                        run_cmd_timed(
                            f"{scripts['test-inline']} {self.arg1} {self.arg2}",
                            timeout=self.config["timeout"],
                        )
                    )
                    if not exp_res.tests_inline[-1].success:
                        logger.info(
                            f"{request.project} testing [inlinetest inline tests] ({i + 1}/{self.config['rerun']}) failed: {exp_res.tests_inline[-1]}"
                        )

                if not all(x.success for x in exp_res.tests_unit):
                    logger.warning(
                        f"Project {request.project}: some tests failed [inlinetest unit tests]"
                    )

                if not all(x.success for x in exp_res.tests_inline):
                    logger.warning(
                        f"Project {request.project}: some tests failed [inlinetest inline tests]"
                    )

        # if we're here, all steps finished so let's compute some quick metrics
        exp_res.metrics = {}
        for x in ["vanilla", "unit", "inline"]:
            exp_res.metrics[f"test_{x}_pass"] = len(
                [x for x in getattr(exp_res, f"tests_{x}") if x.success]
            )
            exp_res.metrics[f"test_{x}_fail"] = len(
                [x for x in getattr(exp_res, f"tests_{x}") if not x.success]
            )
            exp_res.metrics[f"test_{x}_times"] = [
                x.time for x in getattr(exp_res, f"tests_{x}")
            ]
        return exp_res

    def duplicate_diff(self, diff_file: su.arg.RPath, count: int) -> str:
        if not isinstance(diff_file, Path):
            diff_file = Path(diff_file.abs_path)
        diff = su.io.load(diff_file, su.io.Fmt.txt)
        pfile = PatchSet(diff)[0]
        new_pfile = copy.copy(pfile)
        new_pfile.clear()
        added_lines = 0
        for hunk in pfile:
            new_hunk = copy.copy(hunk)
            new_hunk.clear()

            this_hunk_added_lines = 0
            for line in hunk:
                if line.is_added:
                    content = line.value.strip()
                    if content.startswith("Here(") or content.startswith("new Here("):
                        # duplicate here lines
                        for i in range(count - 1):
                            new_hunk.append(copy.copy(line))
                            this_hunk_added_lines += 1

                new_hunk.append(copy.copy(line))

            new_hunk.source_start += added_lines
            new_hunk.target_start += added_lines
            new_hunk.target_length += this_hunk_added_lines
            added_lines += this_hunk_added_lines
            new_pfile.append(new_hunk)

        # print(pfile)
        # print(new_pfile)
        return str(new_pfile)

    def view_result(self, results_file: su.arg.RPath):
        res: IntegratedExpResult = su.io.load(results_file, clz=IntegratedExpResult)
        print(f"===== {res.project} {res.revision} =====")
        if res.metrics is not None:
            print("----- metrics")
            for k, v in res.metrics.items():
                print(f"{k}: {v}")
        print("----- prepare-env-vanilla")
        print(str(res.prepare_env_vanilla))
        print("----- build-vanilla")
        print(str(res.build_vanilla))
        print("----- tests-vanilla")
        for i, x in enumerate(res.tests_vanilla):
            print(f"----- tests-vanilla {i}")
            print(str(x))
        print("----- prepare-env-inline")
        print(str(res.prepare_env_inline))
        print("----- build-inline")
        print(str(res.build_inline))
        print("----- tests-unit")
        for i, x in enumerate(res.tests_unit):
            print(f"----- tests-unit {i}")
            print(str(x))
        print("----- tests-inline")
        for i, x in enumerate(res.tests_inline):
            print(f"----- tests-inline {i}")
            print(str(x))

    def process_results(
        self,
        language: str,
        requests_file: su.arg.RPath,
        results_dirs: List[su.arg.RPath],
        out_dir: su.arg.RPath,
        warmup: int = 1,
    ):
        # load requests
        requests = su.io.load(requests_file, clz=List[IntegratedExpRequest])

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

            # load each project's results
            for request in requests:
                record = {
                    "project": request.project,
                    "revision": "unknown",
                    "duplicating": dup,
                    "error": True,
                    "error-reason": "",
                    "time-vanilla-list": [],
                    "time-vanilla": -1,
                    "time-unit-list": [],
                    "time-unit": -1,
                    "time-inline-list": [],
                    "time-inline": -1,
                    "time-unit-and-inline": -1,
                    "overhead-unit": -1,
                    "overhead-unit-and-inline": -1,
                    "num-vanilla-list": [],
                    "num-vanilla": -1,
                    "num-unit-list": [],
                    "num-unit": -1,
                    "num-inline-list": [],
                    "num-inline": -1,
                    "num-unit-and-inline": -1,
                }
                records.append(record)

                result_file = results_dir / f"{request.project}.json"
                if not result_file.exists():
                    record["error-reason"] = "result file missing"
                    continue
                result = su.io.load(result_file, clz=IntegratedExpResult)

                record["revision"] = result.revision

                # process vanilla env, unit tests results
                if (
                    not result.prepare_env_vanilla.success
                    or not result.build_vanilla.success
                ):
                    record["error-reason"] = "vanilla build failed"
                    continue

                for cmd_res in result.tests_vanilla[warmup:]:
                    if not cmd_res.success:
                        continue
                    record["time-vanilla-list"].append(cmd_res.time)
                    record["num-vanilla-list"].append(
                        get_num_test_from_report(
                            cmd_res.stdout, cmd_res.stderr, language
                        )
                    )
                if len(record["time-vanilla-list"]) == 0:
                    record["error-reason"] = "vanilla tests all failed"
                    continue

                record["time-vanilla"] = np.mean(record["time-vanilla-list"]).item()
                record["num-vanilla"] = max(record["num-vanilla-list"])

                # process inline env, unit tests & inline tests results
                if (
                    not result.prepare_env_inline.success
                    or not result.build_inline.success
                ):
                    record["error-reason"] = "inline build failed"
                    continue

                for cmd_res in result.tests_unit[warmup:]:
                    if not cmd_res.success:
                        continue
                    record["time-unit-list"].append(cmd_res.time)
                    record["num-unit-list"].append(
                        get_num_test_from_report(
                            cmd_res.stdout, cmd_res.stderr, language
                        )
                    )
                if len(record["time-unit-list"]) == 0:
                    record["error-reason"] = "unit tests all failed"
                    continue

                record["time-unit"] = np.mean(record["time-unit-list"]).item()
                record["num-unit"] = max(record["num-unit-list"])

                for cmd_res in result.tests_inline[warmup:]:
                    if not cmd_res.success:
                        continue
                    record["time-inline-list"].append(cmd_res.time)
                    record["num-inline-list"].append(
                        get_num_test_from_report(
                            cmd_res.stdout, cmd_res.stderr, language
                        )
                    )
                if len(record["time-inline-list"]) == 0:
                    record["error-reason"] = "inline tests all failed"
                    continue

                record["time-inline"] = np.mean(record["time-inline-list"]).item()
                record["num-inline"] = max(record["num-inline-list"])

                record["time-unit-and-inline"] = (
                    record["time-unit"] + record["time-inline"]
                )
                record["num-unit-and-inline"] = (
                    record["num-unit"] + record["num-inline"]
                )

                # compute overhead
                record["overhead-unit"] = (
                    record["time-unit"] - record["time-vanilla"]
                ) / record["time-vanilla"]
                record["overhead-unit-and-inline"] = (
                    record["time-unit-and-inline"] - record["time-vanilla"]
                ) / record["time-vanilla"]

                record["error"] = False

        # save the results
        su.io.dump(out_dir / "results.json", records, su.io.Fmt.jsonPretty)

        # compute average results per duplicating
        records_avg = []
        for dup in sorted(seen_dups):
            records_this_dup = [
                r for r in records if r["duplicating"] == dup and not r["error"]
            ]
            record = {"duplicating": dup, "num-project": len(records_this_dup)}
            for x in [
                "time-vanilla",
                "time-unit",
                "time-inline",
                "time-unit-and-inline",
                "num-vanilla",
                "num-unit",
                "num-inline",
                "num-unit-and-inline",
            ]:
                record[f"sum-{x}"] = np.sum([r[x] for r in records_this_dup]).item()
                record[f"avg-{x}"] = np.mean([r[x] for r in records_this_dup]).item()

            record["overhead-unit"] = (
                record["sum-time-unit"] - record["sum-time-vanilla"]
            ) / record["sum-time-vanilla"]
            record["overhead-unit-and-inline"] = (
                record["sum-time-unit-and-inline"] - record["sum-time-vanilla"]
            ) / record["sum-time-vanilla"]
            records_avg.append(record)

        # save the average results
        su.io.dump(out_dir / "results-avg.json", records_avg, su.io.Fmt.jsonPretty)


if __name__ == "__main__":
    su.log.setup(Macros.log_file, level_stderr=su.log.WARNING)
    CLI(IntegratedExperiments, as_positional=False)
