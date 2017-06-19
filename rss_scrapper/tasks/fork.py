# -*- coding: utf-8 -*-
import logging

from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class ForkTask(Task):
    name = "fork"

    tasks = []

    def init(self, tasks=None):
        if tasks is not None:
            self.tasks = tasks

    def init_conf(self, conf):
        tasks = self.create_subtasks(conf)

        self.init(tasks)

    def do_execute(self, data):
        for task in self.tasks:
            res = task.execute(data)
            yield from res
