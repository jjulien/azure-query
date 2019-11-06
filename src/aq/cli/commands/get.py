from aq.cli.commands import *
from aq.graphapi import AzureGraphAPI
import json


class Command(ODataAPICommand):

    description = "Executes HTTP GET functionality against the Microsoft Graph REST API"
    path = "/me"

    def run(self):
        api = AzureGraphAPI(self.login.token)
        response = api.get(self.path, query_params=self.query_params)
        print(json.dumps(response, indent=4))

    def parse_args(self):
        super().parse_args()
        self.sub_parser.add_argument("path", help="The path to do an HTTP GET on from https://graph.microsoft.com/v1.0.  "
                                             "Examples: /me, /users")
        parsed = self.parser.parse_args()
        self.path = parsed.path

    def display_extra_help(self):
        print("\nExample:")
        print(f"{self.parser.prog} get /me")



