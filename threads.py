#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

# from multiprocessing.dummy import Pool as ThreadPool
import signal
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from data import conf
from time import sleep
from common import printOut


def myThreadPool(threadFucntion, dataList, numThread=None):
    if numThread is None:
        numThread = conf.numThread
    printOut(cpu_count(), conf.debug)
    sleep(10)
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGINT, original_sigint_handler)
    tpool = Pool(numThread)
    try:
        tpool.map_async(threadFucntion, dataList, 200).get(9999)
        printOut("running...", conf.debug)
    except KeyboardInterrupt:
        tpool.terminate()
        printOut("tpool stopped!", conf.debug)
    else:
        tpool.close()
