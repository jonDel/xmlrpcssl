xmlrpcssl
=========

**xmlprcssl** is a Python library that provides secure communication (`TLS <https://en.wikipedia.org/wiki/Transport_Layer_Security>`__) beetween clients and servers through xmlrpc protocol. It supports plugable handlers to provide user authentication. For now, it has as an example a ldap based authentication handler.


Server configuration
--------------------

.. code:: python

  >>> from xmlrpcssl import SecureAuthenticatedXMLRPCServer
  >>> from xmlrpcssl.handlers import LdapVerifyingRequestHandler
  >>> from datetime import datetime
  >>> keySsl='/tmp/server.key'
  >>> crtSsl='/tmp/server.crt'
  >>> tcpPort=433
  >>> serverIp='10.0.0.1'
  >>> ldapHost = 'ldapHost' # User must have access granted to this host in ldap
  >>> ldapServer = 'ldapServer' # ip or name of ldap server
  >>> gidNumber = 111 # User must be in this group in order to be authenticated
  >>> isMasterUser = False # True if the user has write permissions in the ldap server
  >>> baseUsrLoginDn = 'o=Organization,c=US' # user base DN to perform login in the ldap server
  >>> baseSearchDn = 'o=Organization,c=US' # search base DN to perform a search in the ldap server base
  >>> RequestHandler = LdapVerifyingRequestHandler # a handler that inherits from BaseRequestHandler and performs user authentication
  >>> optArgs={'isMasterUser':isMasterUser,'baseUsrLoginDn':baseUsrLoginDn,
  ...  'ldapServer':ldapServer,'gidNumber':gidNumber,'baseSearchDn':baseSearchDn,
  ...  'host':ldapHost,'RequestHandler':RequestHandler}
  >>> serverSSL = SecureAuthenticatedXMLRPCServer((serverIp,tcpPort),keySsl,crtSsl, **optArgs)
  >>> def test():
  ...  # toy test function
  ...  return datetime.now().strftime("%H:%M:%S")
  >>> serverSSL.register_function(test)
  >>> serverSSL.serve_forever()


Client configuration
--------------------

.. code:: python

  >>> from xmlrpclib import ServerProxy
  >>> userName = 'ldapUser'
  >>> password = 'ldapUserPassword'
  >>> tcpPort=433
  >>> serverIp='10.0.0.1'
  >>> clientXml = ServerProxy('https://'+userName+':'+password+'@'+serverIp+':'+str(tcpPort))
  >>> response = clientXml.test()
  >>> print response

Installation
------------

To install xmlrpcssl, simply run:

::

  $ pip install xmlrpcssl

xmlrpcssl is compatible with Python 2.6+

Documentation
-------------

https://xmlrpcssl.readthedocs.io/en/latest/

PS: still being developed.


Source Code
-----------

Feel free to fork, evaluate and contribute to this project.

Source: https://github.com/jonDel/xmlrpcssl/

License
-------

GPLv3 licensed.

Credits
-------

-  http://code.activestate.com/recipes/496786-simple-xml-rpc-server-over-https and
   https://github.com/nosmo/python-xmlrpcssl for inspiration
