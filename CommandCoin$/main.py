import click
import Commands.Tester as tester
import Commands.Setup as setup
import Commands.Wallets as wallets
import Commands.Accounts as accounts

#create main group
@click.group()
def main() -> None:
    """Personal finance tracker"""
    pass

#add all commands
main.add_command(tester.tester)
main.add_command(setup.setup)
main.add_command(wallets.wallets)
main.add_command(accounts.accounts)

if __name__ == "__main__":
    main()