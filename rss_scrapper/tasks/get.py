# -*- coding: utf-8 -*-
import logging
import requests

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class GetTask(Task):
    name = "get"

    url = ""

    def init(self, url=None):
        if url is not None:
            self.url = url

    def init_conf(self, conf):
        url = get_parameter(conf, "url", str)
        # TODO: Add auth to parameters

        self.init(url)

    def do_execute(self, data):
        if data is not None:
            logger.warning("This task has been called with some data and is"
                           " not supposed to make use of it. The following"
                           " data has been discarded: %s" % data)

        response = requests.get(self.url)
        yield response.text

    def __str__(self):
        return ("%s (url: '%s')"
                % (self.name, self.url))
