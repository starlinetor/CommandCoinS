import click
from pathlib import Path

settings_dir : str = Path(__file__).parents[2] / "settings.db"

@click.group()
def wallet() -> None:
    """
    Handle your virtual wallets.
    Virtual wallets divide your money for different pourpose 
    """
    pass

