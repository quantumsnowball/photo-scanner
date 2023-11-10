from pathlib import Path
import subprocess
from typing import Any
import click
from photo_scanner.crop import preview_crop
from photo_scanner.utils import Profile
from photo_scanner.utils.config import read_crop_config
from photo_scanner.utils.image import read_image
import photo_scanner.utils.message as msg


NAPS2_EXE = r'/mnt/c/Program Files/NAPS2/NAPS2.Console.exe'
PREVIEW_FILENAME = '.preview.jpg'


def naps2(output: Path | str,
          *,
          profile: str,
          progress: bool = True,
          verbose: bool = True,
          force: bool = True) -> None:
    '''
    scan using NAPS2 console executable
    '''
    # as Path
    output = Path(output) if isinstance(output, str) else output
    # cmd
    cmd = [NAPS2_EXE, '-o', output, '-p', profile, ]
    if progress:
        cmd.append('--progress')
    if verbose:
        cmd.append('--verbose')
    if force:
        cmd.append('--force')

    # run
    _ = subprocess.run(cmd)


def quick_preview(profile: Profile, **kwargs: Any) -> None:
    # as Path
    file = Path(PREVIEW_FILENAME)

    # scan with corresponding profile to .preview.jpg
    msg.info(f'Preview using profile `{profile}`')
    naps2(file, profile=profile, **kwargs)

    # preview file should have been saved to disk
    try:
        # read the image
        image = read_image(file)

        # apply the crop region to the image
        try:
            crop_locs = read_crop_config(profile=profile)
            preview_crop(image, crop_locs)
        except FileNotFoundError:
            click.secho(f"Crop config file not found", fg='red')

        # delete the temp file
        file.unlink()
        print('deleted')
    except FileNotFoundError:
        click.secho(f"Preview file doesn't exist", fg='red')


def scan(output: Path | str,
         profile: Profile,
         **kwargs: Any) -> None:
    msg.info(f'Scanning using profile `{profile}`')
    naps2(output, profile=profile, **kwargs)
