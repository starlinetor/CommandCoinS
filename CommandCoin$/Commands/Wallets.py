import click
from pathlib import Path

#settings location
settings_dir : str = Path(__file__).parents[2] / "data\\settings.db"

@click.group()
def wallet() -> None:
    """
    Used to track expenses and earings\n
    Each wallet requires a parent Account\n
    Multiple wallets can be used to divide your money\n
    """
    pass

@wallet.command()
def create() -> None:
    pass