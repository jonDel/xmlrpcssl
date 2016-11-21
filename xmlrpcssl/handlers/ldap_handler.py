#!/usr/bin/env
'''Ldap handler module for xmlrpcssl client requests'''

import ldap
import httplib
import xmlrpcssl

class LdapVerifyingRequestHandler(xmlrpcssl.BaseRequestHandler):
    '''Ldap handler class for xmlrpcssl client requests

        This Handler class provide methods to handle incoming xmlrpc
        requests from clients.

    '''

    def verify_user_credentials(self):
        ''' Verifies user ldap login and permissions

        Performs user authentication, by using the optional class object attributes,
        (self.opt_args) in a ldap server. The following conditions must be true in order
        to allow user access:
            1. User login (self.opt_args['username'] and self.opt_args['password'])
            2. User must belong to the configured access group(self.opt_args['gidNumber'])
            3. User must have access to the configured host(self.opt_args['host']), which is
               primarily intended to be the host where the xmlrpcssl server is running

        '''
        if not self.opt_args['username'] or not self.opt_args['password']:
            return (False, 'Username or password not well formed', httplib.BAD_REQUEST)
        if self.opt_args['isMasterUser']:
            login_dn = 'uid=' + self.opt_args['username'] + ',' + self.opt_args['baseMasterLoginDn']
        else:
            login_dn = 'uid=' + self.opt_args['username'] + ',' + self.opt_args['baseUsrLoginDn']
        server = 'ldap://' + self.opt_args['ldapServer']
        connection = ldap.initialize(server)
        try:
            connection.simple_bind_s(login_dn, self.opt_args['password'])
        except Exception as error:
            return (False, 'Error authenticating ldap user ' + self.opt_args['username'] + \
                    ' in ldap server ' + self.opt_args['ldapServer'] + ': ' + str(error),
                    httplib.INTERNAL_SERVER_ERROR)
        search_filter = 'uid=' + str(self.opt_args['username'])
        user_info = connection.search_ext_s(self.opt_args['baseSearchDn'], ldap.SCOPE_SUBTREE,
                                          search_filter)
        if not (self.opt_args['host'] in user_info[0][1]['host'] and self.opt_args['gidNumber'] ==\
                user_info[0][1]['gidNumber'][0]):
            return (False, 'Error: ldap user ' + self.opt_args['username'] + ' has not the '
                    'mandatory permissions to execute actions in host ' + self.opt_args['host'],
                    httplib.FORBIDDEN)
        return (True, None, None)
