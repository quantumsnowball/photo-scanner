import click
from photo_scanner.constants import FAST_PROFILE
from photo_scanner.scan import quick_preview


@click.group(invoke_without_command=True)
@click.pass_context
def photo_scanner(ctx: click.Context) -> None:
    # ignore subcommand call
    if ctx.invoked_subcommand is not None:
        return

    # default operations
    click.echo(f'`photo-scanner` is called')


@photo_scanner.command()
def preview() -> None:
    quick_preview(progress=False, verbose=False)
