#! /usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

# from data import kb
from data import conf
from data import kb
from cymruwhois import Client
# import whois
# import os
# import sys
import dns.resolver
import dns.zone
import dns.query
import dns.name


class Checker(object):
	"""
		the Checker
	"""
	def __init__(self):
		self.NSs = []
		self.MXs = []
		self.Zone = []
		self.domain = conf.domain.strip()
		self.Name = dns.name.from_text(self.domain)
		self.subDomain = []
		self.zone = {}
		self.flag = 0
		self.resolver = dns.resolver.Resolver()
		self.resolver.nameservers = conf.nameservers
		self.client = Client()
		self.req = None
	
	def TXTChecker():
		"""
		"""
		pass

	def mxChecker(self):
		"""
		"""
		try:
			print "=====Mail Exchanger====="
			answer = dns.resolver.query(self.domain)
			for rdata in answer:
				self.MXs.append(rdata)
				print "mail exchanger: ", rdata.exchange, "preference: ", rdata.preference
		except:
			pass

	def nsResolver(self):
		"""
		#name = dns.name.from_text(domain)
		"""
		nameservers = []
		try:
			answer = dns.resolver.query(self.domain, 'NS')
			for rdata in answer:
				if rdata is None or rdata == "":
					continue
				self.NSs.append(str(rdata)[:-1])
				nameservers.append(str(rdata)[:-1])
				print "==============================="
				print "nameserver:" + str(rdata)[:-1]
				print "==============================="
			# if len(nameservers):
				# 错了应该存的是IP
			# self.resolver.nameservers = []
			# self.resolver.nameservers = nameservers
		except dns.resolver.NXDOMAIN:
			print "nsResolver,error\n"
			pass
		except dns.resolver.NoAnswer:
			print "nsResolver,error\n"
			pass
		except dns.resolver.Timeout:
			print "nsResolver,error\n"
			pass

	def AXFRChecker(self):
		"""
		pass
		"""
		for ns in self.NSs:
			try:
				axfrGen = dns.query.xfr(ns, self.domain, rdtype=252, lifetime=5)
				try:
					zoneObj = dns.zone.from_xfr(axfrGen)
					if zoneObj is None:
							continue
					for name, node in zoneObj.items():
						rdatasets = node.rdatasets
						for rdataset in rdatasets:
							if rdataset.rdtype not in conf.rdtyps:
								continue
							for rdata in rdataset:
								self.subDomain.append([name, rdata])
								self.flag = 1
				except Exception, e:
					print e
			except Exception, e:
				print "AXFRChecker\n"
				print e

	def IXFRChecker(self):
		"""
		"""
		for ns in self.NSs:
			try:
				ixfrGen = dns.query.xfr(ns, self.domain, rdtype=251, lifetime=5)
				try:
					zoneObj = dns.zone.from_xfr(ixfrGen)
					if zoneObj is None:
							continue
					for name, node in zoneObj.items():
						rdatasets = node.rdatasets
						for rdataset in rdatasets:
							if rdataset.rdtype not in conf.rdtyps:
								continue
							for rdata in rdataset:
								self.subDomain.append([name, rdata])
								self.flag = 1
				except Exception, e:
					print e
			except Exception, e:
				print "IXFRChecker\n"
				print e

	def domainQuery(self, domain):
		"""
		应该讲查询和存储分离开，实现domain查询函数的公用
		"""
		domain = domain.strip()
		# print domain
		try:
			answer = self.resolver.query(domain)
			for rrset in answer.response.answer:
				for rdata in rrset:
					if rdata is None:
						continue
						# print "None"
					if rdata.rdtype == conf.A:
						kb.subDomains.append([answer.qname.to_text()[:-1], rdata.address])
						# print answer.qname[:-1]
						# print rdata.address
					elif rdata.rdtype == conf.CNAME:
						kb.subDomains.append([answer.qname.to_text()[:-1], rdata.target])
						conf.dict.append(answer.qname.to_text()[:-1])
						# print answer.qname[:-1]
					else:
						pass
		except dns.resolver.NXDOMAIN:
			# print "NXDOMAIN"
			pass
		except dns.resolver.NoAnswer:
			# print "NoAnswer."
			pass
		except dns.resolver.Timeout:
			# print "Timeout."
			pass
	
	def wildcardDNSChecker():
    		pass
"""
	def ipWhoisChecker(self):
		req = self.client.lookup(conf.ip)

    	kb.asn = req.asn
    	kb.owner = req.owner

	def domainWhoisChecker(self):
		pass
    
	def whoisChecker(self):
		pass
"""

checker = Checker()