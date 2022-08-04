Developers often want to test one line of code, e.g., to check if a
regular expression is correct. However, if the target line of code is
within a function, unit tests are too coarse-grained to directly
support testing at statement-level of granularity.

We developed a framework for writing inline tests, which enables testing any
single statement within a function.  Our goal is to make it easier for
developers to specify the expected behavior of a single statement, and to run
inline tests in much the same way as they run unit tests.

In this user study, you will use our framework:

  * You will be presented with a short tutorial (takes at most 20 minutes to read)
  * You will be given 4 tasks. In each task, you will be asked to write one or more inline tests
    (each task takes at most 10 minutes to complete)
  * There is a short questionnaire at the end of this file

The entire user study should take no more than 1 hour.


# Tutorial

In this tutorial, we show you how to use our framework to write an
inline test in Python.

An inline test must be written immediately after the statement to be tested.

There are three kinds of API calls:
- initializing an inline test: `Here()`
- providing input: `given(variable, value)`
- making assertions: `check_eq(actual_value, expected_value)`, `check_true(expr)`, `check_false(expr)`

You can run inline tests using this command: `pytest file_name.py`.


## Setting up

To install the Python runtime environment for this user study, please
run: `source prepare-conda-env.sh`. If you see `(inline)` at the
beginning of your terminal prompt, you are good to go.


## Examples

1. See the file tutorial_example_1.py

The goal is to test the following statement, which tokenizes
strings in a provided list of strings:
```
res = list(map(str.split, input_list))
```
We added an inline test to check if the above statement works as
expected.

```
res = list(map(str.split, input_list))
Here().given(input_list, ['Hello World!', 'Have a good day']).check_eq(res, [['Hello', 'World!'], ['Have', 'a', 'good', 'day']])
```
`Here()` uses our API to initialize an inline test.

`given(input_list, ['Hello World!', 'Have a good day'])` is used to
assign `['Hello World!', 'Have a good day']` to the `input_list`
parameter.

`check_eq(res, [['Hello', 'World!'], ['Have', 'a', 'good', 'day']])`
is used to assert that the valued assigned to `res` is equal to the
expected one: `[['Hello', 'World!'], ['Have', 'a', 'good', 'day']]`

To run this test, use `pytest tutorial_example_1.py`. The test outcome
should be "1 passed".

2. See the file tutorial_example_2.py

The goal is to test the statement on line 18, which uses a regular
expression to match nodejs versions.

We wrote 2 inline tests for this statement:
- check if `v8.9.4` is correctly matched with groups `8`, `9`, `4`
- check if `v.8.9.4abc` is correctly matched with groups `8`, `9`, `4`

```
def _detect_nodejs() -> str:
    ...
    match = re.match(r"^v(\d+)\.(\d+)\.(\d+).*$", stdout.decode("utf-8"))

    # First inline test
    Here()
    .given(stdout, "v8.9.4".encode("utf-8"))
    .check_true(match)
    .check_eq(match.groups(), ("8", "9", "4"))

    # Second inline test
    Here()
    .given(stdout, "v8.9.4abc".encode("utf-8"))
    .check_true(match)
    .check_eq(match.groups(), ("8", "9", "4"))
    ...        
```
- Note 1: One can write multiple inline tests for one statement.
- Note 2: One can use multiple assertions in one inline test.
- Note 3: `check_eq/check_true/check_false` method calls must appear
  after `given` method calls.
- Note 4: One can only provide inputs for variables (`stdout` in this
  example); one *cannot* provide inputs for expressions (e.g.,
  `given(stdout.decode("utf-8"), ...)` is invalid).


To run these inline tests, use `pytest tutorial_example_2.py`. The test outcome
should be "2 passed".

3. See the file tutorial_example_3.py

The goal is to test the statements on line 29 and on line 44, which
find strings in the list `refs` that start with `"tag: "`, and extract
the suffix.

