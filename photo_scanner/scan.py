from pathlib import Path
import subprocess
from typing import Any
import click
from photo_scanner.constants import DETAIL_PROFILE, FAST_PROFILE, NAPS2_EXE
from photo_scanner.crop import preview_crop, read_image
from photo_scanner.utils import read_cropping_config_yaml


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


def quick_preview(detail: bool, **kwargs: Any) -> None:
    # as Path
    file = Path(PREVIEW_FILENAME)
    # scan with corresponding profile to .preview.jpg
    profile = FAST_PROFILE if not detail else DETAIL_PROFILE
    click.secho(f'Preview using profile `{profile}`', fg='yellow')
    naps2(file, profile=profile, **kwargs)
    # preview file should have been saved to disk
    try:
        # read the image
        image = read_image(file)
        # apply the crop region to the image
        crop_locs = read_cropping_config_yaml('config.yaml', high_dpi=detail)
        preview_crop(image, crop_locs)
        # delete the temp file
        file.unlink()
    except FileNotFoundError:
        click.secho(f"Preview file doesn't exist", fg='red')


def scan(output: Path | str,
         **kwargs: Any) -> None:
    return naps2(output, profile=DETAIL_PROFILE, **kwargs)


if __name__ == '__main__':
    pass
