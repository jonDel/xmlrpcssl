#!/usr/bin/env
'''Xmlrpc server with SSL and configurable authentication plugin method'''
from base64 import b64decode
import BaseHTTPServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler, SimpleXMLRPCDispatcher
import SocketServer
import socket
import ssl
import httplib

class SecureXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
    '''Provides a ssl secured handler class for xmlrpc requests

    '''

    def setup(self):
        '''Perform prior base class initializations

        '''
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def __init__(self, req, addr, server):
        SimpleXMLRPCRequestHandler.__init__(self, req, addr, server)

    def do_POST(self):
        '''Send POST responses with proper xml content

        '''
        try:
            data = self.rfile.read(int(self.headers["content-length"]))
            response = self.server._marshaled_dispatch(
                data,
                getattr(self, '_dispatch', None)
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
    '''Base Handler providing methods to handle xmlrpc incoming requests

    '''
    def parse_request(self):
        '''Parses incoming requests and perform user authentication

        '''
        if SimpleXMLRPCRequestHandler.parse_request(self):
            ret, error_msg, error_code = self.authenticate(self.headers)
            if ret:
                return True
            else:
                self.send_error(error_code, error_msg)
        return False

    def authenticate(self, headers):
        '''Performs user authentication

        Arguments:

            headers (:obj:`str`): http/https headers received from client

        Returns:
            ret (:obj:`bool`): True if user successfully authenticated, False otherwise
        Returns:
            error_msg (:obj:`str`): Error message if authentication failed, None otherwise
        Returns:
            error_code (:obj:`str`): Error code if authentication failed, None otherwise

        '''
        auth_header = headers.get('Authorization')
        if not auth_header:
            return False, 'No authentication header provided in https request field',\
                   httplib.UNAUTHORIZED
        (basic, _, encoded) = auth_header.partition(' ')
        assert basic == 'Basic', 'Only basic authentication supported'
        (username, _, password) = b64decode(encoded).partition(':')
        if (not username) or (not password):
            return False, 'Authentication field in https request not well formed',\
                   httplib.BAD_REQUEST
        self.opt_args.update({'username': username, 'password': password})
        ret, error_msg, error_code = self.verify_user_credentials()
        if ret:
            return True, None, None
        else:
            return False, error_msg, error_code

    def verify_user_credentials(self): # pylint: disable=no-self-use
        '''Verify the user credentials

        Returns:
            ret (:obj:`bool`): True if user successfully authenticated, False otherwise
        Returns:
            error_msg (:obj:`str`): Error message if authentication failed, None otherwise
        Returns:
            error_code (:obj:`str`): Error code if authentication failed, None otherwise

        OBS: Must be overwritten with a proper authentication method in the child class

        '''
        return False, 'Error: no method provided to verify user credentials', httplib.BAD_REQUEST


class SecureAuthenticatedXMLRPCServer(BaseHTTPServer.HTTPServer, SocketServer.BaseServer,
                                      SimpleXMLRPCDispatcher):
#class SecureAuthenticatedXMLRPCServer(SocketServer.BaseServer,
#                                      SimpleXMLRPCDispatcher):
    ''' Xmlrpc server secured with ssl

    Arguments:
        server_address(:obj:`str`): ip address of the xmlrpc server
        keyfile(:obj:`str`): path of the ssl/tls private keyfile generated for the xmlrpc server
        certfile(:obj:`str`): path of the ssl/tls certificate file signed by the Certification
            Authority
    Keyword Arguments:
        log_requests(:obj:`str`,optional, *default* =True): enable log all requests
        path(:obj:`str`,optional, *default* ='/'): server http path
        RequestHandler(:obj:`class`,optional, *default* =BaseRequestHandler): class to handle
            client requests
        ssl_version(:obj:`int`, optional, *default* = ssl.PROTOCOL_TLSv1 ): ssl protocol
            version code

    '''
    def __init__(self, server_address, keyfile, certfile, **kwargs): # pylint: disable=super-init-not-called
        default_args = {
            'log_requests': True,
            'path': "/",
            'RequestHandler': BaseRequestHandler,
            'ssl_version': ssl.PROTOCOL_TLSv1 # pylint: disable=no-member
            }
        default_args.update(kwargs)
        self.logRequests = default_args['log_requests'] # pylint: disable=invalid-name
        self.paths = default_args['path']
        default_args['RequestHandler'].opt_args = default_args
        try:
            SimpleXMLRPCDispatcher.__init__(self)
        except TypeError:
            # fix for python > 2.5
            SimpleXMLRPCDispatcher.__init__(self, False, None)
        SocketServer.BaseServer.opt_args = kwargs
        SocketServer.BaseServer.__init__(self, server_address, default_args['RequestHandler'])
        self.socket = ssl.wrap_socket(socket.socket(self.address_family, self.socket_type),
                                      server_side=True,
                                      certfile=certfile,
                                      keyfile=keyfile,
                                      ssl_version=default_args['ssl_version']
                                     )
        self.server_bind()
        self.server_activate()

