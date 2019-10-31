from aq.token import AzureOAuth2Token
from aq.login import AzureGraphAPILogin
from aq.graphapi import AzureGraphAPI
import sys

def run():
  login = AzureGraphAPILogin()
  print(f"Currently Logged in as {login.get_username()}")
  api = AzureGraphAPI(login.token)
  print(api.get(sys.argv[1]))


if __name__ == '__main__':
    run()
