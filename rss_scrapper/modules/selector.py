# -*- coding: utf-8 -*-
import logging
from cssselect import GenericTranslator

from modules.xpath import XPathTask
from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class SelectorTask(XPathTask):
    def __init__(self, args):
        Task.__init__(self, args)

        selector_text = Task.get_parameter(args, param_type=str)
        self.expression = GenericTranslator().css_to_xpath(selector_text)
