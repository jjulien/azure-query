import argparse


class AQCLIException(Exception):
    pass


class AQCommand:
    description = "This command has no specific description"

    def __init__(self, name, login):
        if not name:
            raise AQCLIException("You must pass a name when creating an application")
        self.name = name
        self.login = login
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help=self.description)
        self.sub_parser = subparsers.add_parser(name)
        self.parse_args()

    # This method should be used if your application requires any arg parsing
    def parse_args(self):
        pass

    def display_extra_help(self):
        pass

    def display_help(self):
        self.parser.print_help()
        self.display_extra_help()

    def run(self):
        raise AQCLIException(f"No run method was found for application {self.name}")


class ODataAPICommand(AQCommand):
    query_params = {}

    # OData Query Options Described Here
    # https://docs.microsoft.com/en-us/graph/query-parameters#odata-system-query-options
    odata_query_options = ['count', 'expand', 'filter', 'format', 'orderby', 'search', 'select', 'skip', 'top']

    def __init__(self, name, login):
        super().__init__(name, login)
        self.add_odata_query_params()

    def parse_args(self):
        self.sub_parser.add_argument("--count", help="Retrieves the total count of matching resources.\nDetails: "
                                                     "https://docs.microsoft.com/en-us/graph/query-parameters#count-parameter")
        self.sub_parser.add_argument("--expand", help="Retrieves related resources.\nDetails: "
                                                      "https://docs.microsoft.com/en-us/graph/query-parameters#expand-parameter")
        self.sub_parser.add_argument("--filter", help="Filters results (rows).\nDetails: "
                                                      "https://docs.microsoft.com/en-us/graph/query-parameters#filter-parameter")
        self.sub_parser.add_argument("--format", help="Returns the results in the specified media format.\nDetails: "
                                                      "https://docs.microsoft.com/en-us/graph/query-parameters#format-parameter")
        self.sub_parser.add_argument("--orderby", help="Orders results.\nDetails: "
                                                       "https://docs.microsoft.com/en-us/graph/query-parameters#orderby-parameter")
        self.sub_parser.add_argument("--search", help="Returns results based on search criteria. Currently supported "
                                                      "on messages and person collections."
                                                      "https://docs.microsoft.com/en-us/graph/query-parameters#search-parameter")
        self.sub_parser.add_argument("--select", help="Filters properties (columns).\nDetails: "
                                                      "https://docs.microsoft.com/en-us/graph/query-parameters#select-parameter")
        self.sub_parser.add_argument("--skip", help="Indexes into a result set. Also used by some APIs to implement "
                                                    "paging and can be used together with $top to manually page "
                                                    "results.\nDetails: "
                                                    "https://docs.microsoft.com/en-us/graph/query-parameters#skip-parameter")
        self.sub_parser.add_argument("--top", help="Sets the page size of results.\nDetails: "
                                                   "https://docs.microsoft.com/en-us/graph/query-parameters#top-parameter")


    def add_odata_query_params(self):
        parsed = vars(self.parser.parse_args())
        for option in self.odata_query_options:
            if option in parsed.keys():
                # The v1 endpoint still requires some options to be prefixed with $, so prepending this to be safe
                self.query_params[f'${option}'] = parsed[option]
