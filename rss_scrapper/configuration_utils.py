# -*- coding: utf-8 -*-
import logging

from rss_scrapper.configuration import ConfigurationError

logger = logging.getLogger(__name__)


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
            if param_name is None:
                param_display_name = "default"
            else:
                param_display_name = param_name

            raise ConfigurationError("the %s parameter does not have the"
                                     " correct type, expected %s and"
                                     " got %s"
                                     % (param_display_name, param_type,
                                        type(param)),
                                     conf)
        else:
            return param_type(param)

    return param
