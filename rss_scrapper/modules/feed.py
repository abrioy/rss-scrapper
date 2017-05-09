# -*- coding: utf-8 -*-
import logging

import rss_scrapper.task_factory
from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class FeedTask(Task):
    name = "feed"

    tasks = []

    def init(self, args):
        if len(args) == 0:
            logger.warning("There is no tasks in this feed, nothing will"
                           "be generated")

        self.tasks = rss_scrapper.task_factory.create_tasks(args)

    def do_execute(self, data):
        return self.execute_tasks(self.tasks, data)
