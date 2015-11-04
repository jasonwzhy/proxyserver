#! usr/bin/python
# -*- coding:utf-8 -*-
#__author__ = 'Jasonwzhy@gmail.com'


from twisted.internet import reactor,ssl
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from twisted.enterprise import adbapi
from twisted.internet.task import deferLater

from twisted.web.server import NOT_DONE_YET

import sqlite3
from rettpl import ResponseTpl

from datetime import datetime


class DBHandle():
	"""
	connect db handle
	"""
	def condb(self):
		conn = sqlite3.connect('../db/ProxyIPs.db')
		if conn:			
			print "The db connect success:"
		# pass
		return conn
	def condb_adbapi(self):
		connadbapi = adbapi.ConnectionPool("sqlite3",database="../db/ProxyIPs.db")
		return connadbapi
	def reconnect(self):
		pass
		
class GetIp(Resource):
	"""
	Get Ips
	The Url like:http://x.x.x.x/getip/?live=0&count=199&location=0&protocol=0
	@params live:	0- Not alive proxyip 
					1- Alive Ip when checkeddt(checked datetime)
	@params	count:	Get ips count
	@params	location:	0-china 1-foreign
	@params	protocol:	0-HTTP 1-HTTPS
	"""
	def __init__(self):
		Resource.__init__(self)
		self.MAXCOUNT = 1000

	def getChild(self,name,request):
		if name == "":
			return self
		return NotFount()

	def queryip(self,args,request):

		def _get_query(args):
			count = args["count"][0] if "count" in args and args["count"][0].isdigit() and int(args["count"][0])<=self.MAXCOUNT else 1
			#count need less 1000			

			live = args["live"][0] if "live" in args else 1
			location = args["location"][0] if "location" in args else 0
			protocol = args["protocol"][0] if "protocol" in args else 0

			querystr = "select * from ProxyIP where live=%s and location=%s and protocol=%s limit %s" % (live,location,protocol,count)

			return dbhandle.runQuery(querystr)

		_get_query(args).addCallback(lambda x: self._render_result(request,x))
	

	def _render_result(self,request,result):
		res = ResponseTpl(request.args).loadrdata([{"ip":r[1],"port":r[2],"protocol":r[3],"location":r[4],"live":r[6],"checkeddt":r[7],"checkcount":r[9]} for r in result])
		request.write(res)
		request.finish()
		
	def render_GET(self,request):
		self.queryip(request.args,request)
		return NOT_DONE_YET

class Verify(Resource):
	"""
	The Verify APP
	The Url like: http://x.x.x.x/verify/ or
				  https://x.x.x.x/verify/
	For Verify The Ip, Should get ips from proxyserver first than set client ProxyHandler and send request with proxy ip .(If visit the https set ssl._create_unverified_context first)
	"""
	def getChild(self,name,request):
		if name == "":
			return self
		else:
			return NotFount()
		return Resource.getChild(self,name,request)

	def printverify(self,request):
		"""
		# FOR TEST
		"""
		print 'printverify',request.client.port
		
		if HTTPPORT == request.getHost().port:
			print "This is HTTP request"
		elif HTTPSPORT == request.getHost().port:
			print "This is HTTPS request"

	def verify(self,request):
		"""
		Get the ip from request and verify proxy IPs in the DB
		"""
		cip = request.client.host
		# cport = request.client.port
		protocol = 0

		if HTTPPORT == request.getHost().port:
			protocol = HTTP
		elif HTTPSPORT == request.getHost().port:
			protocol = HTTPS

		isexist_query = 'select * from ProxyIP where proxyip="%s" and protocol=%s'%(cip,protocol)

		def _render_verify(result):
			request.write(ResponseTpl({"ClientIP":cip}).verify_success())
			request.finish()

		def _do_verifycheck(result):
			if result:
				pid = result[0][0]
				checkcount = result[0][9]
				
				update_query = "update ProxyIP set live=1,checkeddt=datetime('now', 'localtime'),checkedts = strftime('%%s','now'),checkcount=%s where id=%s"%(1+checkcount,pid)

				dbhandle.runQuery(update_query).addCallback(_render_verify)
			else:
				request.write(ResponseTpl({"ClientIP":cip}).verify_failed())
				request.finish()

		dbhandle.runQuery(isexist_query).addCallback(_do_verifycheck)

	def render_GET(self,request):
		# self.printverify(request)
		self.verify(request)
		return NOT_DONE_YET

class PutIp(Resource):
	"""
	The Put APP
	The Url like:http://x.x.x.x/putip?proxyip=127.0.0.1&port=1234&protocol=0&location=0&description=desc
	"""
	def render_GET(self,request):
		pass
	
	def putip(self,request):
		pass
		def _do_put():
			pass
		def _check():
			pass

	def getChild(self,name,request):
		pass

class NotFount(Resource):
	def getChild(self,name,request):
		return self
	def render_GET(self,request):
		return ResponseTpl().not_fount()


class ServerHandle(Resource):
	"""
	ServerHandle 
	Render The server request and get root APPs
	"""
	def getChild(self,name,request):
		if name == '':
			return self
		elif name == 'verify':
			return Verify()
		elif name == 'getip':
			return GetIp()
		else:
			return NotFount()
		return Resource.getChild(self,name,request)
	def render_GET(self,request):
		return "<h1>Welcome server!<h1>"

# class Item(Resource):
# 	def getChild(self,name,request):
# 		global lcount
# 		lcount += 1
# 		print "request count",lcount
# 		print "In Item",dir(self)
# 		print "self",self.render_HEAD
# 		print "getHost",request.host
# 		print "get item id is:",name
# 		print "request is:",request.args
# 		print "Client IP is:",request.getClientIP()
# 		if name =='':
# 			return ItemErr()
# 		if name.isdigit():
# 			return ItemInfo(int(name))
# class ItemInfo(Resource):
# 	def __init__(self,id):
# 		Resource.__init__(self)
# 		self.id = id
# 	def render_GET(self,request):
# 		return "<html><h3>The Item id is: %s</h3></html>"%self.id

# class ItemErr(Resource):
# 	def render_GET(self,request):
# 		return "<html>Get Item ID Error</html>"

global dbhandle

dbhandle = DBHandle().condb_adbapi()

global HTTPPORT
global HTTPSPORT
global HTTP
global HTTPS

HTTPPORT = 8000
HTTPSPORT = 443
HTTP = 0
HTTPS = 1


root = ServerHandle()

# root2 = SSLServerHandle()
# root.putChild('item',Item())
# root2.putChild('item',Item())
# sslfactory = Site(root2)

factory = Site(root)

reactor.listenTCP(HTTPPORT,factory)
sslContext = ssl.DefaultOpenSSLContextFactory(
		'/tmp/privkey.pem',
		'/tmp/cacert.pem'
	)
reactor.listenSSL(HTTPSPORT,factory,contextFactory = sslContext)
reactor.run()