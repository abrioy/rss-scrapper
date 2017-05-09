# -*- coding: utf-8 -*-
import logging
from re import compile

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class RegexTask(Task):
    name = "regex"

    pattern = None
    replace = None
    flags = 0

    def init(self, args):
        pattern_text = Task.get_parameter(args, "pattern", str)
        self.flags = Task.get_parameter(args, "flags", int, optional=True)
        if self.flags is None:
            self.flags = 0
        self.pattern = compile(pattern_text, int(self.flags))

        self.replace = Task.get_parameter(args, "replace", str)

    def do_execute(self, data):
        yield self.pattern.sub(self.replace, data)

    def __str__(self):
        return ("%s (pattern: '%s', flags: %d, replace: '%s')"
                % (self.name, self.pattern, self.flags, self.replace))
