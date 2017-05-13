# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class ReadTask(Task):
    name = "read"

    file_name = ""

    def init(self, file_name=None):
        if file_name is not None:
            self.file_name = file_name

    def init_conf(self, conf):
        file_name = get_parameter(conf, param_type=str)

        self.init(file_name)

    def do_execute(self, data):
        with open(self.file_name, 'rb') as file:
            yield file.read()

    def __str__(self):
        return ("%s (file: '%s')"
                % (self.name, self.file_name))
