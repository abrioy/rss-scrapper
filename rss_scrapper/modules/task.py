# -*- coding: utf-8 -*-
import logging

from configuration import ConfigurationError

logger = logging.getLogger(__name__)


class Task:
    name = "task"

    args = None

    def __init__(self, args):
        """
        The constructor calls the self.init() function and logs the
         ConfigurationError that it catches, it is not intended to be
         overridden
        :param args:
        """
        self.args = args
        try:
            self.init(args)
        except ConfigurationError as e:
            e.task_path = str(self) + "/" + e.task_path
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
        logger.debug("%s\n%s" % (type(data), data))
        logger.debug("Start task: %s" % self)

        res = self.do_execute(data)

        logger.debug("Stop task:  %s" % self)
        return res

    def do_execute(self, data):
        """
        This function is intended to be extended by subclasses
        :param data: a (most likely unicode) string of data
        :return: a generator of (preferably unicode) strings
        """
        raise NotImplementedError

    def __str__(self):
        return self.__class__.name

    @staticmethod
    def get_parameter(conf, param_name=None, param_type=None, optional=False):
        if param_name is None:
            param = conf
        else:
            if conf is None:
                if optional:
                    return None
                else:
                    raise ConfigurationError(
                        "parameter %s not found, this task expected a"
                        " configuration and got nothing (is there an"
                        " indentation problem ?)" % param_name, conf)

            if not isinstance(conf, dict):
                if optional:
                    return None
                else:
                    raise ConfigurationError(
                        "the task expects a dictionary as its configuration,"
                        " parameter %s not found" % param_name, conf)

            if param_name not in conf:
                if optional:
                    return None
                else:
                    raise ConfigurationError(
                        "the task lacks a mandatory parameter: %s"
                        % param_name, conf)
            param = conf[param_name]

        # Type check
        if param_type is not None:
            if not isinstance(param, param_type):
                raise ConfigurationError("the %s parameter does not have the"
                                         " correct type, expected %s and"
                                         " got %s"
                                         % (param_name, param_type,
                                            type(param)),
                                         conf)
            else:
                return param_type(param)

        return param
