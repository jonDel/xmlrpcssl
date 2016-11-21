'''Example for configuring a xmlrpcssl server with built-in ldap handler'''
from datetime import datetime
from xmlrpcssl import SecureAuthenticatedXMLRPCServer
from xmlrpcssl.handlers import LdapVerifyingRequestHandler

KEY_SSL = '/tmp/server.key'
CRT_SSL = '/tmp/server.crt'

OPT_ARGS = {'isMasterUser': False, 'baseUsrLoginDn': 'o=FILL,c=FILL',
            'ldapServer': 'ldap ip or name',
            'gidNumber': 'user must be in this group to be authenticated',
            'baseSearchDn': 'o=FILL,c=FILL',
            'host': 'user must have access to this host in ldap',
            'RequestHandler':LdapVerifyingRequestHandler}

server_ssl = SecureAuthenticatedXMLRPCServer(("server ip", int("server tcp port")),
                                             KEY_SSL, CRT_SSL, **OPT_ARGS)
def test():
    '''Toy test function'''
    return datetime.now().strftime("%H:%M:%S")

server_ssl.register_function(test)
server_ssl.serve_forever()


