# -*- coding: utf-8 -*-
import logging

from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class DumpTask(Task):
    name = "dump"

    def init(self):
        pass

    def init_conf(self, conf):
        pass

    def do_execute(self, data):
        pass
