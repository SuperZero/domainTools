#! /usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

from cmdline import cmdLineParser
from options import initOptions
from options import mergeConfWithCmd
# from whoisChecker import whoisChecker
from threads import myThreadPool
from common import importDict
from common import printOut
from data import kb
from data import conf
import time


def run():
    """
    real worker
    """
    try:
        from checker import checker
    except Exception, e:
        printOut("aa", conf.debug)
        raise e
    
    try:
        # whoisChecker()
        checker.nsResolver()
        kb.NSs = checker.NSs
        printOut("-----Nameservers:-----", conf.info)
        for item in kb.NSs:
            printOut("    "+item, conf.info)
        printOut("----------------------", conf.info)
        # checker.nsReplace() useless
    except Exception, e:
        raise e

    if conf.zoneTransfer:
        try:
            checker.AXFRChecker()
            checker.IXFRChecker()
            kb.subDomain = checker.subDomain
            kb.flag = checker.flag
        except Exception, e:
            raise e

    if conf.subDomainEnable:
        try:
            importDict()
            myThreadPool(checker.subDomainChecker, conf.dict)
        except Exception, e:
            raise e
    
    # if len(kb.subDomains) > 0:
    #    for item in kb.subDomains:
    #        print item[0], " : ", item[1]
    # else:
    #    print "No SubDomains Found."


def main():
    """
        the entry of program
    """
    try:
        initOptions()
    except Exception, e:
        raise e
   
    try:
        cmdLineParser()
    except Exception, e:
        raise e

    try:
        mergeConfWithCmd()
    except Exception, e:
        raise e
    # checkArgs(cmdLineArgument)
    try:
        run()
    except Exception, e:
        raise e


if __name__ == "__main__":
    start = time.clock()
    main()
    end = time.clock()
    printOut("Time: %f s" % (end - start), conf.info)

