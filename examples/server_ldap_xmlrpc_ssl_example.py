from xmlrpcssl import SecureAuthenticatedXMLRPCServer
from xmlrpcssl.handlers import LdapVerifyingRequestHandler
from datetime import datetime
keySsl='/tmp/server.key'
crtSsl='/tmp/server.crt'

optArgs={'isMasterUser':False,'baseUsrLoginDn':'o=FILL,c=FILL','ldapServer':'ldap ip or name','gidNumber':'user must be in this group to be authenticated','baseSearchDn':'o=FILL,c=FILL', 'host':'user must have access to this host in ldap','RequestHandler':LdapVerifyingRequestHandler}

serverSSL = SecureAuthenticatedXMLRPCServer(("server ip",int("server tcp port")),keySsl,crtSsl, **optArgs)
def test():
    # toy test function
    return datetime.now().strftime("%H:%M:%S")

serverSSL.register_function(test)
serverSSL.serve_forever()


