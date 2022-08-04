#!/bin/bash
# prepares a vanilla conda environment for the project (usually called "inline-testing")
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh

conda_path=$1; shift
env_name=inline-testing

set -e
source ${conda_path}
conda env remove --name $env_name
conda create --name $env_name python=3.8 pip -y
pip install --upgrade pip
conda activate $env_name
# frozen list of dependencies, to avoid long version solving time
echo "numpy==1.21.6
python-dateutil==2.8.2
pytz==2022.1
asv==0.4.2
cython==0.29.28
black==21.5b2
cpplint==1.6.0
flake8==4.0.1
flake8-bugbear==21.3.2
flake8-comprehensions==3.7.0
isort==5.10.1
mypy==0.941
pre-commit==2.18.1
pycodestyle==2.8.0
pyupgrade==2.32.0
gitpython==3.1.27
gitdb==4.0.9
numpydoc==1.3.1
pandas-dev-flaker==0.4.0
pydata-sphinx-theme==0.8.1
pytest-cython==0.2.0
sphinx==4.5.0
sphinx-panels==0.6.0
types-python-dateutil==2.8.14
types-PyMySQL==1.0.19
types-pytz==2021.3.7
types-setuptools==57.4.14
nbconvert==6.5.0
nbsphinx==0.8.8
pandoc==2.2
dask==2022.5.0
toolz==0.11.2
partd==1.2.0
cloudpickle==2.0.0
markdown==3.3.6
feedparser==6.0.8
pyyaml==6.0
requests==2.27.1
boto3==1.17.106
botocore==1.20.106
hypothesis==6.46.2
moto==3.1.7
flask==2.1.2
pytest==7.1.2
pytest-cov==3.0.0
pytest-xdist==2.5.0
pytest-asyncio==0.18.3
pytest-instafail==0.4.2
seaborn==0.11.2
statsmodels==0.13.2
ipywidgets==7.7.0
nbformat==5.4.0
notebook==6.4.11
blosc==1.10.6
bottleneck==1.3.4
ipykernel==6.13.0
ipython==8.3.0
jinja2==3.1.2
matplotlib==3.5.2
numexpr==2.8.1
scipy==1.8.0
numba==0.55.1
beautifulsoup4==4.11.1
html5lib==1.1
lxml==4.8.0
openpyxl==3.0.9
xlrd==2.0.1
xlsxwriter==3.0.3
xlwt==1.3.0
odfpy==1.4.1
fastparquet==0.8.1
pyarrow==7.0.0
python-snappy==0.6.1
tables==3.7.0
s3fs==2021.11.0
aiobotocore==1.4.2
fsspec==2021.11.0
gcsfs==2021.11.0
sqlalchemy==1.4.36
xarray==0.18.2
cftime==1.6.0
pyreadstat==1.1.5
tabulate==0.8.9
natsort==8.1.0
setuptools==61.2.0" > requirements-dev.txt
pip install -r requirements-dev.txt
python setup.py build_ext -j 4
pip install -e . --no-build-isolation --no-use-pep517
