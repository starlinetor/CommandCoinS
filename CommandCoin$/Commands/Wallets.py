import click
from pathlib import Path

@click.group()
def wallets() -> None:
    """
    Used to track expenses and earings\n
    Each wallet requires a parent Account\n
    Multiple wallets can be used to divide your money\n
    """
    pass

@wallets.command()
def create() -> None:
    "WIP"
    pass