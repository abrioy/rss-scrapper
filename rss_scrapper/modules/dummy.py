# -*- coding: utf-8 -*-
import logging

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class DummyTask(Task):
    name = "dummy"

    def init(self, args):
        pass

    def do_execute(self, data):
        yield data
