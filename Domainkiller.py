#! /usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

from cmdline import cmdLineParser
from options import initOptions
from options import mergeConfWithCmd
# from whoisChecker import whoisChecker
from threads import myThreadPool
from common import importDict
from data import kb
from data import conf


def run():
    """
    real worker
    """
    try:
        from checker import checker
    except Exception, e:
        print "aa"
        raise e
    
    try:
        # whoisChecker()
        checker.nsResolver()
        kb.NSs = checker.NSs
    except Exception, e:
        print "a"
        raise e

    if conf.zoneTransfer:
        try:
            checker.AXFRChecker()
            checker.IXFRChecker()
            kb.subDomain = checker.subDomain
            kb.flag = checker.flag
        except Exception, e:
            print "b"
            raise e

    if conf.subDomainEnable:
        try:
            importDict()
            myThreadPool(checker.domainQuery, conf.dict)
        except Exception, e:
            print "c"
            raise e
    
    if len(kb.subDomains) > 0:
        for item in kb.subDomains:
            print item[0], " : ", item[1]
    else:
        print "No SubDomains Found."


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
    main()

# impor 和初始化应该分离
