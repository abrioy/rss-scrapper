# -*- coding: utf-8 -*-
import os
from types import GeneratorType

import pytest

from rss_scrapper.task_factory import create_task
from rss_scrapper.tasks.read import ReadTask

TEST_DATA_FOLDER = "tests/test_data"


@pytest.fixture(params={
    ('lorem_ipsum.txt', None),
    ('utf-8.txt', 'utf-8'),
    ('cp1252.txt', 'cp1252')
})
def test_file(request):
    return os.path.join(TEST_DATA_FOLDER, request.param[0]), request.param[1]


def test_task_read(test_file):
    task = create_task("read")
    assert isinstance(task, ReadTask)

    task.init(file_name=test_file[0], encoding=test_file[1])

    res = task.execute(None)
    assert isinstance(res, GeneratorType)

    res_data = list(res)
    assert len(res_data) == 1
    res_data = res_data[0]

    with open(test_file[0], 'r', encoding=test_file[1]) as file:
        test_data = file.read()
        assert test_data == res_data
