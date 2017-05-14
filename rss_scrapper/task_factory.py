# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration import validate_task_name
from errors import ConfigurationError
import rss_scrapper.tasks.dummy
import rss_scrapper.tasks.feed
import rss_scrapper.tasks.text
import rss_scrapper.tasks.get
import rss_scrapper.tasks.xpath
import rss_scrapper.tasks.selector
import rss_scrapper.tasks.regex
import rss_scrapper.tasks.rss_gen
import rss_scrapper.tasks.write
import rss_scrapper.tasks.concat

logger = logging.getLogger(__name__)
TASKS = [
    rss_scrapper.tasks.dummy.DummyTask,
    rss_scrapper.tasks.feed.FeedTask,
    rss_scrapper.tasks.text.TextTask,
    rss_scrapper.tasks.get.GetTask,
    rss_scrapper.tasks.xpath.XPathTask,
    rss_scrapper.tasks.selector.SelectorTask,
    rss_scrapper.tasks.regex.RegexTask,
    rss_scrapper.tasks.rss_gen.RssGenTask,
    rss_scrapper.tasks.write.WriteTask,
    rss_scrapper.tasks.write.ReadTask,
    rss_scrapper.tasks.concat.ConcatTask,
]
TASKS_MAP = {task.name: task for task in TASKS}


def create_task(name, conf=None, parent_task=None):
    if name not in TASKS_MAP:
        raise ConfigurationError("the task '%s' does not exist" % name)
    else:
        task_class = TASKS_MAP[name]
        return task_class(conf=conf, parent_task=parent_task)


def create_tasks(tasks_conf, parent_task=None):
    tasks = []

    if not isinstance(tasks_conf, list):
        logger.error("Expected a task list and got a %s" % type(tasks_conf))
        raise ConfigurationError("no task list found", conf=tasks_conf)

    for task_conf in tasks_conf:
        if not isinstance(task_conf, dict):
            logger.error("Expected a task and got a %s" % type(task_conf))
            raise ConfigurationError("incorrect task definition",
                                     conf=task_conf)

        for task_name, task_args in task_conf.items():
            validate_task_name(task_name)

            try:
                tasks.append(create_task(task_name, task_args,
                                         parent_task=parent_task))
            except ConfigurationError as e:
                e.conf = task_conf
                raise e

    return tasks


def execute_configuration(conf, dry_run=False):
    if "feeds" not in conf:
        logger.error("The configuration lacks a feeds collection,"
                     " the yaml file should have a 'feeds' dictionary"
                     " at the top level")
        raise ConfigurationError("no feeds found", conf=conf)

    feeds = conf["feeds"]
    if not isinstance(feeds, dict):
        raise ConfigurationError("'feeds' should be a dictionary instead of %s"
                                 % type(feeds))

    logger.debug("Found %d feed(s)" % len(feeds))

    # We create every task before executing any for validation purposes
    tasks = []
    for feed_name, tasks_conf in feeds.items():
        logger.info("Validating feed %s" % feed_name)
        tasks.append((feed_name, create_task("feed", tasks_conf)))

    res = {}
    for (feed_name, task) in tasks:
        if not dry_run:
            logger.info("Executing feed %s" % feed_name)

            task_res = task.execute(None)

            task_res_data = list(task_res)

            if len(task_res_data) == 0:
                logger.info("The feed %s has not returned any data,"
                            " nothing has been generated" % feed_name)

            res[feed_name] = task_res_data
    return res
