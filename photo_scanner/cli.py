from pathlib import Path
import click
from photo_scanner.crop import crop_images
from photo_scanner.scan import quick_preview, scan
from photo_scanner.utils import CROP_CONFIG_PATH, Profile, read_crop_config, read_image, save_images


RAW_FILE = Path('.raw.jpg')


@click.group(invoke_without_command=True)
@click.option('-p', '--profile', default='middle', help='choose the dpi level')
@click.option('-qt', '--quality', default=85, help='image quality level')
@click.pass_context
def photo_scanner(ctx: click.Context, profile: Profile, quality: int) -> None:
    # ignore subcommand call
    if ctx.invoked_subcommand is not None:
        return

    # scan the raw source
    scan(RAW_FILE, profile=profile, verbose=False)
    # read the raw image
    raw_image = read_image(RAW_FILE)
    # crop the images
    crop_locs = read_crop_config(profile)
    cropped_images = crop_images(raw_image, crop_locs)
    # apply post processing enhancement
    # write images to disk
    save_images(cropped_images, quality=quality)
    # delete the raw image
    RAW_FILE.unlink()


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
