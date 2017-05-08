# -*- coding: utf-8 -*-
import logging

from lxml.html import fromstring
from lxml.etree import tostring

from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class XPathTask(Task):
    expression = None

    def __init__(self, args):
        Task.__init__(self, args)

        self.expression = Task.get_parameter(args, param_type=str)

    def do_execute(self, data):
        dom = fromstring(data)

        elements = dom.xpath(self.expression)
        for element in elements:
            yield tostring(element, encoding='unicode')
