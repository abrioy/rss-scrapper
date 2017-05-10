# -*- coding: utf-8 -*-
import logging
from cssselect import GenericTranslator

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.modules.xpath import XPathTask

logger = logging.getLogger(__name__)


class SelectorTask(XPathTask):
    name = "selector"

    selector = ""

    def init(self, selector=None):
        if selector is not None:
            self.selector = selector

        expression = GenericTranslator().css_to_xpath(self.selector)
        XPathTask.init(self, expression)

    def init_conf(self, conf):
        selector = get_parameter(conf, param_type=str)

        self.init(selector)

    def __str__(self):
        return ("%s (expression: %s)"
                % (self.name, self.selector))
