# Replication Guide

This document is a guide to replicate the experiments for evaluating
the performance of I-Test, in both standalone mode (running inline
tests in files extracted from the original projects) and integrated
mode (running inline tests integrated into some open-source projects,
as well as their unit tests).

First, make sure that you have followed the [installation
guide](/INSTALL.md) to set up the experiments environment.

The steps below will guide you to run the experiments, process the
results, and generate Table 3, Figure 12, and Table 4 in our paper.
The experiments setup is described in Section 4.1 of our paper (which
we assume that you have already read).  The data and steps for the
other tables and figures are either described in the paper or in
[README](/README.md).

Unless otherwise mentioned, for all the commands below, please:
1. change directory to "research". Assuming you were at the root of this repository: `cd research`
2. make sure to be using the inline-research environment: `conda activate inline-research`


## Standalone Experiments

### Python

Run inline tests without duplicating them; 4 reruns.
```
python -m research.exp_standalone run --language=python --requests_file=../data/exp/standalone/python.yaml --run_dir=../data/examples/python --rerun=4 --duplicating=1 --out_dir=../results/exp/standalone/python/4-1
```

Run inline tests with duplicating 10 times; 4 reruns.
```
python -m research.exp_standalone run --language=python --requests_file=../data/exp/standalone/python.yaml --run_dir=../data/examples/python --rerun=4 --duplicating=10 --out_dir=../results/exp/standalone/python/4-10
```

Run inline tests with duplicating 100 times; 4 reruns.
```
python -m research.exp_standalone run --language=python --requests_file=../data/exp/standalone/python.yaml --run_dir=../data/examples/python --rerun=4 --duplicating=100 --out_dir=../results/exp/standalone/python/4-100
```

Run inline tests with duplicating 1000 times; 4 reruns.
```
python -m research.exp_standalone run --language=python --requests_file=../data/exp/standalone/python.yaml --run_dir=../data/examples/python --rerun=4 --duplicating=1000 --out_dir=../results/exp/standalone/python/4-1000
```

Process the results and generate summary data files.
```
python -m research.exp_standalone process_results --language=python --requests_file=../data/exp/standalone/python.yaml --out_dir=../results/exp/standalone/python --results_dirs='[../results/exp/standalone/python/4-1, ../results/exp/standalone/python/4-10, ../results/exp/standalone/python/4-100, ../results/exp/standalone/python/4-1000]'
```

The generated data files are
`../results/exp/standalone/python/results.json` and
`../results/exp/standalone/python/results-avg.json`. You can compare
with our version at
`../results-ours/exp/standalone/python/results.json` and
`../results-ours/exp/standalone/python/results-avg.json`.


### Java

Run inline tests without duplicating them; 4 reruns.
```
python -m research.exp_standalone run --language=java --requests_file=../data/exp/standalone/java.yaml --run_dir=../data/examples/java --rerun=4 --duplicating=1 --out_dir=../results/exp/standalone/java/4-1
```

Run inline tests with duplicating 10 times; 4 reruns.
```
python -m research.exp_standalone run --language=java --requests_file=../data/exp/standalone/java.yaml --run_dir=../data/examples/java --rerun=4 --duplicating=10 --out_dir=../results/exp/standalone/java/4-10
```

Run inline tests with duplicating 100 times; 4 reruns.
```
python -m research.exp_standalone run --language=java --requests_file=../data/exp/standalone/java.yaml --run_dir=../data/examples/java --rerun=4 --duplicating=100 --out_dir=../results/exp/standalone/java/4-100
```

Run inline tests with duplicating 1000 times; 4 reruns.
```
python -m research.exp_standalone run --language=java --requests_file=../data/exp/standalone/java.yaml --run_dir=../data/examples/java --rerun=4 --duplicating=1000 --out_dir=../results/exp/standalone/java/4-1000
```

Process the results and generate summary data files.
```
python -m research.exp_standalone process_results --language=java --requests_file=../data/exp/standalone/java.yaml --out_dir=../results/exp/standalone/java --results_dirs='[../results/exp/standalone/java/4-1, ../results/exp/standalone/java/4-10, ../results/exp/standalone/java/4-100, ../results/exp/standalone/java/4-1000]'
```

The generated summary data files are
`../results/exp/standalone/java/results.json` and
`../results/exp/standalone/java/results-avg.json`. You can compare
with our version at
`../results-ours/exp/standalone/java/results.json` and
`../results-ours/exp/standalone/java/results-avg.json`.


## Integrated Experiments

For integrated experiments, the scripts automatically download the
used open-source projects to "_downloads".

### Python

