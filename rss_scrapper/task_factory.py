# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration import ConfigurationError, validate_task_name
import rss_scrapper.modules.dummy
import rss_scrapper.modules.feed
import rss_scrapper.modules.text
import rss_scrapper.modules.get
import rss_scrapper.modules.xpath
import rss_scrapper.modules.selector
import rss_scrapper.modules.regex
import rss_scrapper.modules.rss_gen
import rss_scrapper.modules.write
import rss_scrapper.modules.concat

logger = logging.getLogger(__name__)
TASKS = [
    rss_scrapper.modules.dummy.DummyTask,
    rss_scrapper.modules.feed.FeedTask,
    rss_scrapper.modules.text.TextTask,
    rss_scrapper.modules.get.GetTask,
    rss_scrapper.modules.xpath.XPathTask,
    rss_scrapper.modules.selector.SelectorTask,
    rss_scrapper.modules.regex.RegexTask,
    rss_scrapper.modules.rss_gen.RssGenTask,
    rss_scrapper.modules.write.WriteTask,
    rss_scrapper.modules.concat.ConcatTask,
]
TASKS_MAP = {task.name: task for task in TASKS}


def create_task(name, args, parent_task=None):
    if name not in TASKS_MAP:
        raise ConfigurationError("the task '%s' does not exist" % name)
    else:
        task_class = TASKS_MAP[name]
        return task_class(args, parent_task=parent_task)


def create_tasks(tasks_conf, parent_task=None):
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
                tasks.append(create_task(task_name, task_args,
                                         parent_task=parent_task))
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

    # We create every task before executing any for validation purposes
    tasks = []
    for feed_name, tasks_conf in feeds.items():
        logger.info("Validating feed %s" % feed_name)
        tasks.append((feed_name, create_task("feed", tasks_conf)))

    for (feed_name, task) in tasks:
        if not dry_run:
            logger.info("Executing feed %s" % feed_name)

            task_res = task.execute(None)

            res = list(task_res)

            if len(res) == 0:
                logger.info("The feed %s has not returned any data,"
                            " nothing has been generated" % feed_name)
            else:
                logger.info(res)
