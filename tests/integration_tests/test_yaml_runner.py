# -*- coding: utf-8 -*-
import fnmatch
import os

import pytest

from rss_scrapper.configuration import load_yaml_from_path
from rss_scrapper.task_factory import execute_configuration

TEST_FILES_FOLDER = "tests/integration_tests/yaml_test_files"
TEST_EXPECTS_KEY = "test_expects"

yaml_files = []
for root, dirnames, filenames in os.walk(TEST_FILES_FOLDER):
    for filename in fnmatch.filter(filenames, '*.yaml'):
        yaml_file = os.path.join(root, filename)
        yaml_files.append(yaml_file)


@pytest.fixture(params=yaml_files)
def yaml_file(request):
    return request.param


def test_configuration(yaml_file):
    conf = load_yaml_from_path(yaml_file)

    assert TEST_EXPECTS_KEY in conf, "yaml file should be a test file"

    res = execute_configuration(conf)

    for test_name, test_result in conf[TEST_EXPECTS_KEY].items():
        assert test_name in res, "expected a test named %s" % test_name

        assert test_result == res[test_name]
