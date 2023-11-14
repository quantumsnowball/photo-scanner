from pathlib import Path
import subprocess
from typing import Any
from photo_scanner.crop import preview_crop
from photo_scanner.utils import Layout, Profile
from photo_scanner.utils.config import read_layout_config
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
    output = str(output) if isinstance(output, Path) else output
    # cmd
    cmd = [NAPS2_EXE, '-o', output, '-p', profile, ]
    # flags
    if progress:
        cmd.append('--progress')
    if verbose:
        cmd.append('--verbose')
    if force:
        cmd.append('--force')

    # run
    _ = subprocess.run(cmd)


def quick_preview(layout: Layout, profile: Profile, **kwargs: Any) -> None:
    # as Path
    file = Path(PREVIEW_FILENAME)

    # scan with corresponding profile to .preview.jpg
    msg.info(f'Preview using layout `{layout}` and profile `{profile}`')
    naps2(file, profile=profile, **kwargs)

    # preview file should have been saved to disk
    try:
        try:
            # read layout
            rotation, crop_locs = read_layout_config(layout, profile)
        except FileNotFoundError:
            msg.failure(f"Crop config file not found")
            return

        # read the image
        image = read_image(file, rotation)

        # apply the crop region to the image
        preview_crop(image, crop_locs)
        # delete the temp file
        file.unlink()
    except FileNotFoundError:
        msg.failure(f"Preview file doesn't exist")


def scan(output: Path | str,
         profile: Profile,
         **kwargs: Any) -> None:
    msg.info(f'Scanning using profile `{profile}`')
    naps2(output, profile=profile, **kwargs)
