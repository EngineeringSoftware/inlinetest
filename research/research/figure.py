import os
import random
from statistics import mean
from typing import List

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import seutil as su
from jsonargparse import CLI

from research.macros import Macros


class Figure:
    def __init__(self):
        sns.set()
        sns.set_context("paper")
        # Set matplotlib fonts
        mpl.rcParams["axes.titlesize"] = 18
        mpl.rcParams["axes.labelsize"] = 18
        mpl.rcParams["font.size"] = 14
        mpl.rcParams["xtick.labelsize"] = 18
        mpl.rcParams["xtick.major.size"] = 8
        mpl.rcParams["xtick.minor.size"] = 8
        mpl.rcParams["ytick.labelsize"] = 18
        mpl.rcParams["ytick.major.size"] = 8
        mpl.rcParams["ytick.minor.size"] = 8
        mpl.rcParams["legend.fontsize"] = 14
        mpl.rcParams["legend.title_fontsize"] = 14

    # python -m research.figure figure_expertise
    # x-axis: expertise level, y-axis: time to write, style: task_id
    def figure_expertise(self, userstudy_dir: str = f"{Macros.results_dir}/userstudy"):
        records = []
        for userstudy_file in os.listdir(userstudy_dir):
            if userstudy_file.endswith(".json"):
                records.append(su.io.load(f"{userstudy_dir}/{userstudy_file}"))

        random.seed(42)

        sns.set_theme(color_codes=True)
        df = pd.DataFrame(
            columns=[
                "task id",
                "user id",
                "understanding time",
                "writing time",
                "time per test",
                "python expertise",
                "years of programming",
            ],
            index=[
                str(i) + "-" + str(j)
                for i in range(1, len(records) + 1)
                for j in range(1, 5)
            ],
        )
        for index, record in enumerate(records):
            # user_attibute_to_value = collections.defaultdict(list)
            for task_id in range(1, 5):
                # user_attibute_to_value[f"understanding_time"].append(record[f"task_{task_id}_understanding_time"])
                # user_attibute_to_value[f"writing_time"].append(record[f"task_{task_id}_writing_time"])
                # user_attibute_to_value[f"time_per_test"].append(record[f"task_{task_id}_time_per_test"])

                df.loc[str(index + 1) + "-" + str(task_id)] = pd.Series(
                    {
                        "task id": str(task_id),
                        "user id": str(index + 1),
                        "understanding time": record[
                            f"task_{task_id}_understanding_time"
                        ],
                        "writing time": record[f"task_{task_id}_writing_time"],
                        "time per test": record[f"task_{task_id}_time_per_test"],
                        "python expertise": record["python_expertise"],
                        "years of programming": record["years_of_programming"],
                    }
                )

            # df.loc[str(index+1) + "-" + str(task_id)] = pd.Series({
            #     "task id": str(task_id), \
            #     "user id": str(index + 1), \
            #     "understanding time": mean(user_attibute_to_value["understanding_time"]), \
            #     "writing time": mean(user_attibute_to_value["writing_time"]), \
            #     "time per test": mean(user_attibute_to_value[f"time_per_test"]), \
            #     "python expertise": record["python_expertise"], \
            #     "years of programming": record["years_of_programming"],
            #     })
        print(df)
        # scatterplot
        gfg = sns.stripplot(
            x="python expertise", y="time per test", hue="user id", data=df, alpha=0.05
        )
        gfg.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(
            f"{Macros.figure_dir}/figure_expertise_to_writting_time_per_test.eps"
        )
        plt.clf()

        gfg = sns.stripplot(
            x="python expertise",
            y="understanding time",
            hue="user id",
            data=df,
            alpha=0.05,
        )
        gfg.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(f"{Macros.figure_dir}/figure_expertise_to_understanding_time.eps")
        plt.clf()

        gfg = sns.stripplot(
            x="years of programming",
            y="time per test",
            hue="user id",
            data=df,
            alpha=0.05,
        )
        gfg.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(
            f"{Macros.figure_dir}/figure_programming_year_to_writting_time_per_test.eps"
        )
        plt.clf()

        gfg = sns.stripplot(
            x="years of programming",
            y="understanding time",
            hue="user id",
            data=df,
            alpha=0.05,
        )
        gfg.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(
            f"{Macros.figure_dir}/figure_programming_year_to_understanding_time.eps"
        )
        plt.clf()

        gfg = sns.stripplot(
            x="python expertise", y="time per test", hue="task id", data=df, alpha=0.05
        )
        gfg.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(
            f"{Macros.figure_dir}/figure_task_expertise_to_writting_time_per_test.eps"
        )
        plt.clf()

        gfg = sns.stripplot(
            x="python expertise",
            y="understanding time",
            hue="task id",
            data=df,
            alpha=0.05,
        )
        gfg.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(
            f"{Macros.figure_dir}/figure_task_expertise_to_understanding_time.eps"
        )
        plt.clf()

        gfg = sns.stripplot(
            x="years of programming",
            y="understanding time",
            hue="task id",
            data=df,
            alpha=0.05,
        )
        gfg.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(
            f"{Macros.figure_dir}/figure_task_programming_year_to_understanding_time.eps"
        )

        plt.clf()
        gfg = sns.stripplot(
            x="years of programming",
            y="time per test",
            hue="task id",
            data=df,
            alpha=0.05,
        )
        gfg.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig(
            f"{Macros.figure_dir}/figure_task_programming_year_to_writing_time_per_test.eps"
        )

    def figure_exp_standalone(
        self,
        duplicatings: List[int] = [1, 10, 100, 1000],
        languages: List[str] = ["python", "java"],
        results_dir: su.arg.RPath = Macros.results_dir / "exp" / "standalone",
        out_dir: su.arg.RPath = Macros.figure_dir,
    ):
        records = []
        for language in languages:
            results_avg = su.io.load(results_dir / language / "results-avg.json")
            for record in results_avg:
                if record["duplicating"] not in duplicatings:
                    continue
                record["language"] = language
                record["timept"] = record["sum-time"] / record["sum-num"]
                records.append(record)
        df = pd.DataFrame.from_records(records)

        plt.clf()
        ax = sns.lineplot(x="duplicating", y="sum-time", data=df, hue="language")
        ax.set_xscale("log")
        ax.set_xlabel("duplication times")
        ax.set_ylabel("total time [s]")
        plt.tight_layout()
        plt.savefig(f"{out_dir}/figure_exp_standalone_time.eps")

        plt.clf()
        ax = sns.lineplot(x="duplicating", y="timept", data=df, hue="language")
        ax.set_xscale("log")
        ax.set_xlabel("duplication times")
        ax.set_ylabel("time per test [s]")
        plt.tight_layout()
        plt.savefig(f"{out_dir}/figure_exp_standalone_timept.eps")


if __name__ == "__main__":
    CLI(Figure, as_positional=False)
