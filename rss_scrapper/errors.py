# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class TaskError(Exception):
    task = None

    def __init__(self, message, task=None):
        Exception.__init__(self, message)

        if task is not None:
            self.task = task

    def __str__(self):
        message = ""

        if self.task:
            message += "[task: " + self.task.get_path() + "] "

        message += Exception.__str__(self)

        return message


class ConfigurationError(TaskError):
    conf = None

    def __init__(self, message, task=None, conf=None):
        TaskError.__init__(self, message, task=task)

        self.conf = conf

    def __str__(self):
        message = TaskError.__str__(self)

        if self.conf is not None:
            message += " - invalid configuration: \n%s" % self.conf

        return message


class ExecutionError(TaskError):
    data = None

    def __init__(self, message, task=None, data=None):
        TaskError.__init__(self, message, task=task)

        self.data = data

    def __str__(self):
        message = TaskError.__str__(self)

        if self.data is not None:
            message += " - invalid data: \n%s" % self.data

        return message
