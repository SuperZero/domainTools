#!/usr/bin/env python
# -*- coding:utf-8 -*-
# auth: hugo @ 2016-11-29

from data import conf
from data import cmdLineArgument
from random import choice
from termcolor import colored


def checkDomain(domain):
    """
    pass    
    """
# domain = kb.domain
    pass


def checkArgs():
    """
    pass
    """
    checkDomain(cmdLineArgument.domain)


def importDict():
    count = [conf.tiny, conf.small, conf.large, conf.huge][conf.level]
    with open(conf.dictPath, "r") as dictFile:
        # 增添错误处理
        for item in dictFile:
            conf.dict.append(str(item).strip()+'.'+conf.domain)
            count = count - 1
            if count <= 0:
                break
        dictFile.close()


def randStr(length=None):
    if length is None:
        length = int(conf.randStringLen)
    return "".join(choice(conf.alphabet) for _ in xrange(0, length))


def printOut(output, outlevel=None):
    if outlevel is None:
        outlevel = conf.info
    if (conf.debugEnable) and (outlevel == (conf.debug)):
        print colored("[-]"+str(output), 'blue')
    if outlevel == (conf.info):
        print colored("[+]"+str(output), 'green')
    if outlevel == (conf.warning):
        print colored("[-]"+str(output), 'red')
    if outlevel == (conf.error):
        print colored("[-]"+str(output), 'red')

