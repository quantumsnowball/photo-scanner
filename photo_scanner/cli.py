import click


@click.group()
def photo_scanner() -> None:
    pass


@click.command
def scan() -> None:
    print('hello click photo-scanner')


photo_scanner.add_command(scan)
