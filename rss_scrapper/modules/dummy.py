# -*- coding: utf-8 -*-
import logging

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class DummyTask(Task):
    name = "dummy"

    def init(self):
        pass

    def init_conf(self, conf):
        pass

    def do_execute(self, data):
        yield data
