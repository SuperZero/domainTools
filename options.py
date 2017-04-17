#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

from data import conf
from data import kb
from data import cmdLineArgument


def mergeConfWithCmd():
    conf.domain = cmdLineArgument.domain
    conf.zoneTransfer = cmdLineArgument.zoneTransfer
    conf.subDomainEnable = cmdLineArgument.subDomain
    conf.level = cmdLineArgument.level
    conf.debugEnable = cmdLineArgument.debugEnable


def _setConfAttributes():
    """
        ref: http://blog.csdn.net/guaguastd/article/details/40616155
        1. Check whether a string looks like a valid domain name  
        (?i)^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$  
        
        2. Find valid domain names in longer text  
        (?i)\b([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\b  
        
        3. Check whether each part of the domain is not longer than 63 characters
        (?i)\b((?=[a-z0-9-]{1,63}\.)[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b  
        
        4. Allow internationalized domain names using the punycode notation  
        (?i)\b((xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\b  
        
        5. Check whetehr each part of the domain is not longer than 63 characters,
        and allow internationalized domain names using the punycode notation  
        (?i)\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b
        http://stackoverflow.com/questions/2894902/check-for-a-valid-domain-name-in-a-string
        r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*'
    """
    conf.A = 1
    conf.CNAME = 8
    conf.nameservers = ["223.5.5.5", "223.6.6.6", "114.114.114.114"]
    # conf.rdtyps = ([dns.rdtypes.ANY.CNAME, dns.rdtypes.ANY.NS,
    #                dns.rdtypes.ANY.MX, dns.rdtypes.IN.A,
    #                dns.rdtypes.ANY.TXT, dns.rdtypes.IN.AAAA])
    conf.numThread = 5
    conf.debugEnable = False
    conf.info = 0
    conf.debug = 1
    conf.warning = 2
    conf.error = 3
    conf.dict = []
    conf.tiny = 20  # used for testing
    conf.small = 2000
    conf.large = 10000
    conf.huge = 100000
    conf.levle = 1
    conf.dictPath = "./txt/bitquark_subdomains_top100K.txt"
    conf.subDomains = []
    conf.randStringLen = 6
    conf.alphabet = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    conf.syntaxReg = r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*'
    conf.syntaxReg1 = r'(?i)^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
    conf.syntaxReg2 = r'(?i)\b([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\b'
    conf.syntaxReg3 = r'(?i)\b((?=[a-z0-9-]{1,63}\.)[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b'


def _setKnowledgeBaseAttributes():
    kb.domain = None
    kb.NSs = []
    kb.MXs = []
    kb.Zone = []
    kb.subDomains = []
    kb.zone = None
    kb.flag = 0


def _setCmdlineAttributes():
    cmdLineArgument.domain = None
    cmdLineArgument.zoneTransfer = None
    cmdLineArgument.subDomain = None
    cmdLineArgument.level = 1
    cmdLineArgument.debugEnable = False


def initOptions():
    """
        initialize Options
    """
    _setConfAttributes()
    _setKnowledgeBaseAttributes()
    _setCmdlineAttributes()
