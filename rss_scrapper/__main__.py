# -*- coding: utf-8 -*-

import argparse
import logging
import time

from rss_scrapper.configuration import load_yaml_from_path
from rss_scrapper.task_factory import execute_configuration


def main():
    parser = argparse.ArgumentParser(
        prog='rss_scrapper',
        description='',
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Logging
    parser.add_argument(
        '--log', action='store', required=False,
        dest='log_level', default='5',
        help='logging level (default=5):'
             '\n0=off, 1=critical, 2=errors, 3=warnings, 4=info, 5=debug'
    )
    parser.add_argument(
        '--log-output', action='store', required=False,
        dest='logOutput', default=None,
        help='output log file'
    )

    args = parser.parse_args()

    # Configuring logging
    logger = logging.getLogger("rss_scrapper")
    if args.logOutput:
        handler = logging.FileHandler(args.logOutput)
    else:
        handler = logging.StreamHandler()

    formatter = logging.Formatter(
        '%(name)s |%(asctime)s| %(levelname)-7s %(module)s:%(lineno)-3d -'
        ' %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    log_levels = {
        '0': logging.NOTSET,
        '1': logging.CRITICAL,
        '2': logging.ERROR,
        '3': logging.WARNING,
        '4': logging.INFO,
        '5': logging.DEBUG
    }
    try:
        logger.setLevel(log_levels[args.log_level])
    except KeyError:
        logger.setLevel(logging.NOTSET)
        logger.warning("Invalid logging level:", args.log_level)

    start = time.time()
    logger.debug("Starting...")

    conf = load_yaml_from_path("input.yaml")
    res = execute_configuration(conf)
    print(res)

    logger.debug("Done in %.02fs." % (time.time() - start))


if __name__ == "__main__":
    main()
