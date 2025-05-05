import click
from Commands.Tester import tester
from Commands.Setup import setup

#create main group
@click.group()
def main() -> None:
    """Personal finance tracker"""
    pass

#add all commands
main.add_command(tester)
main.add_command(setup)

if __name__ == "__main__":
    main()