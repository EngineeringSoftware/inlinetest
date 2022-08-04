from jsonargparse import CLI
import seutil as se
from research.macros import Macros
import ast
import collections
import os
from research.inline_test import ExtractInlineTest
import re
import random

class Filter:
    def __init__(self):
        pass

    # python -m research.filter index_to_keyword
    def index_to_keyword(self, file_index: int):
        keyword_dict = dict()
        keywords = se.io.load(
            Macros.results_dir / "grep" / "keywords.txt", se.io.Fmt.txtList
        )
        for index, keyword in enumerate(keywords):
            keyword_dict[index + 1] = keyword
        return keyword_dict[file_index]

    # python -m research.filter filter --filename "examples_java_1.json"
    def filter(self, filename: str):
        res = se.io.load(Macros.results_dir / "grep" / filename)
        keyword = self.index_to_keyword(int(filename.split(".")[0].split("_")[-1]))
        filtered_res = []
        for item in res:
            file_suffix = item["filename"].split("/")[-1]
            # filter out test
            if "test" in file_suffix or "Test" in file_suffix:
                continue
            # filter out return statement
            elif "return" in item["line_content"]:
                continue
            else:
                filtered_res.append(item)
        (Macros.results_dir / "filter").mkdir(exist_ok=True)
        se.io.dump(
            Macros.results_dir / "filter" / filename, filtered_res, se.io.Fmt.jsonPretty
        )

    # python -m research.filter method_extractor --filename "examples_python_9.json"
    def method_extractor(self, filename: str, project_appearance_times: int = 1):
        if (Macros.results_dir / "method").exists():
            se.bash.run(f"rm -rf {Macros.results_dir}/method")
        (Macros.results_dir / "method").mkdir()
        grepped_file = se.io.load(Macros.results_dir / "grep" / filename)
        checked_repos = collections.Counter()
        index = 0
        for grepped in grepped_file:
            if "test" in grepped["filename"]:
                continue
            repo = grepped["filename"].split("/")[0]
            if checked_repos[repo] < project_appearance_times:
                line_numbers = grepped["line_number"].split(",")
                # extract method
                filename = grepped["filename"]
                if filename.endswith(".java"):
                    language = "java"
                elif filename.endswith(".py"):
                    language = "python"
                f = open(f"{Macros.downloads_dir}/{language}/{filename}", "r")
                file_content = f.read()
                try:
                    tree = ast.parse(file_content)
                except SyntaxError:
                    continue
                analyzer = Analyzer(int(line_numbers[0]))
                analyzer.visit(tree)
                if analyzer.start != -1:
                    method = "\n".join(
                        file_content.splitlines()[analyzer.start - 1 : analyzer.end]
                    )
                    method += f"\n{filename}: {analyzer.start}-{analyzer.end}"
                    se.io.dump(
                        Macros.results_dir
                        / "method"
                        / f"{index}_{repo}_{filename.split('/')[-1]}",
                        method,
                        se.io.Fmt.txt,
                    )
                    print(f"{filename}: {analyzer.start}-{analyzer.end}")
                    index += 1
                    checked_repos[repo] += 1

    # python -m research.filter count_statement_with_tests
    @classmethod
    def count_statement_with_tests(
        cls, filename_regex: str = "^(bit|collection|regex|string)"
    ):
        file_name_to_statements = collections.defaultdict(set)
        file_name_to_inline_tests = collections.defaultdict(set)
        for filename in os.listdir(Macros.project_dir / "api" / "python"):
            if filename.endswith(".py") and re.match(filename_regex, filename):
                f = open((Macros.project_dir / "api" / "python" / filename), "r")
                tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    for child in ast.iter_child_nodes(node):
                        child.parent = node
                        if isinstance(child, ast.stmt):
                            # print("child:", ExtractInlineTest.node_to_source_code(child))
                            # print("parent:", ExtractInlineTest.node_to_source_code(node))
                            # print()
                            node.children = (
                                [child]
                                if not hasattr(node, "children")
                                else [child] + node.children
                            )

                for node in ast.walk(tree):
                    if isinstance(
                        node, ast.Call
                    ) and ExtractInlineTest.is_inline_test_class(node):
                        # is inline test
                        file_name_to_inline_tests[filename].add(node.lineno)
                        stmt_node = node.parent
                        while not isinstance(stmt_node, ast.Expr):
                            stmt_node = stmt_node.parent
                        index_stmt_node = stmt_node.parent.children.index(stmt_node)
                        if index_stmt_node >= len(stmt_node.parent.children) - 1:
                            print("No previous sibling")
                        else:
                            for i in range(
                                1, len(stmt_node.parent.children) - index_stmt_node
                            ):
                                prev_stmt_node = stmt_node.parent.children[
                                    index_stmt_node + i
                                ]
                                if isinstance(
                                    prev_stmt_node.value, ast.Call
                                ) and ExtractInlineTest.is_inline_test_class(
                                    prev_stmt_node.value
                                ):
                                    continue
                                else:
                                    file_name_to_statements[filename].add(
                                        prev_stmt_node.lineno
                                    )
                                    break
                if filename not in file_name_to_statements:
                    print(f"{filename} has no tested statements")

        tested_statements = sum([len(v) for v in file_name_to_statements.values()])
        inline_tests = sum([len(v) for v in file_name_to_inline_tests.values()])
        print(f"file_name_to_statements: {tested_statements}")
        print(f"file_name_to_inline_tests: {inline_tests}")
        return (tested_statements, inline_tests)

    # python -m research.filter random_example --language "python"
    def random_example(self, language: str = "python", num_examples: int = 100):
        existing_examples = se.io.load(Macros.data_dir / "examples" / f"{language}.yaml", se.io.Fmt.yaml)
        for existing_example in existing_examples:
            existing_example["path"] = existing_example["project"] + "/" + existing_example["path"]
        random.seed(42)
        grepped_files = []
        for filename in os.listdir(Macros.results_dir / "grep"):
            if re.match(".*python.*\.json", filename):
                grepped_files.append(filename) 
        grepped_contents = []
        for grepped_file in grepped_files:
            grepped_content = se.io.load(Macros.results_dir / "grep" / grepped_file)
            for item in grepped_content:
                if "inline" in item and item["inline"] != "":
                    exist = False
                    for existing_example in existing_examples:
                        if item["filename"] == existing_example["path"] and str(existing_example["line"]) in item["line_number"]:
                            exist = True
                            break
                    if not exist:
                        item["support"] = ""
                        grepped_contents.append(item)
            random.shuffle(grepped_contents)
        se.io.dump(Macros.results_dir / f"random_example_{language}.json", grepped_contents[:num_examples], se.io.Fmt.jsonPretty)

        
class Analyzer(ast.NodeVisitor):
    def __init__(self, func_lineno):
        self.func_lineno = func_lineno
        self.start = -1
        self.end = -1

    def visit_FunctionDef(self, node):
        if node.lineno <= self.func_lineno <= node.end_lineno:
            self.start = node.lineno
            self.end = node.end_lineno
        self.generic_visit(node)


if __name__ == "__main__":
    CLI(Filter, as_positional=False)
