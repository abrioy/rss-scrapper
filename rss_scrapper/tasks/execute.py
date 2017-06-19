# -*- coding: utf-8 -*-
import logging

from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class ExecuteTask(Task):
    name = "execute"

    tasks = []

    def init(self, tasks=None):
        if tasks is not None:
            self.tasks = tasks

    def init_conf(self, conf):
        tasks = self.create_subtasks(conf)

        self.init(tasks)

    def do_execute(self, data):
        return self.execute_tasks(self.tasks, data)
