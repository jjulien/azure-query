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

