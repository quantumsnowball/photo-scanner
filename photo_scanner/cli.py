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

    # scan the raw source
    raw = Path(RAW_FILENAME)
    scan(raw, verbose=False)
    # crop the images
    # apply post processing enhancement
    # determin the correct sequencial filenames
    # write images to disk


@photo_scanner.command()
@click.option('--detail', default=False, is_flag=True, help='use high dpi to preview')
def preview(detail: bool) -> None:
    quick_preview(detail, verbose=False)
