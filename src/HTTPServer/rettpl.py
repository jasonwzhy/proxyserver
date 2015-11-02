#! usr/bin/python
# -*- coding:utf-8 -*-
"""
	return json template
"""
import json

"""
#protocol 0-HTTP 1-HTTPS
#location 0-china 1-foreign
"""

class ResponseTpl():
	"""
		Err Code:
		0:	ok
		-1:	not fount
	"""
	def __init__(self,params={}):
		self._response_data = {"err_code":0,"msg":"ok","params":params,"rdata":[],"total":0}
		#GetIPData
		# self._getip_data = {"ip":"","port":0,"protocol":0}
	
	def loadrdata(self,rdata=[]):
		self._response_data["rdata"] = rdata
		self._response_data["total"] = len(self._response_data["rdata"])
		return json.dumps(self._response_data)
	def not_fount(self):
		self._response_data["err_code"] = -1
		self._response_data["msg"] = "Not Fount Resource."
		return json.dumps(self._response_data)