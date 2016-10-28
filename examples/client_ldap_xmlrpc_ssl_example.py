#!/usr/bin/env
#coding: utf-8
from xmlrpclib import ServerProxy

clientXml = ServerProxy('https://USER:PASSWORD@SERVER_XML-RPC_IP:TCP_PORT')
resp = clientXml.test()
print resp
