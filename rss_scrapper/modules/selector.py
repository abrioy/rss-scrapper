# -*- coding: utf-8 -*-
import logging
from cssselect import GenericTranslator

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.modules.xpath import XPathTask

logger = logging.getLogger(__name__)


class SelectorTask(XPathTask):
    name = "selector"

    selector_text = None

    def init(self, args):
        self.selector_text = get_parameter(args, param_type=str)
        self.expression = GenericTranslator().css_to_xpath(self.selector_text)

    def __str__(self):
        return ("%s (expression: %s)"
                % (self.name, self.selector_text))
