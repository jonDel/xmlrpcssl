.. image:: https://readthedocs.org/projects/xmlrpcssl/badge/?version=latest
   :target: http://xmlrpcssl.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/jonDel/xmlrpcssl/badge.svg?branch=master
   :target: https://coveralls.io/github/jonDel/xmlrpcssl?branch=master

.. image:: https://landscape.io/github/jonDel/xmlrpcssl/master/landscape.svg?style=flat
    :target: https://landscape.io/github/jonDel/xmlrpcssl/master
    :alt: Code Health

.. image:: https://www.versioneye.com/user/projects/58233fdf613b6800422cb9b6/badge.svg?style=flat
    :target: https://www.versioneye.com/user/projects/58233fdf613b6800422cb9b6


xmlrpcssl
=========

**xmlprcssl** is a Python library that provides secure communication \
(`TLS <https://en.wikipedia.org/wiki/Transport_Layer_Security>`__) beetween clients and servers \
through xmlrpc protocol. It supports plugable handlers to provide user authentication. For now, \
it has as an example a ldap based authentication handler.


Server configuration
--------------------

.. code:: python

  >>> from xmlrpcssl import SecureAuthenticatedXMLRPCServer
  >>> from xmlrpcssl.handlers import LdapVerifyingRequestHandler
  >>> from datetime import datetime
  >>> KEY_SSL = '/tmp/server.key'
  >>> CRT_SSL = '/tmp/server.crt'
  >>> TCP_PORT = 433
  >>> SERVER_IP = '10.0.0.1'
  >>> LDAP_HOST = 'ldapHost' # User must have access granted to this host in ldap
  >>> LDAP_SERVER = 'ldapServer' # ip or name of ldap server
  >>> GIDNUMBER = 111 # User must be in this group in order to be authenticated
  >>> IS_MASTER_USER = False # True if the user has write permissions in the ldap server
  >>> BASE_USR_LOGIN_DN = 'o=Organization,c=US' # user base DN to perform login in
   # the ldap server
  >>> BASE_SEARCH_DN = 'o=Organization,c=US' # search base DN to perform a search in
   # the ldap server base
  >>> RequestHandler = LdapVerifyingRequestHandler # a handler that inherits from
   # BaseRequestHandler and performs user authentication
  >>> OPT_ARGS = {'isMasterUser': IS_MASTER_USER, 'baseUsrLoginDn': BASE_USR_LOGIN_DN,
  ...  'ldapServer': LDAP_SERVER, 'gidNumber': GIDNUMBER, 'baseSearchDn': BASE_SEARCH_DN,
  ...  'host': LDAP_HOST, 'RequestHandler': RequestHandler}
  >>> server_ssl = SecureAuthenticatedXMLRPCServer((SERVER_IP, TCP_PORT), KEY_SSL,CRT_SSL,
  ...  **OPT_ARGS)
  >>> def test():
  ...  # toy test function
  ...  return datetime.now().strftime("%H:%M:%S")
  >>> server_ssl.register_function(test)
  >>> server_ssl.serve_forever()


Client configuration
--------------------

.. code:: python

  >>> import ssl
  >>> from xmlrpclib import ServerProxy
  >>> USERNAME = 'ldapUser'
  >>> PASSWORD = 'ldapUserPassword'
  >>> TCP_PORT = 433
  >>> SERVER_IP = '10.0.0.1'
  >>> client_xml = ServerProxy('https://'+USERNAME+':'+PASSWORD+'@'+SERVER_IP+':'+str(TCP_PORT),
      context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
  >>> response = client_xml.test()
  >>> print·response


Installation
------------

To install xmlrpcssl, simply run:

::

  $ pip install xmlrpcssl

xmlrpcssl is compatible with Python 2.6+

Documentation
-------------

https://xmlrpcssl.readthedocs.io

Source Code
-----------

Feel free to fork, evaluate and contribute to this project.

Source: https://github.com/jonDel/xmlrpcssl

License
-------

GPLv3 licensed.

Credits
-------

Credits go to http://code.activestate.com/recipes/496786-simple-xml-rpc-server-over-https and \
https://github.com/nosmo/python-xmlrpcssl for inspiration.
