from aq.token import AzureOAuth2Token
from aq.login import AzureGraphAPILogin

def run():
  login = AzureGraphAPILogin()
  print(f"Currently Logged in as {login.get_username()}")

if __name__ == '__main__':
    run()
