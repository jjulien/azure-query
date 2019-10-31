import os
import json
import base64
import requests
import jwt
import time
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate

class AzureOAuth2Token():

    CACHED_DIRECTORY = '.aq'
    CACHED_TOKEN_FILENAME = 'token'
    CACHED_JWKS_FILENAME = "jwks"

    def __init__(self, raw_token=None):
        if raw_token == None:
            self.raw_token = self.get_cached_token()
        else:
            self.raw_token = raw_token

        if self.valid():
            self.decoded_token = self.decode_token()

    def valid(self):
        if not self.raw_token:
            return False
        return True

    def get_headers_from_raw(self, raw_token):
        return json.loads(base64.b64decode(raw_token.split('.')[0]))

    def get_cache_dir(self):
        return os.path.join(os.environ["HOME"], AzureOAuth2Token.CACHED_DIRECTORY)

    def get_cached_token_filename(self):
        return os.path.join(self.get_cache_dir(), AzureOAuth2Token.CACHED_TOKEN_FILENAME)
    
    def get_cached_jwks_filename(self):
        return os.path.join(self.get_cache_diur(), CACHED_JWKS_FILENAME)
    
    def setup_cache(self):
        cache_dir = self.get_cache_dir()
        if not os.path.isdir(cache_dir):
            os.mkdir(cache_dir, mode=0o700)

    def get_jwk_with_id(self, jwks_id):
        jwks_url = 'https://login.microsoftonline.com/common/discovery/keys'
        response = requests.get(jwks_url)
        json_response = json.loads(response.text)
        for k in json_response['keys']:
            if k["kid"] == jwks_id:
                return k

    def get_cached_token(self, leeway=60):
        cached_token_filename = self.get_cached_token_filename()
        if os.path.exists(cached_token_filename):
            with open(cached_token_filename, 'r') as token_file:
                cached_token = token_file.read()
                decoded_token = self.decode_token(cached_token)
                expires = decoded_token['exp']
                # Do not return an expired cached token
                if expires - leeway - int(time.time()) <= 0:
                    return False
                return cached_token
        return False
    
    def cache_token(self):
        with open(self.get_cached_token_filename(), 'w') as token_file:
            token_file.write(self.raw_token)

    def decode_token(self, raw_token=None):
        if not raw_token:
            raw_token = self.raw_token
        headers = self.get_headers_from_raw(raw_token)
        options = {
            "verify_signature": False,
            "verify_exp": False,
            "verify_nbf": False,
            "verify_iat": False,
            "verify_aud": False,
            "verify_iss": False,
            "require_exp": False,
            "require_iat": False,
            "require_nbf": False,
        }
        k = self.get_jwk_with_id(headers['kid'])
        cert_str = f"-----BEGIN CERTIFICATE-----\n{k['x5c'][0]}\n-----END CERTIFICATE-----\n".encode('utf-8')
        cert_obj = load_pem_x509_certificate(cert_str, default_backend())
        decoded_key = jwt.decode(raw_token, cert_obj.public_key(), verify=False, algorithms=[headers['alg']], options=options)
        return decoded_key

    
    