import collections
from urllib import response
from jsonargparse import CLI
from typing import List
import re
from numpy import False_
from research.macros import Macros
import seutil as su
import os


class Analyze:
    # python -m research.userstudy parse_answers_to_json
    def parse_answers_to_json(
        self,
        directory: str = f"{Macros.project_dir}/userstudy_res/responses",
        include_feedback: bool = True,
    ):
        response_index = 0
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                print("dir", dir)
                if (
                    dir.startswith(".")
                    or dir.startswith("__")
                    or "userstudy" not in dir
                ):
                    continue
                response_index += 1
                res_json = {}
                username = dir.split("_")[0]
                res_txt = su.io.load(f"{directory}/{dir}/README.md", su.io.Fmt.txt)

                # Tasks Time
                res_txt_lines = res_txt.split("\n")
                for index, line in enumerate(res_txt_lines):
                    for task_id in range(1, 5):
                        if (
                            "(at least one) inline tests for a statement" in line
                            and f"({task_id})" in line
                        ):
                            res_json[f"task_{task_id}_understanding_time"] = int(
                                re.findall(r"\d+", res_txt_lines[index + 3])[0]
                            )
                            res_json[f"task_{task_id}_writing_time"] = int(
                                re.findall(r"\d+", res_txt_lines[index + 4])[0]
                            )

                # execute inline tests
                with su.io.cd(f"{directory}/{dir}"):
                    for task_id in range(1, 5):
                        exe_res = su.bash.run(f"pytest task_{task_id}.py").stdout
                        res_json[f"task_{task_id}_num_tests"] = int(
                            re.findall(r"collected (\d+) item", exe_res)[0]
                        )
                        res_json[f"task_{task_id}_time_per_test"] = (
                            res_json[f"task_{task_id}_writing_time"]
                            / res_json[f"task_{task_id}_num_tests"]
                        )
                        res_json[f"task_{task_id}_num_passed_tests"] = int(
                            re.findall(r"(\d+) passed", exe_res)[0]
                        )

                # Q1
                match = re.findall(
                    r"How do you rank the difficulty of learning how to use our framework?((.|\n|\r)*)\(2\)",
                    res_txt,
                )
                if match:
                    difficulty_of_learning_str = match[0][0].split(r">")[1].strip()
                    res_json["difficulty_of_learning"] = int(difficulty_of_learning_str)
                else:
                    raise

                # Q2:
                match = re.findall(
                    r"How do you rank the difficulty of writing inline tests?((.|\n|\r)*)\(3\)",
                    res_txt,
                )

                if match:
                    difficulty_of_using_str = match[0][0].split(r">")[1].strip()
                    res_json["difficulty_of_using"] = int(difficulty_of_using_str)
                else:
                    raise

                # Q3:
                match = re.findall(
                    r"How many total years of programming experience((.|\n|\r)*)\(4\)",
                    res_txt,
                )
                if match:
                    years_str = match[0][0].split(r">")[1].strip()
                    res_json["years_of_programming"] = int(
                        re.findall(r"\d+", years_str)[0]
                    )
                else:
                    raise

                # Q4:
                match = re.findall(
                    r"How do you rank your Python programming expertise?((.|\n|\r)*)\(5\)",
                    res_txt,
                )
                if match:
                    python_expertise_str = match[0][0].split(r">")[1].strip()
                    res_json["python_expertise"] = float(python_expertise_str)
                else:
                    raise

                # Q5:
                res_txt_lines = res_txt.split("\n")
                for index, line in enumerate(res_txt_lines):
                    for task_id in range(1, 5):
                        if line.strip().startswith(f"task {task_id} >"):
                            benefit = line.strip().split(f"task {task_id} >")[1].strip()
                            if (
                                benefit == "yes"
                                or benefit == r"'yes'"
                                or benefit == r'"yes"'
                            ):
                                res_json[f"task_{task_id}_inline_over_unittest"] = 1
                            elif (
                                benefit == "no"
                                or benefit == r"'no'"
                                or benefit == r'"no"'
                            ):
                                res_json[f"task_{task_id}_inline_over_unittest"] = 0
                            else:
                                print(
                                    "inline over unittest:",
                                    benefit,
                                )
                                raise
                            if include_feedback:
                                res_json[f"task_{task_id}_inline_over_unittest_reason"] = (
                                    res_txt_lines[index + 1]
                                    .strip()
                                    .split("rationale (optional) >")[1]
                                    .strip()
                                )

                # Q6:
                if include_feedback:
                    match = re.findall(
                        r"We appreciate your feedback.((.|\n|\r)*)# Response Form",
                        res_txt,
                    )
                    if match:
                        python_expertise_str = match[0][0].strip()
                        res_json["feedback"] = python_expertise_str
                    else:
                        res_json["feedback"] = ""

                    su.io.dump(
                        f"{Macros.results_dir}/userstudy/{username}_reply.json",
                        res_json,
                        su.io.Fmt.jsonPretty,
                    )
                else:
                    su.io.dump(
                        f"{Macros.results_dir}/userstudy/{response_index}_reply.json",
                        res_json,
                        su.io.Fmt.jsonPretty,
                    )


if __name__ == "__main__":
    CLI(Analyze, as_positional=False)
