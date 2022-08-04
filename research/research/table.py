import collections
import os
from statistics import mean, median
from typing import List, Optional

import seutil as su
from jsonargparse import CLI
from seutil import latex
from seutil.project import Project

from research.filter import Filter
from research.macros import Macros
from research.utils import SUMMARIES_FUNCS


class Table:
    # python -m research.table table_inline_tests_category
    def table_inline_tests_category(
        self,
        category: List[str] = ["Regex", "String", "Bit", "Collection", "Stream"],
        header: List[str] = ["PL", "Projs", "Files", "TestedStmts", "InlineTests"],
    ):
        file = latex.File(Macros.table_dir / f"table-inline-tests-category.tex")
        file.append(r"\begin{table}[h]")
        file.append(r"\begin{center}")
        file.append(r"\caption{\CaptionInlineTestsCategory}")
        file.append(r"\vspace{-10px}")
        file.append(r"\scalebox{0.85}{")
        file.append(r"\begin{tabular}{|l|l|l|l|l|l|}")
        file.append(r"\hline")
        file.append(r"\HeaderCategory")
        for h in header:
            file.append(r"& \Header" + h)
        file.append(r"\\ \hline")

        for c in category:
            for lang in ["Python", "Java"]:
                if (lang == "Python" and c == "Stream") or (
                    lang == "Java" and c == "Collection"
                ):
                    continue
                if lang == "Python" and c in ["Regex", "String", "Bit"]:
                    file.append(r"\multirow{2}{*}{" + c + "}")
                if c in ["Collection", "Stream"]:
                    file.append(c)
                for h in header:
                    if h == "PL":
                        file.append(r" & " + lang)
                    else:
                        file.append(r" & \UseMacro{Num" + lang + c + h + r"}")
                if lang == "Python" and c in ["Regex", "String", "Bit"]:
                    file.append(r"\\ \cline{2-6}")
                else:
                    file.append(r"\\ \hline")
        file.append(r"\end{tabular}")
        file.append(r"}")
        file.append(r"\label{table:category-stat}")
        file.append(r"\end{center}")
        file.append(r"\end{table}")
        file.save()

    # python -m research.table data_python_inline_tests_category
    def data_python_inline_tests_category(
        self,
        category: List[str] = ["Regex", "String", "Bit", "Collection"],
    ):
        file = latex.File(Macros.table_dir / f"data-python-inline-tests-category.tex")

        python_examples = su.io.load(Macros.data_dir / "examples" / f"python.yaml")

        projects_set = set([x["project"] for x in python_examples])
        total_examples = len(python_examples)
        total_inline_tests = 0
        total_tested_stmts = 0

        for c in category:
            (
                number_of_tested_stmts,
                number_of_inline_tests,
            ) = Filter.count_statement_with_tests(f"^{c.lower()}")
            total_inline_tests += number_of_inline_tests
            total_tested_stmts += number_of_tested_stmts
            file.append_macro(
                latex.Macro(f"NumPython{c}TestedStmts", number_of_tested_stmts)
            )
            file.append_macro(
                latex.Macro(f"NumPython{c}InlineTests", number_of_inline_tests)
            )
            num_of_projects = len(
                {
                    x["project"]
                    for x in python_examples
                    if x["name"].startswith(c.lower())
                }
            )
            file.append_macro(latex.Macro(f"NumPython{c}Projs", num_of_projects))
            num_of_files = len(
                {x["name"] for x in python_examples if x["name"].startswith(c.lower())}
            )
            file.append_macro(latex.Macro(f"NumPython{c}Files", num_of_files))

        file.append_macro(latex.Macro(f"NumPythonProjs", len(projects_set)))
        file.append_macro(latex.Macro(f"NumPythonFiles", total_examples))
        file.append_macro(latex.Macro(f"NumPythonInlineTests", total_inline_tests))
        file.append_macro(latex.Macro(f"NumPythonTestedStmts", total_tested_stmts))

        file.save()

    # python -m research.table data_java_inline_tests_category
    def data_java_inline_tests_category(
        self,
        category: List[str] = ["Regex", "String", "Bit", "Stream"],
    ):
        file = latex.File(Macros.table_dir / f"data-java-inline-tests-category.tex")

        all_java_examples = su.io.load(Macros.data_dir / "examples" / f"java.yaml")

        projects_set = {x["project"] for x in all_java_examples}
        total_examples = len(all_java_examples)
        total_inline_tests = 0
        total_tested_stmts = 0

        for c in category:
            tested_stmt_lines = collections.defaultdict(set)
            inline_test_lines = collections.defaultdict(set)
            java_examples = [
                x for x in all_java_examples if x["name"].startswith(c.lower())
            ]
            java_files = {x["name"] + ".java" for x in java_examples}
            for java_file in java_files:
                with su.io.cd(Macros.project_dir / "java"):
                    bash_res = su.bash.run(
                        f"mvn exec:java -Dexec.mainClass='org.inlinetest.InlineTestRunnerSourceCode' -Dexec.args='--input_file={Macros.api_dir}/java/{java_file} --output_mode=new --assertion_style=assert'"
                    ).stdout
                    bash_res = bash_res.split("\n")
                    for bash_line in bash_res:
                        if bash_line.startswith("tested stmt lineno:"):
                            tested_stmt_lines[java_file].add(
                                int(bash_line.split(":")[-1].strip())
                            )
                        if bash_line.startswith("inline test lineno:"):
                            inline_test_lines[java_file].add(
                                int(bash_line.split(":")[-1].strip())
                            )

            number_of_tested_stmts = sum([len(x) for x in tested_stmt_lines.values()])
            file.append_macro(
                latex.Macro(f"NumJava{c}TestedStmts", number_of_tested_stmts)
            )
            total_tested_stmts += number_of_tested_stmts
            number_of_inline_tests = sum([len(x) for x in inline_test_lines.values()])
            file.append_macro(
                latex.Macro(f"NumJava{c}InlineTests", number_of_inline_tests)
            )
            total_inline_tests += number_of_inline_tests

            java_projects = {x["project"] for x in java_examples}
            file.append_macro(latex.Macro(f"NumJava{c}Projs", len(java_projects)))
            file.append_macro(latex.Macro(f"NumJava{c}Files", len(java_examples)))

        file.append_macro(latex.Macro(f"NumJavaTestedStmts", total_tested_stmts))
        file.append_macro(latex.Macro(f"NumJavaInlineTests", total_inline_tests))
        file.append_macro(latex.Macro(f"NumJavaProjs", len(projects_set)))
        file.append_macro(latex.Macro(f"NumJavaFiles", total_examples))
        file.save()

    # python -m research.table data_userstudy_res
    def data_userstudy_res(
        self, userstudy_dir: str = f"{Macros.results_dir}/userstudy"
    ):
        file = latex.File(Macros.table_dir / f"data-userstudy-res.tex")
        records = []
        for userstudy_file in os.listdir(userstudy_dir):
            if userstudy_file.endswith(".json"):
                records.append(su.io.load(f"{userstudy_dir}/{userstudy_file}"))
        print(records[0])

        metrics = collections.defaultdict(list)
        metrics_summary = {}
        metric_names = [
            "difficulty_of_learning",
            "difficulty_of_using",
            "years_of_programming",
            "python_expertise",
        ]
        for task_id in range(1, 5):
            metric_names.append(f"task_{task_id}_time_per_test")
            metric_names.append(f"task_{task_id}_understanding_time")
            metric_names.append(f"task_{task_id}_writing_time")
            metric_names.append(f"task_{task_id}_num_tests")
            metric_names.append(f"task_{task_id}_num_passed_tests")
        for m in metric_names:
            for r in records:
                metrics[m].append(r[m])

            for s, f in SUMMARIES_FUNCS.items():
                metrics_summary[f"{s}_{m}"] = f(metrics[m])

        for k, v in metrics_summary.items():
            file.append_macro(latex.Macro(k, f"{v:.1f}"))

        for m in ["time_per_test", "understanding_time", "writing_time", "num_tests"]:
            avg_value_list = []
            median_value_list = []
            for task_id in range(1, 5):
                avg_value_list.append(metrics_summary[f"AVG_task_{task_id}_{m}"])
                median_value_list.append(metrics_summary[f"MEDIAN_task_{task_id}_{m}"])
            file.append_macro(latex.Macro(f"AVG_{m}", f"{mean(avg_value_list):.1f}"))
            file.append_macro(
                latex.Macro(f"MEDIAN_{m}", f"{median(avg_value_list):.1f}")
            )

        benefits = collections.Counter()
        correct_times = collections.Counter()
        for task_id in range(1, 5):
            for r in records:
                # r[f"task_{task_id}_inline_over_unittest"] 1 means yes and 0 means no
                benefits[f"task_{task_id}_benefit"] += r[
                    f"task_{task_id}_inline_over_unittest"
                ]
                correct_times[f"task_{task_id}_correct_times"] += (
                    1
                    if r[f"task_{task_id}_num_passed_tests"]
                    == r[f"task_{task_id}_num_tests"]
                    else 0
                )
        for k, v in benefits.items():
            file.append_macro(latex.Macro(k, v))
        for k, v in correct_times.items():
            file.append_macro(latex.Macro(k, v))
        file.append_macro(latex.Macro("NumUsers", len(records)))
        file.save()

    # python -m research.table table_userstudy_res
    def table_userstudy_res(
        self, userstudy_dir: str = f"{Macros.results_dir}/userstudy"
    ):
        file = latex.File(Macros.table_dir / f"table-userstudy-res.tex")
        file.append(r"\begin{table}[h]")
        file.append(r"\begin{center}")
        file.append(r"\caption{\TitleUserStudyResults}")
        file.append(r"\vspace{-10px}")
        file.append(r"\scalebox{0.82}{")
        file.append(r"\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|}")
        file.append(r"\hline")

        file.append(
            r"\HeaderTask & \multicolumn{2}{l|}{\HeaderUnderstandingTime} &  \multicolumn{2}{l|}{\HeaderWritingTime} &  \multicolumn{2}{l|}{\HeaderNumTests} &  \multicolumn{2}{l|}{\HeaderWritingTimePerTest} & \HeaderNumPassedTests & \HeaderBenefits \\"
        )
        file.append(r"\cline{2-9}")
        file.append(
            r" & \HeaderAvg & \HeaderMed & \HeaderAvg & \HeaderMed & \HeaderAvg & \HeaderMed & \HeaderAvg & \HeaderMed & & \\"
        )
        file.append(r"\hline")
        for task_id in range(1, 5):
            file.append(str(task_id))
            file.append(
                r" & \UseMacro{" + f"AVG_task_{task_id}_understanding_time" + r"}"
            )
            file.append(
                r" & \UseMacro{" + f"MEDIAN_task_{task_id}_understanding_time" + r"}"
            )
            file.append(r" & \UseMacro{" + f"AVG_task_{task_id}_writing_time" + r"}")
            file.append(r" & \UseMacro{" + f"MEDIAN_task_{task_id}_writing_time" + r"}")
            file.append(r" & \UseMacro{" + f"AVG_task_{task_id}_num_tests" + r"}")
            file.append(r" & \UseMacro{" + f"MEDIAN_task_{task_id}_num_tests" + r"}")
            file.append(r" & \UseMacro{" + f"AVG_task_{task_id}_time_per_test" + r"}")
            file.append(
                r" & \UseMacro{" + f"MEDIAN_task_{task_id}_time_per_test" + r"}"
            )
            file.append(
                r" & \UseMacro{"
                + f"task_{task_id}_correct_times"
                + r"}"
                + "/"
                + r"\UseMacro{NumUsers}"
            )
            file.append(
                r" & \UseMacro{"
                + f"task_{task_id}_benefit"
                + r"}"
                + "/"
                + r"\UseMacro{NumUsers}"
            )
            file.append(r"\\")
            file.append(r"\hline")
        # Avg
        file.append(r"\HeaderAvg")
        file.append(r" & \UseMacro{AVG_understanding_time}")
        file.append(r" & \UseMacro{MEDIAN_understanding_time}")
        file.append(r" & \UseMacro{AVG_writing_time}")
        file.append(r" & \UseMacro{MEDIAN_writing_time}")
        file.append(r" & \UseMacro{AVG_num_tests}")
        file.append(r" & \UseMacro{MEDIAN_num_tests}")
        file.append(r" & \UseMacro{AVG_time_per_test}")
        file.append(r" & \UseMacro{MEDIAN_time_per_test}")
        file.append(r" & \HeaderNA")
        file.append(r" & \HeaderNA")
        file.append(r"\\")
        file.append(r"\hline")

        file.append(r"\end{tabular}")
        file.append(r"}")
        file.append(r"\label{table:user-study-res}")
        file.append(r"\end{center}")
        file.append(r"\end{table}")
        file.save()

    def data_combine_languages(self):
        languages = ["java", "python"]

        file = latex.File(Macros.table_dir / "data-combine-languages.tex")
        metrics = collections.defaultdict(int)

        # combine data-$lang-inline-tests-category
        for lang in languages:
            macros = latex.Macro.load_from_file(
                Macros.table_dir / f"data-{lang}-inline-tests-category.tex"
            )
            metrics["NumTotalProjs"] += macros[f"Num{lang.capitalize()}Projs"].value
            metrics["NumTotalFiles"] += macros[f"Num{lang.capitalize()}Files"].value
            metrics["NumTotalInlineTests"] += macros[
                f"Num{lang.capitalize()}InlineTests"
            ].value
            metrics["NumTotalTestedStmts"] += macros[
                f"Num{lang.capitalize()}TestedStmts"
            ].value

        # combine skips
        for lang in languages:
            macros = latex.Macro.load_from_file(
                Macros.table_dir / f"data-exp-skips-{lang}.tex"
            )
            metrics["exp-total-proj-can-run-unit-tests"] += macros[
                f"exp-{lang}-proj-can-run-unit-tests"
            ].value
            metrics[f"exp-{lang}-skipped-all"] = (
                macros[f"exp-{lang}-skipped"].value
                + macros[f"exp-{lang}-skipped-unit-tests"].value
            )
            metrics["exp-total-skipped-all"] += metrics[f"exp-{lang}-skipped-all"]

        for k, v in metrics.items():
            if isinstance(v, int):
                fmt = ",d"
            else:
                fmt = ",.2f"
            file.append_macro(latex.Macro(k, f"{v:{fmt}}"))

        file.save()

    def data_exp_standalone(
        self,
        language: str,
        duplicatings: List[int] = [1, 10, 100, 1000],
        results_dir: Optional[su.arg.RPath] = None,
        out_file: Optional[su.arg.RPath] = None,
    ):
        if results_dir is None:
            results_dir = Macros.results_dir / "exp" / "standalone" / language
        if out_file is None:
            out_file = Macros.table_dir / f"data-exp-standalone-{language}.tex"
        file = latex.File(out_file)
        records = su.io.load(results_dir / "results.json")

        for dup in duplicatings:
            records_this_dup = [r for r in records if r["duplicating"] == dup]

            metrics = collections.defaultdict(list)
            for r in records_this_dup:
                metrics["num"].append(r["num"])
                metrics["time"].append(r["time"])
                metrics["timept"].append([r["time"] / r["num"]])

            metrics_summary = {}
            for m, l in metrics.items():
                for s, f in SUMMARIES_FUNCS.items():
                    metrics_summary[f"{m}-{s}"] = f(l)
            metrics_summary["timept-MACROAVG"] = (
                metrics_summary["time-SUM"] / metrics_summary["num-SUM"]
            )

            for k, v in metrics_summary.items():
                if isinstance(v, int):
                    fmt = ",d"
                elif "timept" in k:
                    fmt = ",.3f"
                else:
                    fmt = ",.2f"
                file.append_macro(
                    latex.Macro(f"exp-{language}-{k}-dup{dup}-its", f"{v:{fmt}}")
                )

        file.save()

    def table_exp_standalone(
        self,
        language: str,
        duplicatings: List[int] = [1, 10, 100, 1000],
        out_file: Optional[su.arg.RPath] = None,
    ):
        if out_file is None:
            out_file = Macros.table_dir / f"table-exp-standalone-{language}.tex"
        file = latex.File(out_file)

        file.append(r"\begin{tabular}{|l@{\hspace{2pt}}|@{\hspace{2pt}}r|r|r|}")
        file.append(r"\hline")
        file.append(
            r"\HeaderDup & \HeaderNumITStandalone & \HeaderTimeITStandalone & \HeaderTimePerTestITStandalone \\"
        )
        file.append(r"\hline")

        for dup in duplicatings:
            file.append(latex.Macro(f"dup-{dup}").use())
            for m in ["num", "time"]:
                file.append(
                    " & " + latex.Macro(f"exp-{language}-{m}-SUM-dup{dup}-its").use()
                )
            file.append(
                " & "
                + latex.Macro(f"exp-{language}-timept-MACROAVG-dup{dup}-its").use()
            )
            file.append(r" \\")

        file.append(r"\hline")
        file.append(r"\end{tabular}")

        file.save()

    def data_exp_skips(
        self,
        language: str,
        examples_file: Optional[su.arg.RPath] = None,
        results_dir: Optional[su.arg.RPath] = None,
        out_file: Optional[su.arg.RPath] = None,
    ):
        if examples_file is None:
            examples_file = Macros.data_dir / "examples" / f"{language}.yaml"
        if results_dir is None:
            results_dir = Macros.results_dir / "exp" / "integrated" / language
        if out_file is None:
            out_file = Macros.table_dir / f"data-exp-skips-{language}.tex"

        examples = su.io.load(examples_file)
        proj_names = sorted(set([x["project"] for x in examples]))

        file = latex.File(out_file)

        # analyze the project counts
        file.append_macro(latex.Macro(f"exp-{language}-proj-initial", len(proj_names)))

        skipped = su.io.load(results_dir / "skipped.yaml")
        file.append_macro(latex.Macro(f"exp-{language}-skipped", len(skipped)))
        for x in skipped:
            proj_names.remove(x)
        file.append_macro(latex.Macro(f"exp-{language}-proj-can-run", len(proj_names)))
        skipped_reasons = collections.Counter(skipped.values())
        for reason, count in skipped_reasons.items():
            reason = reason.replace(" ", "-")
            file.append_macro(latex.Macro(f"exp-{language}-skipped-{reason}", count))

        skipped_unit_tests = su.io.load(results_dir / "skipped-unit-tests.yaml")
        for x in skipped:
            if x in skipped_unit_tests:
                del skipped_unit_tests[x]
        file.append_macro(
            latex.Macro(f"exp-{language}-skipped-unit-tests", len(skipped_unit_tests))
        )
        for x in skipped_unit_tests:
            proj_names.remove(x)
        file.append_macro(
            latex.Macro(f"exp-{language}-proj-can-run-unit-tests", len(proj_names))
        )
        skipped_unit_tests_reasons = collections.Counter(skipped_unit_tests.values())
        for reason, count in skipped_unit_tests_reasons.items():
            reason = reason.replace(" ", "-")
            file.append_macro(
                latex.Macro(f"exp-{language}-skipped-unit-tests-{reason}", count)
            )

        file.save()

    def data_exp_integrated(
        self,
        language: str,
        duplicatings: List[int] = [1, 10, 100, 1000],
        results_dir: Optional[su.arg.RPath] = None,
        out_file: Optional[su.arg.RPath] = None,
    ):
        if results_dir is None:
            results_dir = Macros.results_dir / "exp" / "integrated" / language
        if out_file is None:
            out_file = Macros.table_dir / f"data-exp-integrated-{language}.tex"

        file = latex.File(out_file)

        records = su.io.load(results_dir / "results.json")
        # compute time per test
        for record in records:
            if record["error"]:
                for mode in ["vanilla", "unit", "inline", "unit-and-inline"]:
                    record[f"timept-{mode}"] = -1
            else:
                for mode in ["vanilla", "unit", "inline", "unit-and-inline"]:
                    record[f"timept-{mode}"] = (
                        record[f"time-{mode}"] / record[f"num-{mode}"]
                    )

        for dup in duplicatings:
            metrics = collections.defaultdict(list)
            records_this_dup = [r for r in records if r["duplicating"] == dup]
            for record in records_this_dup:
                project = record["project"]

                for m in [
                    f"{x}-{y}"
                    for x in ["time", "num", "timept"]
                    for y in ["vanilla", "unit", "inline", "unit-and-inline"]
                ] + [f"overhead-{y}" for y in ["unit", "unit-and-inline"]]:
                    if not record["error"]:
                        metrics[m].append(record[m])

                    v = record[m]
                    if isinstance(v, int):
                        fmt = ",d"
                    elif "overhead" in m or "timept" in m:
                        fmt = ",.3f"
                    else:
                        fmt = ",.2f"
                    if v == -1:
                        v = "ERROR"
                        fmt = "s"

                    file.append_macro(
                        latex.Macro(
                            f"exp-{language}-{project}-{m}-dup{dup}",
                            f"{v:{fmt}}",
                        )
                    )

            metrics_summary = {}
            for m, l in metrics.items():
                for s, f in SUMMARIES_FUNCS.items():
                    metrics_summary[f"{m}-{s}"] = f(l)
            for x in ["vanilla", "unit", "inline", "unit-and-inline"]:
                metrics_summary[f"timept-{x}-MACROAVG"] = (
                    metrics_summary[f"time-{x}-SUM"] / metrics_summary[f"num-{x}-SUM"]
                )
            for x in ["unit", "unit-and-inline"]:
                metrics_summary[f"overhead-{x}-MACROAVG"] = (
                    metrics_summary[f"time-{x}-SUM"]
                    - metrics_summary[f"time-vanilla-SUM"]
                ) / metrics_summary["time-vanilla-SUM"]
            for m, v in metrics_summary.items():
                if isinstance(v, int):
                    fmt = ",d"
                elif "overhead" in m or "timept" in m:
                    fmt = ",.3f"
                else:
                    fmt = ",.2f"

                file.append_macro(
                    latex.Macro(f"exp-{language}-{m}-dup{dup}", f"{v:{fmt}}")
                )

        file.save()

    def table_exp_integrated(
        self,
        language: str,
        requests_file: Optional[su.arg.RPath] = None,
        out_file: Optional[su.arg.RPath] = None,
    ):
        if requests_file is None:
            requests_file = Macros.data_dir / "exp" / "integrated" / f"{language}.yaml"
        if out_file is None:
            out_file = Macros.table_dir / f"table-exp-integrated-{language}.tex"

        requests = su.io.load(requests_file)
        proj_names = sorted(r["project"] for r in requests)

        file = latex.File(out_file)

        file.append(r"\begin{tabular}{|l|r|r||r|r||r|r|r||r|r|r|}")
        file.append(r"\hline")
        file.append(
            r"\HeaderProj & \HeaderNumVanilla & \HeaderNumITOnly"
            + r" & \HeaderTimeVanilla & \HeaderTimePerTestVanilla"
            + r" & \HeaderTimeITEnabled & \HeaderTimePerTestITEnabled & \HeaderOverheadITEnabled"
            + r" & \HeaderTimeITDisabled & \HeaderTimePerTestITDisabled & \HeaderOverheadITDisabled \\"
        )
        file.append(r"\hline")
        columns = [
            "num-vanilla",
            "num-inline",
            "time-vanilla",
            "timept-vanilla",
            "time-unit-and-inline",
            "timept-unit-and-inline",
            "overhead-unit-and-inline",
            "time-unit",
            "timept-unit",
            "overhead-unit",
        ]
        for proj in proj_names:
            file.append(latex.Macro(f"proj-{proj}").use())
            for m in columns:
                file.append(
                    " & " + latex.Macro(f"exp-{language}-{proj}-{m}-dup1").use()
                )
            file.append(r" \\")
        file.append(r"\hline")
        file.append(r"\HeaderAvg")
        for m in columns:
            if "overhead" in m or "timept" in m:
                file.append(
                    " & " + latex.Macro(f"exp-{language}-{m}-MACROAVG-dup1").use()
                )
            else:
                file.append(" & " + latex.Macro(f"exp-{language}-{m}-AVG-dup1").use())
        file.append(r" \\")
        file.append(r"\HeaderSum")
        for m in columns:
            if "overhead" in m or "timept" in m:
                file.append(r" & \HeaderNA")
            else:
                file.append(" & " + latex.Macro(f"exp-{language}-{m}-SUM-dup1").use())
        file.append(r" \\")
        file.append(r"\hline")
        file.append(r"\end{tabular}")

        file.save()

    def table_exp_integrated_dups(
        self,
        language: str,
        duplicatings: List[int] = [1, 10, 100, 1000],
        out_file: Optional[su.arg.RPath] = None,
    ):
        if out_file is None:
            out_file = Macros.table_dir / f"table-exp-integrated-dups-{language}.tex"

        file = latex.File(out_file)

        file.append(r"\begin{tabular}{|l|r|r||r|r||r|r|r||r|r|r|}")
        file.append(r"\hline")
        file.append(
            r"\HeaderDup & \HeaderNumVanilla & \HeaderNumITOnly"
            + r" & \HeaderTimeVanilla & \HeaderTimePerTestVanilla"
            + r" & \HeaderTimeITEnabled & \HeaderTimePerTestITEnabled & \HeaderOverheadITEnabled"
            + r" & \HeaderTimeITDisabled & \HeaderTimePerTestITDisabled & \HeaderOverheadITDisabled \\"
        )
        file.append(r"\hline")
        columns = [
            "num-vanilla",
            "num-inline",
            "time-vanilla",
            "timept-vanilla",
            "time-unit-and-inline",
            "timept-unit-and-inline",
            "overhead-unit-and-inline",
            "time-unit",
            "timept-unit",
            "overhead-unit",
        ]
        for dup in duplicatings:
            file.append(latex.Macro(f"dup-{dup}").use())
            for m in columns:
                if "overhead" in m or "timept" in m:
                    file.append(
                        " & "
                        + latex.Macro(f"exp-{language}-{m}-MACROAVG-dup{dup}").use()
                    )
                else:
                    file.append(
                        " & " + latex.Macro(f"exp-{language}-{m}-SUM-dup{dup}").use()
                    )
            file.append(r" \\")
        file.append(r"\hline")
        file.append(r"\end{tabular}")

        file.save()


if __name__ == "__main__":
    CLI(Table, as_positional=False)
