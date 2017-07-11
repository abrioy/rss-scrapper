# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config
import time

import sys

from rss_scrapper.configuration import get_from_path
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
        'configuration', action='store',
        metavar="input.yaml", type=str,
        help='the configuration file'
    )

    args = parser.parse_args()

    # Configuring logging
    logging.config.fileConfig('rss_scrapper/logging.ini')
    logger = logging.getLogger('rss_scrapper')

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

    if args.configuration:
        start = time.time()
        logger.debug("Starting...")

        conf = get_from_path(args.configuration)
        result = execute_configuration(conf)
        sys.stdout.write(result)

        logger.debug("Done in %.02fs." % (time.time() - start))

if __name__ == "__main__":
    main()
