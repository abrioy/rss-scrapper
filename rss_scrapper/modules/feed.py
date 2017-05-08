# -*- coding: utf-8 -*-
import logging

import rss_scrapper.task_factory
from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class FeedTask(Task):
    tasks = []

    def __init__(self, args):
        Task.__init__(self, args)

        if len(args) == 0:
            logger.warning("There is no tasks in this feed, nothing will"
                           "be generated")

        self.tasks = rss_scrapper.task_factory.create_tasks(args)

    def do_execute(self, data):
        return execute_sub_tasks(self.tasks, 0, data)


def execute_sub_tasks(tasks, index, data):
    if index >= len(tasks):
        yield data
        return

    task = tasks[index]
    res = task.execute(data)

    for d in res:
        yield from execute_sub_tasks(tasks, index+1, d)
