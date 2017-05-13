# -*- coding: utf-8 -*-
import os
from types import GeneratorType

import pytest

from rss_scrapper.task_factory import create_task
from rss_scrapper.tasks.read import ReadTask

TEST_DATA_FOLDER = "tests/test_data"


@pytest.fixture(params={
    "lorem_ipsum.txt",
    "utf-8.txt",
    "cp1252.txt",
})
def test_file_path(request):
    return os.path.join(TEST_DATA_FOLDER, request.param)


def test_task_read(test_file_path):
    task = create_task("read")
    assert isinstance(task, ReadTask)

    task.init(file_name=test_file_path)

    res = task.execute(None)
    assert isinstance(res, GeneratorType)

    res_data = list(res)
    assert len(res_data) == 1
    res_data = res_data[0]

    with open(test_file_path, 'rb') as test_file:
        test_data = test_file.read()
        assert test_data == res_data
