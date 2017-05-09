# -*- coding: utf-8 -*-
import logging
from feedgen.feed import FeedGenerator

import rss_scrapper.task_factory
from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.modules.task import Task

logger = logging.getLogger(__name__)


class RssGenTask(Task):
    name = "rss_gen"

    input_tasks = []
    output_feed_tasks = {}
    output_elems_tasks = {}
    copy_fields = None

    def init(self, args):
        self.copy_fields = get_parameter(args, "copy_fields", bool,
                                         optional=True)
        if self.copy_fields is None:
            self.copy_fields = False

        input_conf = get_parameter(args, "input", list)
        output_conf = get_parameter(args, "output", dict)
        output_feed_conf = get_parameter(output_conf, "feed", dict)
        output_elems_conf = get_parameter(output_conf, "elements", dict)

        self.input_tasks = \
            rss_scrapper.task_factory.create_tasks(input_conf)

        # Feed attributes tasks
        for attribute, att_tasks_conf in output_feed_conf.items():
            self.output_feed_tasks[attribute] = \
                rss_scrapper.task_factory.create_tasks(att_tasks_conf)

        # Elements attributes tasks
        for attribute, att_tasks_conf in output_elems_conf.items():
            self.output_elems_tasks[attribute] = \
                rss_scrapper.task_factory.create_tasks(att_tasks_conf)

    def do_execute(self, data):
        input_res = rss_scrapper.task_factory.execute_tasks(
            self.input_tasks, data)
        input_data_list = list(input_res)

        # Rss feed header
        fg = FeedGenerator()
        fill_feed_info(fg, self.output_feed_tasks, data)

        # Feed content
        for data in input_data_list:
            feed_entry = fg.add_entry()
            fill_feed_info(feed_entry, self.output_elems_tasks, data)

        yield fg.rss_str(pretty=True)


def fill_feed_info(info, elements_tasks, data):
    for attribute, att_tasks in elements_tasks.items():
        res = rss_scrapper.task_factory.execute_tasks(att_tasks, data)

        res_data = list(res)
        if len(res_data) == 0:
            logger.warning("The output task for the attribute %s has"
                           " not returned any data, skipping the"
                           " attribute" % attribute)
        elif len(res_data) > 1:
            logger.warning("The output task for the attribute %s has"
                           " returned more than one value, skipping"
                           " the attribute" % attribute)
        else:
            # FIXME: Quick because the link attribute expects a dictionary
            if attribute == "link":
                res_data[0] = {'href': res_data[0]}

            # Calling the setter
            setter = getattr(info, attribute)
            setter(res_data[0])
