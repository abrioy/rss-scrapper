# -*- coding: utf-8 -*-
import logging
from lxml.html import fromstring
from lxml.etree import tostring

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class XPathTask(Task):
    name = "xpath"

    expression = None

    def init(self, args):
        self.expression = get_parameter(args, param_type=str)

    def do_execute(self, data):
        dom = fromstring(data)

        elements = dom.xpath(self.expression)
        for element in elements:
            if isinstance(element, str):
                yield element
            else:
                yield tostring(element, encoding='unicode')

    def __str__(self):
        return ("%s (expression: '%s')"
                % (self.name, self.expression))
