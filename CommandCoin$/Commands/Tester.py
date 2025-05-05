import click

@click.group()
def tester() -> None:
    """Testing and debug"""
    pass

@tester.command()
def print_test() -> None:
    """Print to screen test"""
    string =[
    ""
    r"_________                                           .____________        .__         ____/\__ ",
    r"\_   ___ \  ____   _____   _____ _____    ____    __| _/\_   ___ \  ____ |__| ____  /   / /_/ ",
    r"/    \  \/ /  _ \ /     \ /     \\__  \  /    \  / __ | /    \  \/ /  _ \|  |/    \ \__/ / \  ",
    r"\     \___(  <_> )  Y Y  \  Y Y  \/ __ \|   |  \/ /_/ | \     \___(  <_> )  |   |  \/ / /   \ ",
    r" \______  /\____/|__|_|  /__|_|  (____  /___|  /\____ |  \______  /\____/|__|___|  /_/ /__  / ",
    r"    \/             \/      \/     \/     \/      \/         \/               \/  \/   \/      ",
    ""]
    
    click.echo("\n".join(string))
    click.echo("Font credits : https://github.com/Marak/asciimo/blob/master/fonts/Graffiti.flf")