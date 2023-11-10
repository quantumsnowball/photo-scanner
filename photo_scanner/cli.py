from pathlib import Path
import click
from photo_scanner.crop import crop_images
from photo_scanner.enhancement import apply_autocontrast, apply_equalize, show_diff
from photo_scanner.scan import NAPS2_EXE, quick_preview, scan
from photo_scanner.utils import Profile
from photo_scanner.utils.config import LAYOUT_CONFIG_PATH, read_crop_config
from photo_scanner.utils.image import read_image, save_images
import photo_scanner.utils.message as msg


RAW_FILE = Path('.raw.jpg')


@click.group(invoke_without_command=True)
@click.option('-p', '--profile', default='middle', help='choose the dpi level')
@click.option('-qt', '--quality', default=85, help='image quality level')
@click.option('--autocontrast', default=False, is_flag=True, help='autocontrast enhancement')
@click.option('--equalize', default=False, is_flag=True, help='equalize enhancement')
@click.pass_context
def photo_scanner(ctx: click.Context,
                  profile: Profile,
                  quality: int,
                  autocontrast: bool,
                  equalize: bool) -> None:
    # always welcome the user
    msg.welcome()

    # ignore subcommand call
    if ctx.invoked_subcommand is not None:
        return

    while (True):
        # prompt
        if msg.prompt_default_accept(click.style('Continue to scan and crop?')):
            break
        # ensure config is valid
        crop_locs = read_crop_config(profile)
        # preview loop
        while (True):
            # prompt
            if msg.prompt_default_reject(click.style('Preview crop area?')):
                break
            # preview
            quick_preview(profile='lowest', verbose=False)
        # scan the raw source
        scan(RAW_FILE, profile=profile, verbose=False)
        # read the raw image
        raw_image = read_image(RAW_FILE)
        # crop the images
        images = crop_images(raw_image, crop_locs)
        # apply post processing enhancement
        if autocontrast:
            images = [apply_autocontrast(im) for im in images]
            msg.info('Autocontrast: ON')
        if equalize:
            images = [apply_equalize(im) for im in images]
            msg.info('Equalize: ON')
        # write images to disk
        save_images(images, quality=quality)
        # delete the raw image
        RAW_FILE.unlink()


@photo_scanner.command()
@click.option('-p', '--profile', default='lowest', help='choose the dpi level')
def preview(profile: Profile) -> None:
    while (True):
        # prompt
        if msg.prompt_default_accept(click.style('Continue preview?', fg='cyan')):
            break
        # preview
        quick_preview(profile, verbose=False)
        #
        msg.success(f'Preview displayed Successfully')


@photo_scanner.command()
@click.argument('original', nargs=1)
@click.argument('target', nargs=1)
def diff(original: str, target: str) -> None:
    # show diff
    show_diff(original, target)


@photo_scanner.command()
def check() -> None:
    # check naps2 exe
    if Path(NAPS2_EXE).exists():
        msg.success(f'NAPS2 executible exists: {NAPS2_EXE}')
    else:
        msg.failure(f'NAPS2 executible not found')
    # check config yaml
    if Path(LAYOUT_CONFIG_PATH).exists():
        msg.success(f'Layout config file exists: {LAYOUT_CONFIG_PATH}')
    else:
        msg.failure(f'Layout config file not found')
