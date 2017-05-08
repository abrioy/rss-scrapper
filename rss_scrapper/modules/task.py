# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class Task:
    args = None

    def __init__(self, args):
        """
        The task will validate and parse its argument on creation
        if the arguments are invalid, a ConfigurationError will be raised
        Tasks may recursively call other tasks through the task_factory
        but it is advised to create all the required tasks in this function for
        validation purposes
        :param args:
        """
        self.args = args

    def execute(self, data):
        """
        The task will be executed with the provided data and return a list
        of whatever data is appropriate
        :param data:
        :return:
        """
        logger.debug("Executing task: %s" % self)

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def execute_subtasks(tasks, data):
        for task in tasks:
            if data is None:
                # First task
                data = task.execute(data)
            else:
                new_data = []
                for d in data:
                    new_data.append(task.execute(d))
                data = new_data

        return data
