# Inline tests

A new type of tests that check the correctness of code at statement level.

## Introduction

This repo contains the code and data for producing the experiments in
[Inline Tests][paper-url].  In this work, we proposed a new type of
tests, inline tests, which reside below unit tests in the hierarchy of
test types.  Inline tests can be used to test the code on the
statement level. We implemented I-Test framework for developers to
write inline tests in Java and Python. I-Test framework has been
integrated with popular testing frameworks pytest and Junit. 

The code includes:
* I-Test framework for Java
* scripts for collecting and filtering examples suitable for writing inline tests
* scripts for evaluating the performance of I-Test

The data includes:
* the 50 Python examples and 50 Java examples with our written inline tests
* results of performance evaluation (on our machine)
* the documents used in our user study
* anonymized results of our user study


**How to...**
* **install I-Test and the environment for replicating our study**: see detailed steps in [INSTALL.md](/INSTALL.md)
* **replicate our performance evaluation of I-Test**: see detailed steps in [REPLICATION.md](/REPLICATION.md)
* **replicate other parts of our paper, e.g., collecting examples and user study**: we already described the steps in the paper, and you may find the documents and intermediate files for those in this repository; see the remainder of this README for more details

## Examples

### Java
The string manipulation (Line 12) in this code snippet takes the original String `titleStr`, removes all newline characters, replaces any sequences of multiple spaces with a single space, and trims any leading or trailing whitespace. `titleStr` is updated to be a more uniform string with single spaces separating words and no extraneous whitespace at the beginning or end.
The inline test (Line 13) that we write for target statement (Line 12) consists of three parts:
- Declaration with itest() constructor
- Assigning inputs with given() function calls
- Specifying test oracles with check_*() function calls

```java
public class Example {
  protected void onAttachedToWindow() {
    VoIPService service = VoIPService.getSharedInstance();
    if (service != null && service.groupCall != null) {
      String titleStr;
      if (!TextUtils.isEmpty(service.groupCall.call.title)) {
        titleStr = service.groupCall.call.title;
      } else {
        titleStr = service.getChat().title;
      }
      if (titleStr != null) {
        titleStr = titleStr.replace("\n", " ").replaceAll(" +", " ").trim();
        itest().given(titleStr, "I am a Title\n\nAnd:  Subtitle\n").checkEq(titleStr, "I am a Title And: Subtitle");
      }
    }
  } 
}
```

To run the inline test, we need to install I-Test framework, which requires Java 8 and Maven. The script of installing Java 8, Maven and I-Test is [here](/java/install.sh). Execute `./install.sh` to install them.

If you already have Java 8 and Maven installed, you can install I-Test framework with the following command:
```bash
cd java
mvn install
```

After installing I-Test framework, we can run the inline test by running the following command from the root directory of this repository:
```bash
proj_path=${PWD}
cd ${PWD}/data/examples/readme
bash ${proj_path}/data/examples/java/run-only.sh $path_to_ITest_jar $path_to_example_file
```
In this example, the path to I-Test jar is
`${proj_path}/java/target/inlinetest-1.0.jar` and the path to example
file is `Example` (without extension of .java).

### Python

