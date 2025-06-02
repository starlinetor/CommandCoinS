import click
from pathlib import Path

#settings location
settings_dir : str = Path(__file__).parents[2] / "data\\settings.db"

@click.group()
def accounts() -> None:
    """
    Rappresentation of one of your bank accounts\n
    Holds information, settings and automations\n
    You can create a wallets to track expenses\n
    """
    pass

@accounts.command()
def create() -> None:
    "WIP"
    pass