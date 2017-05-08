# -*- coding: utf-8 -*-
import logging

from configuration import ConfigurationError

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
        logger.debug("%s\n%s" % (type(data), data))
        logger.debug("Start task: %s" % self)
        res = self.do_execute(data)
        logger.debug("Stop task: %s" % self)
        return res

    def do_execute(self, data):
        """
        This function is intended to be extended by subclasses
        :param data:
        :return:
        """
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def get_parameter(conf, param_name=None, param_type=None, optional=False):
        if param_name is None:
            param = conf
        else:
            if param_name not in conf:
                if optional:
                    return None
                else:
                    raise ConfigurationError("the task lacks a mandatory"
                                             " parameter: %s" % param_name,
                                             conf)
            param = conf[param_name]

        # Type check
        if param_type is not None and not isinstance(param, param_type):
            raise ConfigurationError("the %s parameter does not have the"
                                     " correct type, expected %s and got %s"
                                     % (param_name, param_type,
                                        type(param)),
                                     conf)
        return param
