# Installation Guide

I-Test currently supports two programming languages, Python and Java.

We provide two options:
1. install with [docker][sec-docker]
2. install to [local environment][sec-local]. 

## Docker
[sec-docker]: #docker
Install [docker][docker-webpage]
```
docker pull ...
```

### System Requirements

The minimum requirements for replicating our experiments are:
- at least 20GB of free disk space

For your reference, we used the machine with the following specs to
run experiments:
- Intel Core i7-11700K @ 3.60GHz (8 cores, 16 threads) CPU
- 64 GB RAM
- Ubuntu 20.04 operating system

## Local
[sec-local]: #local

We utilize the package management systems
([conda][conda-webpage] for Python and [sdkman][sdkman-webpage] for
Java) to install the necessary dependencies for I-Test itself, for our
experiment scripts, and for running the unit tests of other
open-source projects in our integrated experiments.

This document will guide you through the following steps (with some
usage examples to verify if the installation is successful):
- install the package management systems
- install the I-Test framework
- install the environment for running our experiment scripts


### System Requirements

The minimum requirements for replicating our experiments are:
- a Linux operating system (MacOS not guaranteed to work)
- at least 10GB of free disk space

Note that I-Test framework itself is not limited to Linux; we have
tested the I-Test framework on a MacOS machine (with MacOS 10.15.7).
However, a part of our experiment scripts uses Bash and relies on
Linux-specific grammars.

For your reference, we used the machine with the following specs to
run experiments:
- Intel Core i7-11700K @ 3.60GHz (8 cores, 16 threads) CPU
- 64 GB RAM
- Ubuntu 20.04 operating system


### Installing Package Management Systems

The two package management systems we use, [conda][conda-webpage] and
[sdkman][sdkman-webpage], can both be installed in user mode (i.e.,
does not require sudo).  To install each of them, you will need to
execute some commands AND configure your `.bashrc` appropriately, and
then restart the terminal for the changes to take effect.  If you
happend to have existing installations of (a recent version of) either
package management system, you do not need to install it again.

#### conda for Python

1. Download the Miniconda installation script from
   [here](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links);
   pick the correct link according to your CPU architecture (usually
   "Miniconda3 Linux 64-bit", but for ARM should be "Miniconda3
   Linux-aarch64 64-bit").
   For example:
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

(Installing Anaconda is also fine, which is bundled with some
libraries that we don't need.)

2. Execute the downloaded script, and follow the prompts on the
   terminal to install conda at the desired location. For example:

```
bash Miniconda3-latest-Linux-x86_64.sh
```

3. If not already done at the end of the last step, run `conda init` which automatically changes your `.bashrc` file to use conda.

4. Restart your terminal. By executing `conda --version`, you should be able to see the version of conda you just installed.


#### sdkman for Java

1. Execute the following command, and follow the prompts on the
   terminal to install sdkman.

```
curl -s "https://get.sdkman.io" | bash
```

2. Restart your terminal. By executing `sdk version`, you should be able to see the version of sdkman you just installed.


### Installing the I-Test Framework

#### Python 3.7+

1. Change directory to "python". Assuming you were at the root of this
   repository: `cd python`

2. Execute `./prepare-conda-env.sh`

3. Execute `conda activate inline-dev`

4. You should be able to see "(inline-dev) " as the prefix of the
   prompt in your terminal. Then, to further check if installation is
   successful, you can run the tests for the I-Test framework in
   Python: `pytest`

* Trouble shooting: if you get error "CondaEnvironmentError: cannot
  remove current environment. deactivate and run conda remove again",
  please run `conda deactivate` to exit the inline-dev environment,
  then try again.

#### Java 8

1. Change directory to "java". Assuming you were at the root of this
   repository: `cd java`

2. Execute `./install.sh`

3. During the installation in the previous step, we actually already
   run the tests for the I-Test framework in Java.  You can also run
   these tests again to double-check if the installation is
   successful: `sdk use java 8.0.302-open; sdk use maven 3.8.3; mvn test`


### Installing the Environment for Experiment Scripts

1. Change directory to "research". Assuming you were at the root of
   this repository: `cd research`

2. Execute `./prepare-conda-env.sh`

3. Execute `conda activate inline-research`

4. You should be able to see "(inline-dev) " as the prefix of the
   prompt in your terminal. Then, to further check if installation is
   successful, you can run the script for running the inline tests in
   the 50 Python example files and 50 Java example files:

```
python -m research.exp_standalone run --language=python --requests_file=../data/exp/standalone/python.yaml --run_dir=../data/examples/python --out_dir=/tmp/inlinetest-smoke/python --force=True
python -m research.exp_standalone run --language=java --requests_file=../data/exp/standalone/java.yaml --run_dir=../data/examples/java --out_dir=/tmp/inlinetest-smoke/java --force=True
```

For both of the previous commands, you should see a progress bar that ends at "running: 100% ... 50/50 ...", without warning or error messages.


* Trouble shooting: if you get error "CondaEnvironmentError: cannot
  remove current environment. deactivate and run conda remove again",
  please run `conda deactivate` to exit the inline-dev environment,
  then try again.

### TeX Live
Install the latest version.
#### Linux
[TeX Live](https://tug.org/texlive/quickinstall.html)
#### Mac
[MacTeX](https://tug.org/mactex/)
#### Windows
[TeX Live on Windows](https://tug.org/texlive/windows.html#install)

[docker-webpage]: https://docs.docker.com/engine/install/
[conda-webpage]: https://docs.conda.io/en/latest/
[sdkman-webpage]: https://sdkman.io/