from pathlib import Path
import click
from photo_scanner.scan import quick_preview, scan


RAW_FILENAME = '.raw.jpg'


@click.group(invoke_without_command=True)
@click.pass_context
def photo_scanner(ctx: click.Context) -> None:
    # ignore subcommand call
    if ctx.invoked_subcommand is not None:
        return

    # default operations
    raw = Path(RAW_FILENAME)
    scan(raw, verbose=False)


@photo_scanner.command()
def preview() -> None:
    quick_preview(progress=False, verbose=False)
