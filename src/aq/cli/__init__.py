from aq.login import AzureGraphAPILogin
import importlib
import sys


def run():
    if len(sys.argv) < 2:
        command_name = "help"
    else:
        command_name = sys.argv[1]

    try:
        command_module = importlib.import_module(f"aq.cli.commands.{command_name}")
        if command_name == 'help':
            login = None
        else:
            login = AzureGraphAPILogin()
        command = command_module.Command(command_name, login)
    except ModuleNotFoundError:
        command_module = importlib.import_module(f"aq.cli.commands.help")
        command = command_module.Command("help", None)
        sys.stderr.write(f"\nERROR: The command \"{command_name}\" was not found\n")
        sys.stderr.flush()
        command.run()
        sys.exit(1)
    command.run()


if __name__ == '__main__':
    run()
