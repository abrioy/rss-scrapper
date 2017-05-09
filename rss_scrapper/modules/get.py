# -*- coding: utf-8 -*-
import logging

import requests as requests

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class GetTask(Task):
    name = "get"

    url = None

    def init(self, args):
        self.url = Task.get_parameter(args, "url", str)
        # TODO: Add auth to parameters

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