The tool for python is available as a plugin [pytest-inline](https://github.com/pytest-dev/pytest-inline) for pytest. Refer to the [README](https://github.com/pytest-dev/pytest-inline/blob/main/README.md) for installation and usage.

## Repo structure

- [java](/java): code of I-Test framework for Java
- [research](/research): scripts for our experiments
- data
  - [examples](/data/examples): 50 Python and 50 Java examples with our written inline tests
  - [exp](/data/exp): the configurations for running performance evaluation experiments
  - [patches](/data/patches): the patches used in performance evaluation experiments, to integrated inline tests into open-source projects
  - [projects](/data/projects) and [projects-used](/data/projects-used): the list of top-100 starred open-source GitHub projects that we used to search for statements under test
  - [scripts](/data/scripts): the scripts used in performance evaluation experiments, for preparing environment and executing the unit tests or inline tests in open-source projects
- [results](/results): directory for storing the results of running performance evaluation experiments; used in the [replication guide](/REPLICATION.md)
- [results-ours](/results-ours): the results of performance evaluation on our machine
- userstudy
  - [content](/userstudy/content): the package we send to each participant in our user study
  - [response](/userstudy/response): anonymized responses collected of our user study
- [appendix.pdf](/appendix.pdf): an appendix that describes:
  - A: the detailed procedure of searching for statements under test in open-source projects
  - B: API of I-Test framework
  - C: analysis of user study responses

[paper-url]: https://dl.acm.org/doi/abs/10.1145/3551349.3556952


## Including more examples to our experiments

If you want to add additional subjects to our standalone/integrated
experiments, please follow these steps:

### To include standalone examples

1. Add standalone code with inline tests to the `/data/examples/$lang`
   directory (with `$lang$` being `python` or `java`).

2. Append the name of the added file to `/data/exp/standalone/$lang.yaml`.

That's it. The next time you run the standalone experiments, these new
examples should be included.


### To include integrated examples 

Adding integrated examples is a bit harder, as you need to first
properly configure the environment (figuring out the build script,
installing required dependencies using conda/sdkman) for running the
unit tests in the subject project.  You also need to figure out how to
install inlinetest (for Python/Java) into that environment.  Once you
figure out these, include the example by:

1. Add the metadata of the subject project (must include full_name,
   url, revision, and default_branch) into
   `/data/projects-used/$lang.yaml`.

2. Create a directory with the full_name of the subject project under
   `/data/scripts/$lang/`. Now under that directory, you need to
   prepare up to 6 Bash scripts (please check the scripts for other
   projects under that directory for examples):

  - prepare-env-vanilla.sh: for configuring the environment for
    running vanilla unit tests.

  - prepare-env-inline.sh: for configuring the environment for running
    unit tests + inline tests.

  - build.sh (optional): for building the subject project, which is a
    script shared by both vanilla environment and unit+inline
    environment.

  - test-vanilla.sh: for running vanilla unit tests.

  - test-unit.sh: for running unit tests under the unit+inline
    environment (when inline tests are added).

  - test-inline.sh: for running inline tests under the unit+inline
    environment (when inline tests are added).

3. Add a patch (in unidiff format, usually obtained by `diff -u` or
   `git diff`) for the inline test you want to add to the subject
   project to `/data/patches/$lang/examples/`.

4. If installing inlinetest into the subject project requires
   modifying some build script (e.g., `pom.xml`), you need to add a
   patch for doing that to `/data/patches/$lang/projects/`, named
   `$full_name.patch`.

5. Append the project name and the name(s) of the inline test
   patch(es) to `/data/exp/integrated/$lang.yaml`.

That's it for adding integrated examples. You may want to run the
integrated examples script with `--only=[$full_name]` option to only
run the new project you added.  If any script failed, you can check
the logs by doing `python -m research.exp_integrated view_result
--results_file=../results/exp/integrated/$lang/4-1/$full_name.json`
(modify the results file path accordingly), and fix the
scripts/patches as needed.

## Citation
If you have used I-Test in a research project, please cite the research paper in any related publication:

Title: [Inline Tests](https://dl.acm.org/doi/abs/10.1145/3551349.3556952)

Authors: [Yu Liu](https://sweetstreet.github.io/), [Pengyu Nie](https://pengyunie.github.io/), [Owolabi Legunsen](https://mir.cs.illinois.edu/legunsen/), [Milos Gligoric](http://users.ece.utexas.edu/~gligoric/)

```bibtex
@inproceedings{LiuASE22InlineTests,
  title =        {Inline Tests},
  author =       {Yu Liu and Pengyu Nie and Owolabi Legunsen and Milos Gligoric},
  pages =        {1--13},
  booktitle =    {International Conference on Automated Software Engineering},
  year =         {2022},
}
```

Title: [pytest-inline][paper-url]

Authors: [Yu Liu](https://sweetstreet.github.io/), [Zachary Thurston](), [Alan Han](), [Pengyu Nie](https://pengyunie.github.io/), [Milos Gligoric](http://users.ece.utexas.edu/~gligoric/), [Owolabi Legunsen](https://mir.cs.illinois.edu/legunsen/)

```bibtex
@inproceedings{LiuICSE23PytestInline,
  title =        {pytest-inline: An Inline Testing Tool for Python},
  author =       {Yu Liu and Zachary Thurston and Alan Han and Pengyu Nie and Milos Gligoric and Owolabi Legunsen},
  pages =        {1--4},
  booktitle =    {International Conference on Software Engineering, DEMO},
  year =         {2023},
}
```
