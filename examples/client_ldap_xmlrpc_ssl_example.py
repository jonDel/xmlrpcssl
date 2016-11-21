from xmlrpclib import ServerProxy
import ssl

client_xml = ServerProxy('https://USER:PASSWORD@SERVER_XML-RPC_IP:TCP_PORT',
                         context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
resp = client_xml.test()
print resp
