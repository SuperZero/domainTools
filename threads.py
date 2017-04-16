#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

# from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Pool
from data import conf


def myThreadPool(threadFucntion, dataList, numThread=None):
    if numThread is None:
        numThread = conf.numThread
    tpool = Pool(numThread)
    tpool.map(threadFucntion, dataList)
    # 增加终止条件
