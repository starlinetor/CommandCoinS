import click
from Commands.Tester import tester

@click.group()
def main():
    """Personal finance tracker"""
    pass

main.add_command(tester)

if __name__ == "__main__":
    main()