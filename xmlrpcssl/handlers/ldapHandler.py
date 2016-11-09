#!/usr/bin/env

import ldap
import xmlrpcssl
import httplib

class LdapVerifyingRequestHandler(xmlrpcssl.BaseRequestHandler):
	'''Ldap handler for xmlrpc client requests

		This Handler class provide methods to handle incoming xmlrpc
		requests from clients.

	'''

	def verifyUserCredentials(self):
		''' Verifies user ldap login and permissions

		Performs user authentication, by using the optional class object attributes,
		(self.optArgs) in a ldap server. The following conditions must be true in order
		to allow user access:
			1. User login (self.optArgs['username'] and self.optArgs['password'])
			2. User must belong to the configured access group(self.optArgs['gidNumber'])
			3. User must have access to the configured host(self.optArgs['host']), which is
			   primarily intended to be the host where the xmlrpcssl server is running

		'''
		if not self.optArgs['username'] or not self.optArgs['password']:
			return (False, 'Username or password not well formed', httplib.BAD_REQUEST)
		if self.optArgs['isMasterUser']:
			loginDn = 'uid=' + self.optArgs['username'] + ',' + self.optArgs['baseMasterLoginDn']
		else:
			loginDn = 'uid=' + self.optArgs['username'] + ',' + self.optArgs['baseUsrLoginDn']
		server = 'ldap://' + self.optArgs['ldapServer']
		connection = ldap.initialize(server)
		try:
			connection.simple_bind_s(loginDn, self.optArgs['password'])
		except Exception as error:
			return (False, 'Error authenticating ldap user ' + self.optArgs['username'] + ' in ldap server ' + self.optArgs['ldapServer'] + ': ' + str(error), httplib.INTERNAL_SERVER_ERROR)
		searchFilter = 'uid=' + str(self.optArgs['username'])
		userInfo = connection.search_ext_s(self.optArgs['baseSearchDn'], ldap.SCOPE_SUBTREE, searchFilter)
		if not (self.optArgs['host'] in userInfo[0][1]['host'] and self.optArgs['gidNumber'] == userInfo[0][1]['gidNumber'][0]):
			return (False, 'Error: ldap user ' + self.optArgs['username'] + ' has not the mandatory permissions to execute actions in host ' + self.optArgs['host'], httplib.FORBIDDEN)
		return (True, None, None)
