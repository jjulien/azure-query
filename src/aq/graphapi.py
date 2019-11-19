import requests
import json

class AzureGraphAPI():

    BASE_GRAPH_URL = 'https://graph.microsoft.com/v1.0'
    BETA_GRAPH_URL = 'https://graph.microsoft.com/beta'

    def __init__(self, token, beta=False):
        self.token = token
        if beta:
            self.base_url = AzureGraphAPI.BETA_GRAPH_URL
        else:
            self.base_url = AzureGraphAPI.BASE_GRAPH_URL

    def get_headers(self):
        headers = {
            "Authorization": f"Bearer {self.token.raw_token}"
        }
        return headers
    
    def get(self, path, query_params={}):
        full_url = f"{self.base_url}/{path}"
        response = requests.get(full_url, headers=self.get_headers(), params=query_params)
        return json.loads(response.text)
