from aq.token import AzureOAuth2Token
from six.moves import BaseHTTPServer
import random, string
import urllib.parse
import os
import json

class AzureGraphAPILogin():
    # Graph API Client ID
    PROD_AZURE_CLIENTID = "de8bc8b5-d9f9-48b1-a8ad-b748da725064"
    
    # OAuth Token Endpoint
    BASE_OAUTH_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    
    # These are the default scopes used by the online Graph API explorer 
    # https://developer.microsoft.com/en-us/graph/graph-explorer
    OAUTH_SCOPES = [
      "openid",
      "profile",
      "User.ReadWrite",
      "User.ReadBasic.All",
      "Sites.ReadWrite.All",
      "Contacts.ReadWrite",
      "People.Read",
      "Notes.ReadWrite.All",
      "Tasks.ReadWrite",
      "Mail.ReadWrite",
      "Files.ReadWrite.All",
      "Calendars.ReadWrite"
    ]

    token = None

    def __init__(self):
        self.token = AzureOAuth2Token()
        if not self.token.valid():
            self.token = AzureOAuth2Token(self.do_web_login())
            self.token.cache_token()

    def get_username(self):
        return self.token.decoded_token['upn']

    def do_web_login(self):
        try:
            request_state = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(20))
        except NotImplementedError:
            request_state = 'code'
        url_arguments = {
          "nonce": "graph_explorer",
          "response_mode": "fragment",
          "prompt": "select_account",
          "mkt": "en-US",
          "client_id": AzureGraphAPILogin.PROD_AZURE_CLIENTID,
          "response_type": "token",
          "redirect_uri": "http://localhost:8400",
          "state": request_state,
          "scope": " ".join(AzureGraphAPILogin.OAUTH_SCOPES)
        }

        url_arg_string = urllib.parse.urlencode(url_arguments, quote_via=urllib.parse.quote)
        full_url = "%s?%s" % (AzureGraphAPILogin.BASE_OAUTH_URL, url_arg_string)
        
        web_server = ClientRedirectServer(('localhost', 8400), ClientRedirectHandler)
    
        import subprocess
    
        value = subprocess.Popen(['open', full_url])
    
        while True:
            web_server.handle_request()
            if 'error' in web_server.query_params or b'token' in web_server.query_params:
                break
    
        if 'error' in web_server.query_params:
            logger.warning('Authentication Error: "%s". Description: "%s" ', web_server.query_params['error'],
                           web_server.query_params.get('error_description'))
    
        access_token = web_server.query_params[b'token'][0].decode('utf-8')

        return access_token




class ClientRedirectServer(BaseHTTPServer.HTTPServer):  # pylint: disable=too-few-public-methods
    query_params = {}

class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # pylint: disable=line-too-long
    token = ''

    def do_POST(self):
        try:
            from urllib.parse import parse_qs
        except ImportError:
            from urlparse import parse_qs  # pylint: disable=import-error

        response = {"status": "success"}
        try:
            data = self.rfile.read(int(self.headers['Content-Length']))
            query = parse_qs(data)
            self.server.query_params = query
            self.token = query[b'token'][0].decode('utf-8')
        except:
            response = {"status": "fail"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

        self.server.query_params = query

    def do_GET(self):
        try:
            from urllib.parse import parse_qs
        except ImportError:
            from urlparse import parse_qs  # pylint: disable=import-error

        if self.path.endswith('/favicon.ico'):  # deal with legacy IE
            self.send_response(204)
            return

        landing_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'auth_landing_pages', 'handle-response.html')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(landing_file, 'rb') as html_file:
           self.wfile.write(html_file.read())
        return
          
    def log_message(self, format, *args):  # pylint: disable=redefined-builtin,unused-argument,no-self-use
        pass  # this prevent http server from dumping messages to stdout