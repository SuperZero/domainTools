#! /usr/bin/env python
# -*- coding: utf-8 -*-
# auth:hugo

# from data import kb
from data import conf
from data import kb
from cymruwhois import Client
from common import randStr
from common import printOut
# import whois
# import os
# import sys
import requests
from bs4 import BeautifulSoup
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
		# self.req = None
	
	def TXTChecker():
		"""
		"""
		pass

	def mxChecker(self):
		"""
		"""
		try:
			printOut("=====Mail Exchanger=====", conf.info)
			answer = dns.resolver.query(self.domain)
			for rdata in answer:
				self.MXs.append(rdata)
				printOut ("mail exchanger: " + rdata.exchange + "preference: " + rdata.preference, conf.info)
		except:
			pass

	def nsResolver(self):
		"""
		#name = dns.name.from_text(domain)
		"""
		try:
			answer = dns.resolver.query(self.domain, 'NS')
			for rdata in answer:
				if rdata is None or rdata == "":
					continue
				self.NSs.append(str(rdata)[:-1])
				# nameservers.append(str(rdata)[:-1])
		except dns.resolver.NXDOMAIN:
			# print "nsResolver,error\n"
			pass
		except dns.resolver.NoAnswer:
			# print "nsResolver,error\n"
			pass
		except dns.resolver.Timeout:
			# print "nsResolver,error\n"
			pass

	def nsReplace(self):
		try:
			if len(self.NSs) > 0:
				answer = self.domainQuery(self.NSs[0])
				for rrset in answer.response.answer:
						for rdata in rrset:
							if rdata is None:
								continue
								# print "None"
							self.resolver.nameservers = []
							self.resolver.nameservers = [str(rdata.address)]
		except:
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
					printOut(e, conf.error)
			except Exception, e:
				# print "AXFRChecker\n"
				printOut(e, conf.error)

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
					printOut(e, conf.error)
			except Exception, e:
				# print "IXFRChecker\n"
				printOut(e, conf.error)

	def domainQuery(self, domain, rdtype=1, rdclass=1):
		"""
		"""
		try:
			answer = self.resolver.query(domain, rdtype, rdclass)
			return answer
		except dns.resolver.NXDOMAIN:
			# print "NXDOMAIN"
			pass
		except dns.resolver.NoAnswer:
			# print "NoAnswer."
			pass
		except dns.resolver.Timeout:
			# print "Timeout."
			pass
			
	def subDomainChecker(self, domain):
		"""
		"""
		# print domain
		try:
			answer = self.domainQuery(domain)
			# printOut(threading.current_thread(), conf.debug)
			for rrset in answer.response.answer:
				for rdata in rrset:
					if rdata is None:
						continue
						# print "None"
					if rdata.rdtype == conf.A:
						kb.subDomains.append([answer.qname.to_text()[:-1], rdata.address])
						printOut(answer.qname.to_text()[:-1] + "==>" + rdata.address, conf.info)
						# print answer.qname[:-1]
						# print rdata.address
					elif rdata.rdtype == conf.CNAME:
						kb.subDomains.append([answer.qname.to_text()[:-1], rdata.target])
						conf.dict.append(answer.qname.to_text()[:-1])
						printOut(answer.qname.to_text()[:-1] + "==>" + rdata.target, conf.info)
						# print answer.qname[:-1]
					else:
						pass
		except KeyboardInterrupt:
			printOut("Stop", conf.debug)
		except Exception:
			pass
		 
	def wildcardDNSChecker(self):
		answer1 = self.domainQuery(randStr() + conf.domain, rdtype=1, rdclass=1)
		answer2 = self.domainQuery(randStr() + conf.domain, rdtype=1, rdclass=1)
		def getaddress(answer):
			for rrset in answer.response.answer:
				for rdata in rrset:
					if rdata is None:
						continue
					if rdata.rdtype == conf.A:
						return rdata.address
		if getaddress(answer1) == getaddress(answer2):
    			printOut("WildCard DNS Record Found.\n", conf.info)

	def whoisChecker(self):
    		"""
			another API: https://www.whois.com/whois/baidu.com, need https
			no support of edu domian.
			"""
		chinaz = 'http://whois.chinaz.com/'+str(self.domain)
		r = requests.get(url=chinaz)
		
		if r.status_code != 200:
			print "查询失败"
		bs = BeautifulSoup(r.text, "html.parser")
		
		def NoResult(input):
			result = bs.find("div", text=input)
			if result is None:
				return "None"
			else:
				return result.find_next_siblings()[0].span.string.encode('gb18030')

		printOut("-----Whois info-----", conf.info)
		printOut("Registrar:\t\t" + NoResult("注册商") , conf.info)
		printOut("Contact:\t\t" + NoResult("联系人") , conf.info)
		printOut("Phone:\t\t" + NoResult("联系电话") , conf.info)
		printOut("Updated Date:\t\t" + NoResult("更新时间") , conf.info)
		printOut("Creation Date:\t" + NoResult("创建时间") , conf.info)
		printOut("Expiration Date:\t" + NoResult("过期时间") , conf.info)
		printOut("Company Name:\t" + NoResult("公司") , conf.info)
		# printOut("Registrar: " + NoResult("注册商") , conf.info)
		printOut("-------------------", conf.info)

"""
	def ipWhoisChecker(self):
		req = self.client.lookup(conf.ip)

    	kb.asn = req.asn
    	kb.owner = req.owner

	def domainWhoisChecker(self):
		pass
"""

checker = Checker()