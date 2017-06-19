# -*- coding: utf-8 -*-

from rss_scrapper.task_factory import create_task
from rss_scrapper.tasks.dump import DumpTask


def test_task_dump_create():
    task = create_task("dump")
    assert isinstance(task, DumpTask)

    res = task.execute(None)

    res_data = list(res)
    assert len(res_data) == 0


def test_task_dump_execute():
    task = create_task("dump")
    assert isinstance(task, DumpTask)

    res = task.execute(['A', 'B', 'C'])

    res_data = list(res)
    assert len(res_data) == 0

    res = task.execute(range(1, 100))

    res_data = list(res)
    assert len(res_data) == 0
