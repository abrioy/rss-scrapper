# -*- coding: utf-8 -*-
import logging

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class ConcatTask(Task):
    name = "concat"

    tasks = []

    def init(self, tasks=None):
        if tasks is not None:
            self.tasks = tasks

    def init_conf(self, conf):
        tasks = self.create_subtasks(conf)

        self.init(tasks)

    def do_execute(self, data):
        concat_res = ''
        for task in self.tasks:
            res_data = list(task.execute(data))
            concat_res += ''.join(res_data)

        yield concat_res
