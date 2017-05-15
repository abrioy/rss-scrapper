# -*- coding: utf-8 -*-
import logging
from re import compile

from rss_scrapper.errors import ExecutionError
from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class RegexTask(Task):
    name = "regex"

    pattern = ""
    pattern_expression = None
    replace = ""
    flags = 0

    def init(self, pattern=None, replace=None, flags=None):
        if pattern is not None:
            self.pattern = pattern
        if replace is not None:
            self.replace = replace
        if flags is not None:
            self.flags = flags

        self.pattern_expression = compile(self.pattern, self.flags)

    def init_conf(self, conf):
        pattern = get_parameter(conf, "pattern", str)
        replace = get_parameter(conf, "replace", str)
        flags = get_parameter(conf, "flags", int, optional=True)

        self.init(pattern, replace, flags)

    def do_execute(self, data):
        if data is None or not isinstance(data, str):
            raise ExecutionError("This task can only work if it receives a"
                                 " string", data=data)

        yield self.pattern_expression.sub(self.replace, data)

    def __str__(self):
        return ("%s (pattern: '%s', flags: %d, replace: '%s')"
                % (self.name, self.pattern, self.flags, self.replace))
