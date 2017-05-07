# -*- coding: utf-8 -*-

import argparse
import logging
import time


def main():
    parser = argparse.ArgumentParser(
        prog='rss_scrapper',
        description='',
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Logging
    parser.add_argument(
        '--log', action='store', required=False,
        dest='log_level', default='4',
        help='logging level (default=4):'
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

    logger.debug("Done in %.02fs." % (time.time() - start))


if __name__ == "__main__":
    main()
