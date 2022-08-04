from jsonargparse import CLI
import seutil as se
import requests
from research.macros import Macros
from tqdm import tqdm
import os
import re


class Collector:
    def __init__(self):
        pass

    def bash_str_parse_helper(self, bash_str: str):
        bash_str = bash_str.replace(".", r"\.")
        # bash_str = bash_str.replace("(", r"\(")
        return bash_str

    # python -m research.collector filter_examples_with_keywords --language "python" --keyword "re.match"
    def filter_examples_with_keywords(
        self, language: str, keyword: str, exclude_keyword: str = ""
    ):
        if not (Macros.results_dir / "grep").exists():
            (Macros.results_dir / "grep").mkdir()
        search_keyword = self.bash_str_parse_helper(keyword)
        print(
            f"Filter examples with keyword '{search_keyword}' by language: {language}"
        )
        count = 0
        json_res = []
        with se.io.cd(Macros.downloads_dir / language):
            file_suffix = "py" if language == "python" else "java"
            if exclude_keyword:
                search_exclude_keyword = self.bash_str_parse_helper(exclude_keyword)
                print(
                    f"grep -rn '{search_keyword}' --include=*.{file_suffix} | grep -v '{search_exclude_keyword}'"
                )
                res = se.bash.run(
                    f"grep -rn '{search_keyword}' --include=*.{file_suffix} -C 5 | grep -v '{search_exclude_keyword}'"
                ).stdout
            else:
                print(f"grep -rn '{search_keyword}' --include=*.{file_suffix} -C 5")
                res = se.bash.run(
                    f"grep -rn '{search_keyword}' --include=*.{file_suffix} -C 5"
                ).stdout
            for block in re.split("^--", res, flags=re.MULTILINE):
                filename = ""
                line_number_list = []
                line_list = []
                for line in block.split("\n"):
                    if line == "":
                        continue
                    # a special example "keras-team_keras/..."
                    # split_lines = re.split(":|-", line, maxsplit=2)
                    re_line = re.match(r"^(.*)[-:](\d+)[-:](.*)$", line)
                    if not re_line:
                        print("cannot match regex:", line)
                        continue
                    split_lines = re_line.groups()
                    if len(split_lines) < 3:
                        print("length smaller than 3:", line, block)
                        continue
                    filename = split_lines[0]
                    line_number = split_lines[1]
                    line_content = split_lines[2]
                    line_number_list.append(line_number)
                    line_list.append(line_content)
                if filename == "" or len(line_number_list) == 0 or len(line_list) == 0:
                    print(
                        "filename or line_number_list or line_list is empty:",
                        line,
                        block,
                    )
                    continue
                json_res.append(
                    {
                        "filename": filename,
                        "line_number": ",".join(line_number_list),
                        "line_content": line_list,
                        "inline": "",
                    }
                )
                count += 1

        print(f"{count} examples found")
        file_index = 1
        for json_file in os.listdir(Macros.results_dir / "grep"):
            if json_file.endswith(".json"):
                file_index += 1
        se.io.dump(
            f"{Macros.results_dir}/grep/examples_{language}_{file_index}.json",
            json_res,
            se.io.Fmt.jsonPretty,
        )

    # python -m research.collector filter_projects --language "python"
    def filter_projects(self, language: str):
        print(f"Filter projects by language: {language}")
        url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page=100"
        headers = {"Authorization": "Token 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"}
        response = requests.get(url, headers=headers)
        if response.ok:
            projects = response.json()["items"]
            print(f"{len(projects)} {language} projects found")

            json_list = []
            txt_list = []
            txt_list.append(["project", "URL", "examples"])
            for project in projects:
                if project["full_name"] in Macros.tutorial_projects:
                    print(project["full_name"] + " is a tutorial project")
                    continue
                project["examples"] = []
                json_list.append(project)
                txt_list.append([project["full_name"], project["clone_url"], ""])
            se.io.dump(
                f"{Macros.data_dir}/projects/{language}.json",
                json_list,
                se.io.Fmt.jsonPretty,
            )
            se.io.dump(
                f"{Macros.data_dir}/projects/{language}.txt",
                txt_list,
                se.io.Fmt.txtList,
            )

    # python -m research.collector download_projects --language "python"
    def download_projects(self, language: str):
        print(f"Download projects by language: {language}")
        projects = se.io.load(f"{Macros.data_dir}/projects/{language}.json")
        (Macros.downloads_dir / language).mkdir(exist_ok=True)
        with se.io.cd(Macros.downloads_dir / language):
            for project in tqdm(projects):
                project_folder = project["full_name"].replace("/", "_")
                if os.path.exists(
                    Macros.downloads_dir / language / f"{project_folder}"
                ):
                    continue
                print(f"Downloading {project['full_name']}")
                se.bash.run("git clone " + project["clone_url"] + " " + project_folder)


if __name__ == "__main__":
    CLI(Collector, as_positional=False)
