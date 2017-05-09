# -*- coding: utf-8 -*-
import logging

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class FeedTask(Task):
    name = "feed"

    tasks = []

    def init(self, args):
        if len(args) == 0:
            logger.warning("There is no tasks in this feed, nothing will"
                           "be generated")

        self.tasks = self.create_subtasks(args)

    def do_execute(self, data):
        return self.execute_tasks(self.tasks, data)
