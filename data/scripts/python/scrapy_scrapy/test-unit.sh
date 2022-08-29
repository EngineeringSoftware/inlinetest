#!/bin/bash
# test the project, with inline test plugin loaded but disabled
# this script is executed under the project directory root
# argument: 
# $1: path to conda.sh

conda_path=$1; shift
env_name=inline-testing

source ${conda_path}
conda activate $env_name

set -e
pytest tests/ -k "not test_commands and not test_crawler and not test_engine and not test_feedexport and not test_utils_display" --inlinetest-disable --deselect=tests/test_crawl.py::CrawlTestCase::test_start_requests_lazyness --deselect=tests/test_crawl.py::CrawlSpiderTest::test_process_request_instance_method
