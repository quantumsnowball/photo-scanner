from pathlib import Path
import click
from photo_scanner.scan import quick_preview, scan
from photo_scanner.utils import CROP_CONFIG_PATH, Profile


RAW_FILENAME = '.raw.jpg'


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-p', '--profile', default='middle', help='choose the dpi level')
def photo_scanner(ctx: click.Context, profile: Profile) -> None:
    # ignore subcommand call
    if ctx.invoked_subcommand is not None:
        return

    # scan the raw source
    raw = Path(RAW_FILENAME)
    scan(raw, profile=profile, verbose=False)
    # crop the images
    # apply post processing enhancement
    # determin the correct sequencial filenames
    # write images to disk


@photo_scanner.command()
@click.option('-p', '--profile', default='low', help='choose the dpi level')
def preview(profile: Profile) -> None:
    quick_preview(profile, verbose=False)


@photo_scanner.command()
def check() -> None:
    if Path(CROP_CONFIG_PATH).exists():
        click.secho(f'Crop config file exists: {CROP_CONFIG_PATH}', fg='green')
    else:
        click.secho(f'Crop config file not found', fg='red')
