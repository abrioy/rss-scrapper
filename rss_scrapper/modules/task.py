# -*- coding: utf-8 -*-
import logging

import rss_scrapper.task_factory
from rss_scrapper.configuration import ConfigurationError

logger = logging.getLogger(__name__)


class Task:
    name = "task"
    path = ""

    args = None

    def __init__(self, args, path=""):
        """
        The constructor calls the self.init() function and logs the
         ConfigurationError that it catches, it is not intended to be
         overridden
        :param args:
        """
        self.args = args
        self.path = path
        try:
            self.init(args)
        except ConfigurationError as e:
            if e.task is None:
                e.task = self
            raise e

    def init(self, args):
        """
        This function will be called in the constructor, subclasses are to
         initialize their fields here
        The task will validate and parse its argument on creation
         if the arguments are invalid, a ConfigurationError will be raised
         Tasks may recursively call other tasks through the task_factory
         but it is advised to create all the required tasks in this function
         for validation purposes
        :param args:
        :return:
        """
        raise NotImplementedError

    def execute(self, data):
        """
        The task will be executed with the provided data and return a generator
        This function is not intended to be reimplemented by subclasses
        :param data: a (most likely unicode) string of data
        :return: a generator of (preferably unicode) strings
        """
        # logger.debug("%s\n%s" % (type(data), data))
        logger.debug("Execute task: %s" % self.get_path())

        res = self.do_execute(data)
        return res

    def do_execute(self, data):
        """
        This function is intended to be extended by subclasses
        :param data: a (most likely unicode) string of data
        :return: a generator of (preferably unicode) strings
        """
        raise NotImplementedError

    def execute_tasks(self, tasks, data, index=0):
        if index >= len(tasks):
            yield data
        else:
            task = tasks[index]
            res = task.execute(data)

            for res_data in res:
                yield from self.execute_tasks(tasks, res_data, index=index + 1)

    def create_subtask(self, args, subpath=None):
        path = self.get_path()
        if subpath is not None:
            path += "[%s]" % subpath

        return rss_scrapper.task_factory.create_task(
            args, base_path=path)

    def create_subtasks(self, args, subpath=None):
        path = self.get_path()
        if subpath is not None:
            path += "[%s]" % subpath

        return rss_scrapper.task_factory.create_tasks(
            args, base_path=path)

    def get_path(self):
        return self.path + '/' + self.name

    def __str__(self):
        return self.__class__.name
