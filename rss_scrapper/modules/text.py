# -*- coding: utf-8 -*-
import logging

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class TextTask(Task):
    text = None

    def __init__(self, args):
        Task.__init__(self, args)

        self.text = Task.get_parameter(args, param_type=str)

    def do_execute(self, data):
        yield self.text
