from pathlib import Path
from typing import Literal


Profile = Literal['low', 'middle', 'high']
ImageFormats = Literal['jpg', 'png']


def highest_filename(ext: ImageFormats) -> int:
    # find all image files in cwd
    cwd = Path().cwd()
    files = cwd.glob(f'*.{ext}')
    # find the highest number filename
    nums = [int(f.stem) for f in files if f.stem.isdigit()]
    if len(nums) == 0:
        return 0
    return max(nums)
