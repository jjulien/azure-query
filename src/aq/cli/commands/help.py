import os
import re
import sys
import importlib

from aq.cli.commands import AQCommand


class Command(AQCommand):

    description = "Displays this help message"

    def run(self):
        print("\nAzure Query CLI\n")
        print("This tool provides an easy to use CLI implementation of the Microsoft Graph API REST interface")
        print(f"Usage: {os.path.basename(sys.argv[0])} [subcommand] [options]\n")
        print("List of Sub Commands:")
        sub_command_path = os.path.dirname(__file__)
        max_length = 0
        sub_commands = []
        for sub_command in os.listdir(sub_command_path):
            if re.match("^__.*", sub_command) or not re.match('.*\.py$', sub_command):
                continue
            else:
                sub_commands.append(sub_command[:-3])
                if len(sub_command) > max_length:
                    max_length = len(sub_command)
        for sub_command in sub_commands:
            command_module = importlib.import_module(f"aq.cli.commands.{sub_command}")
            description = command_module.Command.description
            print(f"{sub_command.rjust(max_length + 3, ' ')} : {description}")
