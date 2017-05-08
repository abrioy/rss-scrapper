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

    def execute(self, data):
        Task.execute(self, data)

        return Task.execute_subtasks(self.tasks, data)
