# -*- coding: utf-8 -*-
import logging

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class ConcatTask(Task):
    name = "concat"

    tasks = None

    def init(self, args):
        self.tasks = self.create_subtasks(args)

    def do_execute(self, data):
        concat_res = ''
        for task in self.tasks:
            res_data = list(task.execute(data))
            concat_res += ''.join(res_data)

        yield concat_res
