#!/usr/bin/env
#coding: utf-8
from base64 import b64decode
import BaseHTTPServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler,SimpleXMLRPCDispatcher
import SocketServer
import socket
import ssl
import httplib

class SecureXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
	def setup(self):
		self.connection = self.request
		self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
		self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

	def __init__(self, req, addr, server):
		SimpleXMLRPCRequestHandler.__init__(self, req, addr, server)

	def do_POST(self):
		try:
			data = self.rfile.read(int(self.headers["content-length"]))
			response = self.server._marshaled_dispatch(
					data, getattr(self, '_dispatch', None)
				)
		except Exception, post_exception:
			self.send_response(httplib.INTERNAL_SERVER_ERROR)
			self.end_headers()
			raise post_exception
		else:
			self.send_response(httplib.OK)
			self.send_header("Content-type", "text/xml")
			self.send_header("Content-length", str(len(response)))
			self.end_headers()
			self.wfile.write(response)
			self.wfile.flush()


class BaseRequestHandler(SecureXMLRPCRequestHandler):
	def parse_request(self):
		if SimpleXMLRPCRequestHandler.parse_request(self):
			ret, errorMsg, errorCode = self.authenticate(self.headers)
			if ret:
				return True
			else:
				self.send_error(errorCode, errorMsg)
		return False

	def authenticate(self, headers):
		auth_header = headers.get('Authorization')
		if not auth_header:
			return False, 'No authentication header provided in https request field', httplib.UNAUTHORIZED
		(basic, _, encoded) = auth_header.partition(' ')
		assert basic == 'Basic', 'Only basic authentication supported'
		(username, _, password) = b64decode(encoded).partition(':')
		if (not username) or (not password):
			return False, 'Authentication field in https request not well formed',httplib.BAD_REQUEST
		self.optArgs.update({'username':username,'password':password})
		ret, errorMsg, errorCode =  self.verifyUserCredentials()
		if ret:
			return True, None, None
		else:
			return False, errorMsg, errorCode

	def verifyUserCredentials(self):
		'''
		Description: must be overwritten with a proper auth method
		'''
		return False, 'Error: no method provided to verify user credentials', httplib.BAD_REQUEST


class SecureAuthenticatedXMLRPCServer(BaseHTTPServer.HTTPServer,SimpleXMLRPCDispatcher):
	def __init__(self, server_address, keyfile, certfile,**kwargs):
		defaultArgs= {
			'logRequests':True,
			'path':"/",
			'RequestHandler':BaseRequestHandler,
			'ssl_version':ssl.PROTOCOL_TLSv1
		}
		defaultArgs.update(kwargs)
		self.logRequests = defaultArgs['logRequests']
		self.paths = defaultArgs['path']
		defaultArgs['RequestHandler'].optArgs = defaultArgs
		try:
			SimpleXMLRPCDispatcher.__init__(self)
		except TypeError:
			# fix for python > 2.5
			SimpleXMLRPCDispatcher.__init__(self, False, None)
		SocketServer.BaseServer.optArgs=kwargs
		SocketServer.BaseServer.__init__(self, server_address, defaultArgs['RequestHandler'])
		self.socket = ssl.wrap_socket(socket.socket(self.address_family,
			self.socket_type),
			server_side=True,
			certfile=certfile,
			keyfile=keyfile,
			ssl_version=defaultArgs['ssl_version']
		)
		self.server_bind()
		self.server_activate()


