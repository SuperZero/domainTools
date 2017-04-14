#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

# import whois
from data import kb
from cymruwhois import Client


def ipWhoisChecker(ip):
    c = Client()
    r = c.lookup(ip)

    kb.asn = r.asn
    kb.owner = r.owner


def domainWhoisChecker():
    pass


def whoisChecker():
    pass