Run unit tests and inline tests without duplicating them; 4 reruns.
```
python -m research.exp_integrated run --language=python --requests_file=../data/exp/integrated/python.yaml --rerun=4 --duplicating=1 --out_dir=../results/exp/integrated/python/4-1
```

Run unit tests and inline tests with duplicating 10 times; 4 reruns.
```
python -m research.exp_integrated run --language=python --requests_file=../data/exp/integrated/python.yaml --rerun=4 --duplicating=10 --out_dir=../results/exp/integrated/python/4-10
```

Run unit tests and inline tests with duplicating 100 times; 4 reruns.
```
python -m research.exp_integrated run --language=python --requests_file=../data/exp/integrated/python.yaml --rerun=4 --duplicating=100 --out_dir=../results/exp/integrated/python/4-100
```

Run unit tests and inline tests with duplicating 1000 times; 4 reruns.
```
python -m research.exp_integrated run --language=python --requests_file=../data/exp/integrated/python.yaml --rerun=4 --duplicating=1000 --out_dir=../results/exp/integrated/python/4-1000
```

Process the results and generate summary data files.
```
python -m research.exp_integrated process_results --language=python --requests_file=../data/exp/integrated/python.yaml --out_dir=../results/exp/integrated/python --results_dirs='[../results/exp/integrated/python/4-1, ../results/exp/integrated/python/4-10, ../results/exp/integrated/python/4-100, ../results/exp/integrated/python/4-1000]'
```

The generated summary data files are
`../results/exp/integrated/python/results.json` and
`../results/exp/integrated/python/results-avg.json`. You can compare
with our version at
`../results-ours/exp/integrated/python/results.json` and
`../results-ours/exp/integrated/python/results-avg.json`.


### Java

Run unit tests and inline tests without duplicating them; 4 reruns.
```
python -m research.exp_integrated run --language=java --requests_file=../data/exp/integrated/java.yaml --rerun=4 --duplicating=1 --out_dir=../results/exp/integrated/java/4-1
```

Run unit tests and inline tests with duplicating 10 times; 4 reruns.
```
python -m research.exp_integrated run --language=java --requests_file=../data/exp/integrated/java.yaml --rerun=4 --duplicating=10 --out_dir=../results/exp/integrated/java/4-10
```

Run unit tests and inline tests with duplicating 100 times; 4 reruns.
```
python -m research.exp_integrated run --language=java --requests_file=../data/exp/integrated/java.yaml --rerun=4 --duplicating=100 --out_dir=../results/exp/integrated/java/4-100
```

Run unit tests and inline tests with duplicating 1000 times; 4 reruns.
```
python -m research.exp_integrated run --language=java --requests_file=../data/exp/integrated/java.yaml --rerun=4 --duplicating=1000 --out_dir=../results/exp/integrated/java/4-1000
```
It is expected that some tests in `alibaba_fastjson` and `apache_kafka` would fail when duplicating 1000 times because of code too large.

Process the results and generate summary data files.
```
python -m research.exp_integrated process_results --language=java --requests_file=../data/exp/integrated/java.yaml --out_dir=../results/exp/integrated/java --results_dirs='[../results/exp/integrated/java/4-1, ../results/exp/integrated/java/4-10, ../results/exp/integrated/java/4-100, ../results/exp/integrated/java/4-1000]'
```

The generated summary data files are
`../results/exp/integrated/java/results.json` and
`../results/exp/integrated/java/results-avg.json`. You can compare
with our version at
`../results-ours/exp/integrated/java/results.json` and
`../results-ours/exp/integrated/java/results-avg.json`.


# FAQ

Q: What can I do if I get a timeout error like this?
```
cmd: /home/itdocker/inlinetest/data/scripts/java/skylot_jadx/build.sh default
success: False; time: 999.3513159751892
TIMEOUT!!!
```

A: We set 1000 seconds as timeout for running unit tests by default. If your machine is slow (for example, when using docker), default timeout might not be enough. Both research.exp_standalone and research.exp_standalone provide a keyword argument `timeout` which accepts a number in seconds.
For example, this command runs java integrated tests with 10000 seconds as timeout.
```
python -m research.exp_integrated run --language=java --requests_file=../data/exp/integrated/java.yaml --rerun=1 --duplicating=1 --out_dir=../results/exp/integrated/java/1-1 --timeout=10000
```

Q: How can I run a subset of projects?

Both research.exp_standalone and research.exp_standalone provide a keyword argument `out` which accepts a list of projects.
For example, this command runs python integrated tests on project "bokeh/bokeh" and "davidsandberg/facenet"

```
python -m research.exp_integrated run --language=python --requests_file=../data/exp/integrated/python.yaml --rerun=1 --duplicating=1 --out_dir=../results/exp/integrated/python/1-1 --only="[bokeh_bokeh,davidsandberg_facenet]"
```