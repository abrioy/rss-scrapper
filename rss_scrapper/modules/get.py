# -*- coding: utf-8 -*-
import logging

import requests as requests

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class GetTask(Task):
    url = None

    def __init__(self, args):
        Task.__init__(self, args)

        self.url = Task.get_parameter(args, "url", str)
        # TODO: Add auth to parameters

    def do_execute(self, data):
        if data is not None:
            logger.warning("This task has been called with some data and is"
                           " not supposed to make use of it. The following"
                           " data has been discarded: %s" % data)

        response = requests.get(self.url)
        yield response.text
