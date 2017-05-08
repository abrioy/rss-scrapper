# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration import ConfigurationError, validate_task_name
import rss_scrapper.modules.feed
import rss_scrapper.modules.get
import rss_scrapper.modules.selector
import rss_scrapper.modules.regex

logger = logging.getLogger(__name__)

TASKS_MAP = {
    "feed": rss_scrapper.modules.feed.FeedTask,
    "get": rss_scrapper.modules.get.GetTask,
    "selector": rss_scrapper.modules.selector.SelectorTask,
    "regex": rss_scrapper.modules.regex.RegexTask,
}


def create_task(name, args):
    if name not in TASKS_MAP:
        raise ConfigurationError("the task '%s' does not exist" % name)
    else:
        task_class = TASKS_MAP[name]
        return task_class(args)


def create_tasks(tasks_conf):
    tasks = []

    if not isinstance(tasks_conf, list):
        logger.error("Expected a task list and got a %s" % type(tasks_conf))
        raise ConfigurationError("no task list found", tasks_conf)

    for task_conf in tasks_conf:
        if not isinstance(task_conf, dict):
            logger.error("Expected task and for a %s" % type(task_conf))
            raise ConfigurationError("incorrect task definition", task_conf)

        for task_name, task_args in task_conf.items():
            validate_task_name(task_name)

            try:
                tasks.append(create_task(task_name, task_args))
            except ConfigurationError as e:
                e.node = task_conf
                raise e

    return tasks


def execute_configuration(conf, dry_run=False):
    if "feeds" not in conf:
        logger.error("The configuration lacks a feeds collection,"
                     " the yaml file should have a 'feeds' dictionary"
                     " at the top level")
        raise ConfigurationError("no feeds found", conf)

    feeds = conf["feeds"]
    if not isinstance(feeds, dict):
        raise ConfigurationError("'feeds' should be a dictionary instead of %s"
                                 % type(feeds))

    logger.debug("Found %d feed(s)" % len(feeds))

    for feed_name, tasks_conf in feeds.items():
        logger.info("Feed %s" % feed_name)

        feed_task = create_task("feed", tasks_conf)
        if not dry_run:
            task_res = feed_task.execute(None)

            res = list(task_res)

            if len(res) == 0:
                logger.info("The feed %s has not returned any data,"
                            " nothing has been generated" % feed_name)
            else:
                logger.info(res)
