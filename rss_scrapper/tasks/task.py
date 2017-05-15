# -*- coding: utf-8 -*-
import logging

import rss_scrapper.task_factory
from rss_scrapper.errors import TaskError

logger = logging.getLogger(__name__)


class Task:
    name = "task"
    parent_task = None

    args = None

    def __init__(self, conf=None, parent_task=None):
        """
        The constructor calls the self.init() function and logs the
         ConfigurationError that it catches, it is not intended to be
         overridden
        :param conf:
        """
        self.parent_task = parent_task

        if conf is not None:
            try:
                self.init_conf(conf)
            except TaskError as e:
                if e.task is None:
                    e.task = self
                raise e

    def init_conf(self, conf):
        """
        This function will be called in the constructor, subclasses are to
         parse their configuration here.
        If the configuration is invalid, a ConfigurationError will be raised.
        Tasks may recursively create other tasks through the appropriate method
         but it is advised to create them all in this function for validation
        purposes
        :param conf:
        :return:
        """
        raise NotImplementedError

    def init(self):
        """
        This function is intended to initialize all the static data required
         by the task
        This will be called from the init_conf function (and thus the
         constructor if a configuration was passed) in order to initialize
         the task
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
            args, parent_task=self)

    def create_subtasks(self, args, subpath=None):
        path = self.get_path()
        if subpath is not None:
            path += "[%s]" % subpath

        return rss_scrapper.task_factory.create_tasks(
            args, parent_task=self)

    def get_path(self):
        if self.parent_task is None:
            return '/' + self.name
        else:
            return self.parent_task.get_path() + '/' + self.name

    def __str__(self):
        return self.__class__.name
