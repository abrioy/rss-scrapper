# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class TextTask(Task):
    name = "text"

    text = ""

    def init(self, text=None):
        if text is not None:
            self.text = text

    def init_conf(self, conf):
        text = get_parameter(conf, param_type=str)

        self.init(text)

    def do_execute(self, data):
        yield self.text

    def __str__(self):
        return ("%s (string: '%s')"
                % (self.name, self.text))
