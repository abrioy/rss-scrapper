# -*- coding: utf-8 -*-
import fnmatch
import os

import pytest

from rss_scrapper.configuration import get_from_path
from rss_scrapper.task_factory import execute_configuration

TEST_FILES_FOLDER = "tests/integration_tests/yaml_test_files"
TEST_EXPECTS_KEY = "test_expects"
FEEDS_KEY = "feeds"

yaml_files = []
for root, dirnames, filenames in os.walk(TEST_FILES_FOLDER):
    for filename in fnmatch.filter(filenames, '*.yaml'):
        yaml_file = os.path.join(root, filename)
        yaml_files.append(yaml_file)


@pytest.fixture(params=yaml_files)
def yaml_file(request):
    return request.param


def test_configuration(yaml_file):
    conf = get_from_path(yaml_file)

    assert TEST_EXPECTS_KEY in conf, \
        "yaml file should contains expected test results"
    assert FEEDS_KEY in conf, "yaml file should contains a feed"

    res = execute_configuration(conf)

    for feed_name in conf[FEEDS_KEY].keys():
        assert feed_name in conf[TEST_EXPECTS_KEY], \
            "no expected result entry for the feed %s" % feed_name

    for test_name, test_result in conf[TEST_EXPECTS_KEY].items():
        assert test_name in res, "expected a test named %s" % test_name

        assert res[test_name] == test_result
