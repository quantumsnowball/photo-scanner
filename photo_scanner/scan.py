from pathlib import Path
import subprocess
from typing import Any

from photo_scanner.constants import DEFAULT_PROFILE, FAST_PROFILE, NAPS2_EXE
from photo_scanner.crop import read_image


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


def quick_preview(**kwargs: Any) -> None:
    file = Path(PREVIEW_FILENAME)
    # scan with fast profile to .preview.jpg
    naps2(file, profile=FAST_PROFILE, **kwargs)
    # display the image
    image = read_image(file)
    image.show('Quick Preview')
    # delete the temp file
    if file.exists():
        file.unlink()


def scan(output: str,
         **kwargs: Any) -> None:
    return naps2(output, profile=DEFAULT_PROFILE, **kwargs)


if __name__ == '__main__':
    pass
