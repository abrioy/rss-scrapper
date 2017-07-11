# -*- coding: utf-8 -*-
import logging

import parsedatetime as parsedatetime
import pytz
from feedgen.feed import FeedGenerator

from rss_scrapper.configuration_utils import get_parameter
from rss_scrapper.tasks.task import Task

logger = logging.getLogger(__name__)


class RssGenTask(Task):
    name = "rss_gen"

    copy_fields = False
    input_tasks = []
    output_feed_tasks = {}
    output_elems_tasks = {}

    def init(self, copy_fields=None, input_tasks=None, output_feed_tasks=None,
             output_elems_tasks=None):
        if copy_fields is not None:
            self.copy_fields = copy_fields
        if input_tasks is not None:
            self.input_tasks = input_tasks
        if output_feed_tasks is not None:
            self.output_feed_tasks = output_feed_tasks
        if output_elems_tasks is not None:
            self.output_elems_tasks = output_elems_tasks

    def init_conf(self, conf):
        copy_fields = get_parameter(conf, "copy_fields", bool,
                                    optional=True)

        input_conf = get_parameter(conf, "input", list)
        output_conf = get_parameter(conf, "output", dict)

        output_feed_conf = get_parameter(output_conf, "feed", dict)
        output_elems_conf = get_parameter(output_conf, "elements", dict)

        # Input tasks
        input_tasks = \
            self.create_subtasks(input_conf, subpath="input")

        # Feed attributes tasks
        output_feed_tasks = {}
        for attribute, att_tasks_conf in output_feed_conf.items():
            subpath = "feed/" + attribute
            output_feed_tasks[attribute] = \
                self.create_subtasks(att_tasks_conf, subpath=subpath)

        # Elements attributes tasks
        output_elems_tasks = {}
        for attribute, att_tasks_conf in output_elems_conf.items():
            subpath = "elements/" + attribute
            output_elems_tasks[attribute] = \
                self.create_subtasks(att_tasks_conf, subpath=subpath)

        self.init(copy_fields, input_tasks, output_feed_tasks,
                  output_elems_tasks)

    def do_execute(self, data):
        input_res = self.execute_tasks(self.input_tasks, data)
        input_data_list = list(input_res)

        # Rss feed header
        fg = FeedGenerator()
        self.fill_feed_info(fg, self.output_feed_tasks, data)

        # Feed content
        for data in input_data_list:
            feed_entry = fg.add_entry()
            self.fill_feed_info(feed_entry, self.output_elems_tasks, data)

        yield fg.rss_str(pretty=True)

    def fill_feed_info(self, info, elements_tasks, data):
        for attribute, att_tasks in elements_tasks.items():
            res = self.execute_tasks(att_tasks, data)

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
                # FIXME: Quick fix because the link attribute expects a dict
                if attribute == "link":
                    res_data[0] = {'href': res_data[0]}
                elif attribute == "pubdate":
                    calendar = parsedatetime.Calendar()
                    res_data[0], _ = calendar.parseDT(
                        datetimeString=res_data[0],
                        tzinfo=pytz.utc)

                # Calling the setter
                setter = getattr(info, attribute)
                setter(res_data[0])
