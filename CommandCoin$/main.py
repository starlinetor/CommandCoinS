import click
from Commands.Tester import tester
from Commands.Setup import setup
from Commands.Wallets import wallet
from Commands.Accounts import accounts

#create main group
@click.group()
def main() -> None:
    """Personal finance tracker"""
    pass

#add all commands
main.add_command(tester)
main.add_command(setup)
main.add_command(wallet)
main.add_command(accounts)

if __name__ == "__main__":
    main()