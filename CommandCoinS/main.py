import click
from Commands import Tester as c_tester
from Commands import Setup as c_setup
from Commands import Wallets as c_wallets
from Commands import Accounts as c_accounts
from Commands import Tags as c_tags
from Commands import Expenses as c_expenses

#create main group
@click.group()
def main() -> None:
    """Personal finance tracker"""
    pass

#add all commands
main.add_command(c_tester.tester)
main.add_command(c_setup.setup)
main.add_command(c_wallets.wallets)
main.add_command(c_accounts.accounts)
main.add_command(c_tags.tags)
main.add_command(c_expenses.expenses)

if __name__ == "__main__":
    main()