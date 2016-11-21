from xmlrpclib import ServerProxy

client_xml = ServerProxy('https://USER:PASSWORD@SERVER_XML-RPC_IP:TCP_PORT')
resp = client_xml.test()
print resp
