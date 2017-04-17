#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

import sys
from argparse import ArgumentParser
from argparse import SUPPRESS
from argparse import ArgumentError
from data import cmdLineArgument


def cmdLineParser():
    """
        cmdline parser, parse the parameters and arguments from cmdline
    """
    argv = None
    if not sys.argv:
        argv = sys.argv[1:]

    parser = ArgumentParser(description="Process the cmdline input.",
                            usage="%(prog)s [options]",
                            argument_default=SUPPRESS)

    parser.add_argument("--domain", "-d", required=True,
                        nargs=1, dest="domain")
    parser.add_argument("--zonetransfer", "-z", required=False,
                        action="store_true", default=False,
                        dest="zoneTransfer", 
                        help="Check the existence of exiZone Transfer.")
    parser.add_argument("--bruteforce", "-s",  required=False,
                        action="store_true", default=False, dest="subDomain",
                        help="for sub-domain bruteforce.")
    parser.add_argument("--level", "-l", required=False, dest="level",
                        type=int, default=1, help="the size of dict(level:1 2 3)")
    parser.add_argument("--debug", "-v", required=False,
                        action="store_true", default=False, dest="debugEnable",
                        help="print degug info.")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1")

    try:
        args = ''
        args = parser.parse_args(argv)
    except ArgumentError, e:
        raise e

    cmdLineArgument.domain = args.domain[0]
    if args.zoneTransfer:
        cmdLineArgument.zoneTransfer = 1
    if args.subDomain:
        cmdLineArgument.subDomain = True
    if args.level in [0, 1, 2, 3]:
        cmdLineArgument.level = args.level
    if args.debugEnable:
        cmdLineArgument.debugEnable = True