```
def git_versions_from_keywords(keywords, tag_prefix, verbose):
    """Get version information from git keywords."""
    ...
    # starting in git-1.8.3, tags are listed as "tag: foo-1.0" instead of
    # just "foo-1.0". If we see a "tag: " prefix, prefer those.
    TAG = "tag: "
    tags = set([r[len(TAG) :] for r in refs if r.startswith(TAG)])

    # First inline test
    Here().given(refs, ["tag: foo-1.0", "tag: bar-3.2"])
    .given(TAG, "tag: ")
    .check_eq(tag, {"bar-3.2", "foo-1.0"})

    # Second inline test
    Here().given(refs, ["foo-1.0", "bar-3.2"])
    .given(TAG, "tag: ")
    .check_eq(tag, set())

    if not tags:
        # Either we're using git < 1.8.3, or there really are no tags. We use
        # a heuristic: assume all version tags have a digit. The old git %d
        # expansion behaves like git log --decorate=short and strips out the
        # refs/heads/ and refs/tags/ prefixes that would let us distinguish
        # between branches and tags. By ignoring refnames without digits, we
        # filter out many common branch names like "release" and
        # "stabilization", as well as "HEAD" and "master".
        tags = set([r for r in refs if re.search(r"\d", r)])

        # Third inline test
        Here().given(
            refs, ["foo-1.0", "bar-3.2", "release", "stabilization", "master"]
        ).check_eq(tags, {"foo-1.0", "bar-3.2"})
```
- Note 1: You need to initialize every variable used in the tested
  statement even if it is defined before the tested statement, e.g.,
  variable `TAG` needs to be initialized again with `given()`, even if
  it was previously initialized to `"tag: "`.

To run these inline tests, use `pytest tutorial_example_3.py`. The test outcome
should be, "3 passed".


# Tasks

There are 4 tasks. You may choose inputs and expected outputs as
needed, but we request that you use `pytest task_X.py` to ensure that
your tests pass (where `X` is the ID of the task). Record the time
that you spend on each task (divided into time for understanding the
tested statement and total time for writing all your tests), and fill
them in the provided spaces.

- Note 1: We provide some code context for the statement(s) being
  tested to help you understand the statement(s), but you should not
  need to fully understand the code beyond the statement that is being
  tested.
- Note 2: Time for setting up Python runtime environment should not
  be included in the times that you report.
- Note 3: An inline test can only check one statement, not a group of (consecutive) statements.
- Note 4: Providing test inputs should be done by using the "given()"
  function (as shown in the tutorial examples), instead of using
  assignment statements.
- Note 5: Please limit the time for each task to 10min; if you could
  not solve the task in time limit, please feel free to skip the task
  and put "not finished" below.

(1) Goal: write (at least one) inline tests for a statement containing a regular expression.
- File: task_1.py
- Line to be tested: 12
- Time spent in understanding the statement (in minutes) > 
- Total time spent in writing all inline tests (in minutes) > 

(2) Goal: write (at least one) inline tests for a statement that performs string manipulation.
- File: task_2.py
- Line to be tested: 31
- Time spent in understanding the statement (in minutes) > 
- Total time spent in writing all inline tests (in minutes) > 

(3) Write (at least one) inline tests for a statement that manipulates collections.
- File: task_3.py
- Line to be tested: 17
- Time spent in understanding the statement (in minutes) > 
- Total time spent in writing all inline tests (in minutes) > 

(4) Write (at least one) inline tests for a statement that performs bit manipulation.
- File: task_4.py
- Line to be tested: 28
- Time spent in understanding the statement (in minutes) > 
- Total time spent in writing all inline tests (in minutes) > 


# Questionnaire

(1) How do you rank the difficulty of learning how to use our framework?
    Please use a score in the range 1~5:
    1 - very difficult; 2 - difficult; 3 - moderate; 4 - easy; 5 - very easy.
> 

(2) How do you rank the difficulty of writing inline tests?
    Please use a score in the range 1~5:
    1 - very difficult; 2 - difficult; 3 - moderate; 4 - easy; 5 - very easy.
> 

(3) How many total years of programming experience (in industry,
    research, etc.) do you have?
> 

(4) How do you rank your Python programming expertise?
    Please use a score in the range 1~5:
    1 - novice; 2 - beginner; 3 - intermediate; 4 - advanced; 5 - expert.
> 

(5) For each task above, do you think that writing inline tests is
    beneficial, compared with just writing unit tests? Note that
    inline tests are complement but not a replacement for unit tests. 
    Please answer `yes` or `no`. You can optionally include a rationale.

task 1 > 
rationale (optional) > 

task 2 > 
rationale (optional) > 

task 3 > 
rationale (optional) > 

task 4 > 
rationale (optional) > 

(6) If you have any comments on how the framework can be improved,
features that you would to see in an inline testing framework, or any
other general comment about the idea of testing individual statements,
write those comments below. We appreciate your feedback.
> 


# Response Form

After you finish all the tasks, please compress the folder using
`./package.sh` to get `userstudy.zip`, and send it via email to 
Yuki Liu <yuki.liu@utexas.edu>
