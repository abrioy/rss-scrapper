# -*- coding: utf-8 -*-
import logging
from re import compile

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class RegexTask(Task):
    pattern = None
    replace = None

    def __init__(self, args):
        Task.__init__(self, args)

        pattern_text = Task.get_parameter(args, "pattern", str)
        flags = Task.get_parameter(args, "flags", int, optional=True)
        if flags is None:
            flags = 0
        self.pattern = compile(pattern_text, flags)

        self.replace = Task.get_parameter(args, "replace", str)

    def do_execute(self, data):
        yield self.pattern.sub(self.replace, data)
