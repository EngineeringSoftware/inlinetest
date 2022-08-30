import collections
import copy
import dataclasses
import re
import time
from pathlib import Path
from subprocess import TimeoutExpired
from typing import Dict, List, Optional, Union

import numpy as np
import seutil as su
from jsonargparse import CLI
from jsonargparse.typing import Path_dc, Path_drw, Path_fc, Path_fr
from tqdm import tqdm
from unidiff import PatchSet

from research.macros import Macros
from research.utils import SUMMARIES_FUNCS

logger = su.log.get_logger(__name__)


@dataclasses.dataclass
class CmdResult:
    cmd: str = None
    success: bool = False
    time: float = None
    timeout: bool = False
    returncode: int = None
    stdout: str = None
    stderr: str = None

    def __str__(self):
        s = f"cmd: {self.cmd}\n"
        s += f"success: {self.success}; time: {self.time}\n"
        if self.timeout:
            s += "TIMEOUT!!!\n"
        else:
            s += f"returncode: {self.returncode}\n"
            s += "--- stdout:\n"
            s += self.stdout + "\n"
            s += "--- stderr:\n"
            s += self.stderr + "\n"
        return s


def run_cmd_timed(command: str, timeout: Optional[int] = None) -> CmdResult:
    res = CmdResult(cmd=command)
    start_time = time.time()
    try:
        rr = su.bash.run(command, timeout=timeout)
    except TimeoutExpired:
        res.success = False
        res.timeout = True
    else:
        res.success = rr.returncode == 0
        res.returncode = rr.returncode
        res.stdout = rr.stdout
        res.stderr = rr.stderr
    finally:
        res.time = time.time() - start_time
    return res


def build_java_inlinetest():
    with su.io.cd(Macros.project_dir / "java"):
        su.bash.run("./install.sh", 0)


def get_num_test_from_report(stdout: str, stderr: str, language: str) -> int:
    if language == "python":
        return _get_num_test_from_report_python(stdout, stderr)
    elif language == "java":
        return _get_num_test_from_report_java(stdout, stderr)
    else:
        raise NotImplementedError(f"{language} not supported")


_re_ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
_re_report_python = re.compile(
    r"^=+ (\d+ \w+, )?(?P<passed>\d+) passed(, \d+ \w+)* in .*=+$"
)


def _get_num_test_from_report_python(stdout: str, stderr: str) -> int:
    stdout_lines = stdout.split("\n")
    for line in stdout_lines[::-1]:
        line = _re_ansi_escape.sub("", line)
        m = _re_report_python.match(line)
        if m is not None:
            return int(m.group("passed"))
    return -1


_re_report_java_inlinetest = re.compile(r"^inline tests passed: (?P<count>\d+)$")
_re_report_java_maven = re.compile(
    r"^(\[[A-Z]+\] )?Tests run: (?P<count>\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)$"
)
_re_report_java_gradle = re.compile(r"^(?P<count>\d+) tests completed(, \d+ \w+)*$")
_re_report_java_gradle_one = re.compile(r"^[\w\d_$]+Test > .* PASSED$")


def _get_num_test_from_report_java(stdout: str, stderr: str) -> int:
    stdout_lines = stdout.split("\n")
    total = 0
    found_gradle_summary = False
    total_gradle_one = 0
    for line in stdout_lines[::-1]:
        line = _re_ansi_escape.sub("", line)

        m = _re_report_java_inlinetest.match(line)
        if m is not None:
            total += int(m.group("count"))
            continue

        m = _re_report_java_maven.match(line)
        if m is not None:
            total += int(m.group("count"))
            continue

        m = _re_report_java_gradle.match(line)
        if m is not None:
            found_gradle_summary = True
            total += int(m.group("count"))
            continue

        m = _re_report_java_gradle_one.match(line)
        if m is not None:
            total_gradle_one += 1
            continue

    if not found_gradle_summary:
        total += total_gradle_one

    if total == 0:
        return -1
    return total


class ExperimentsRunner:
    def find_used_projects(
        self,
        language: str,
        revisions_txt: Optional[Path_fr] = None,
        out_dir: Union[Path_drw, Path_dc, Path] = Macros.data_dir / "projects-used",
    ):
        if not isinstance(out_dir, Path):
            out_dir = Path(out_dir.abs_path)
        if revisions_txt is not None:
            revisions_txt = Path(revisions_txt.abs_path)

        examples = su.io.load(Macros.data_dir / "examples" / f"{language}.yaml")
        full_projects = su.io.load(Macros.data_dir / "projects" / f"{language}.json")
        proj_name2data = {
            x["owner"]["login"] + "_" + x["name"]: x for x in full_projects
        }

        used_proj_names = sorted(set(x["project"] for x in examples))
        logger.info(f"{len(used_proj_names)} projects found")
        for proj in used_proj_names:
            if proj not in proj_name2data:
                raise RuntimeError(f"{proj} data not found in full projects")

        proj_name2revision = collections.defaultdict(lambda: "HEAD")
        if revisions_txt is not None:
            for line in su.io.load(revisions_txt, su.io.Fmt.txtList):
                proj_name, revision = line.split()
                if proj_name.startswith("./"):
                    proj_name = proj_name[2:]
                proj_name2revision[proj_name] = revision

        used_projects = []
        for proj_name in used_proj_names:
            data = proj_name2data[proj_name]
            project = su.project.Project(
                full_name=proj_name,
                url=data["clone_url"],
                data={
                    "revision": proj_name2revision[proj_name],
                    "default_branch": data["default_branch"],
                    "forks_count": data["forks_count"],
                    "stargazers_count": data["stargazers_count"],
                    "open_issues_count": data["open_issues_count"],
                    "size": data["size"],
                },
            )
            used_projects.append(project)

        su.io.dump(out_dir / f"{language}.yaml", used_projects)

    def download_projects(self, language: str):
        projects: List[Project] = su.io.load(
            Macros.data_dir / "projects-used" / f"{language}.yaml", clz=List[Project]
        )
        with tqdm(total=len(projects)) as pbar:
            for project in projects:
                pbar.set_description(f"Cloning {project.full_name}")
                project.clone(Macros.downloads_dir / language)
                project.checkout(project.revision, forced=True)
                pbar.update(1)


if __name__ == "__main__":
    su.log.setup(Macros.log_file, level_stderr=su.log.WARNING)
    CLI(ExperimentsRunner, as_positional=False)
