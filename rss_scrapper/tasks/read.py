# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class ReadTask(Task):
    name = "read"

    file_name = ""
    encoding = None

    def init(self, file_name=None, encoding=None):
        if file_name is not None:
            self.file_name = file_name
        if encoding is not None:
            self.encoding = encoding

    def init_conf(self, conf):
        file_name = get_parameter(conf, 'file', param_type=str)
        encoding = get_parameter(conf, 'encoding', param_type=str,
                                 optional=True)

        self.init(file_name, encoding)

    def do_execute(self, data):
        with open(self.file_name, 'r', encoding=self.encoding) as file:
            yield file.read()

    def __str__(self):
        return ("%s (file: '%s')"
                % (self.name, self.file_name))
