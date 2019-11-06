import requests
import json

class AzureGraphAPI():

    BASE_GRAPH_URL = 'https://graph.microsoft.com/v1.0'

    def __init__(self, token):
        self.token = token
    
    def get_headers(self):
        headers = {
            "Authorization": f"Bearer {self.token.raw_token}"
        }
        return headers
    
    def get(self, path, query_params={}):
        full_url = f"{AzureGraphAPI.BASE_GRAPH_URL}/{path}"
        response = requests.get(full_url, headers=self.get_headers(), params=query_params)
        return json.loads(response.text)
