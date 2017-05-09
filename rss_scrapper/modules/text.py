# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class TextTask(Task):
    name = "text"

    text = None

    def init(self, args):
        self.text = get_parameter(args, param_type=str)

    def do_execute(self, data):
        yield self.text

    def __str__(self):
        return ("%s (string: '%s')"
                % (self.name, self.text))
