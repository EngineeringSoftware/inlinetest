from os.path import expanduser
import os
from pathlib import Path


class Macros:
    this_dir: Path = Path(os.path.dirname(os.path.realpath(__file__)))
    home_dir: Path = Path(expanduser("~"))
    project_dir: Path = this_dir.parent.parent
    log_file = project_dir / "experiments.log"
    python_dir: Path = project_dir / "python"
    table_dir: Path = project_dir / "papers" / "paper" / "tables"
    figure_dir: Path = project_dir / "papers" / "paper" / "figures"
    results_dir: Path = project_dir / "results"
    downloads_dir: Path = project_dir / "_downloads"
    data_dir: Path = project_dir / "data"
    api_dir: Path = project_dir / "api"

    tutorial_projects: list = [
        # java
        "iluwatar/java-design-patterns",
        "doocs/advanced-java",
        "macrozheng/mall",
        "GrowingGit/GitHub-Chinese-Top-Charts",
        "geekxh/hello-algorithm",
        "shuzheng/zheng",
        "JeffLi1993/springboot-learning-example",
        "YunaiV/SpringBoot-Labs",
        "williamfiset/Algorithms",
        "heibaiying/BigData-Notes",
        "mission-peace/interview",
        "lihengming/spring-boot-api-project-seed",
        "janishar/mit-deep-learning-book-pdf",
        "careercup/CtCI-6th-Edition",
        "macrozheng/mall-learning",
        "Snailclimb/JavaGuide",
        "0voice/interview_internal_reference",
        "kdn251/interviews",
        "TheAlgorithms/Java",
        "MisterBooo/LeetCodeAnimation",
        "ityouknow/spring-boot-examples",
        "hollischuang/toBeTopJavaer",
        "zhisheng17/flink-learning",
        "doocs/leetcode",
        "forezp/SpringCloudLearning",
        "dyc87112/SpringBoot-Learning",
        "winterbe/java8-tutorial",
        "DuGuQiuBai/Java",
        "xkcoding/spring-boot-demo",
        "lenve/vhr",
        # python
        "public-apis/public-apis",
        "donnemartin/system-design-primer",
        "jackfrued/Python-100-Days",
        "vinta/awesome-python",
        "521xueweihan/HelloGitHub",
        "fighting41love/funNLP",
        "TheAlgorithms/Python",
        "wangzheng0822/algo",
        "keon/algorithms",
        "eugenp/tutorials",
        "miloyip/game-programmer",
        "gto76/python-cheatsheet",
        "floodsung/Deep-Learning-Papers-Reading-Roadmap",
        "bregman-arie/devops-exercises",
        "charlax/professional-programming",
        "qiurunze123/miaosha",
        "shimohq/chinese-programmer-wrong-pronunciation",
        "yunjey/pytorch-tutorial",
        "josephmisiti/awesome-machine-learning",
    ]
