#!/usr/bin/env python
# -*- coding:utf-8 -*-
# auth: hugo @ 2016-11-29

from data import conf
from data import cmdLineArgument
from random import choice


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
    count = [conf.small, conf.large, conf.huge][conf.level-1]
    with open(conf.dictPath, "r") as dictFile:
        # 增添错误处理
        for item in dictFile:
            conf.dict.append(str(item).strip()+'.'+conf.domain)
            count = count - 1
            if count <= 0:
                break
        dictFile.close()


def randStr(length=conf.randStringLen):
    return "".join(choice(conf.alphabet) for _ in xrange(0, length))
