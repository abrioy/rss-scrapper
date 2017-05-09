# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class WriteTask(Task):
    name = "write"

    file_name = None

    def init(self, args):
        self.file_name = get_parameter(args, param_type=str)

    def do_execute(self, data):
        with open(self.file_name, 'wb') as file:
            file.write(data)

        yield data

    def __str__(self):
        return ("%s (file: '%s')"
                % (self.name, self.file_name))
