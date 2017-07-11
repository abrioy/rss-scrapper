# -*- coding: utf-8 -*-
import logging

import yaml
from yaml import YAMLError

logger = logging.getLogger(__name__)


def get_from_path(path):
    with open(path, 'r') as file:
        return get_from_file(file)


def get_from_file(file):
    logger.debug("Loading configuration from: %s" % file.name)
    try:
        return yaml.load(file)
    except YAMLError as e:
        logger.error("Error while parsing the configuration file: %s %s"
                     % (type(e).__name__, e))
        raise e
