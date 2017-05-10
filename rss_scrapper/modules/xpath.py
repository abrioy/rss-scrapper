# -*- coding: utf-8 -*-
import logging
from lxml.html import fromstring
from lxml.etree import tostring

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class XPathTask(Task):
    name = "xpath"

    expression = ""

    def init(self, expression=None):
        if expression is not None:
            self.expression = expression

    def init_conf(self, conf):
        expression = get_parameter(conf, param_type=str)

        self.init(expression)

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
