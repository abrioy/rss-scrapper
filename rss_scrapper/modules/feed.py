# -*- coding: utf-8 -*-
import logging

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class FeedTask(Task):
    name = "feed"

    tasks = []

    def init(self, tasks=None):
        if tasks is not None:
            self.tasks = tasks

        if len(tasks) == 0:
            logger.warning("There is no tasks in this feed, nothing will"
                           "be generated")

    def init_conf(self, conf):
        tasks = self.create_subtasks(conf)

        self.init(tasks)

    def do_execute(self, data):
        return self.execute_tasks(self.tasks, data)
