from pathlib import Path
from typing import Literal
from PIL import Image
from dataclasses import dataclass
import yaml


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


def read_image(name: Path | str,
               rotation: int = 270) -> Image.Image:
    # as Path
    name = Path(name) if isinstance(name, str) else name
    # open
    image = Image.open(name)
    # rotate the image
    rotated = image.rotate(rotation, expand=True)
    #
    return rotated


def save_images(images: list[Image.Image],
                *,
                quality: int = 85,
                ext: ImageFormats = 'jpg') -> None:
    # save
    highest = highest_filename(ext)
    for i, image in enumerate(images):
        image.save(Path(f'{highest+i+1}.{ext}'), quality=quality)


Profile = Literal['low', 'middle', 'high']


@dataclass
class CropLocation:
    x: int
    y: int
    width: int
    height: int
    profile: Profile

    def __post_init__(self):
        # scale the factor according to profile
        self.x *= self.factor
        self.y *= self.factor
        self.width *= self.factor
        self.height *= self.factor

    @property
    def factor(self) -> int:
        return {'low': 1, 'middle': 2, 'high': 4}[self.profile]

    @property
    def x_(self) -> int:
        return self.x+self.width

    @property
    def y_(self) -> int:
        return self.y+self.height

    @property
    def top(self):
        return ((self.x, self.y), (self.x_, self.y))

    @property
    def bottom(self):
        return ((self.x, self.y_), (self.x_, self.y_))

    @property
    def left(self):
        return ((self.x, self.y), (self.x, self.y_))

    @property
    def right(self):
        return ((self.x_, self.y), (self.x_, self.y_))

    @property
    def line_width(self) -> int:
        return 5 * self.factor


CropLocations = list[CropLocation]
CROP_CONFIG_PATH = Path.home() / '.config/photo-scanner/crop.yaml'


def read_crop_config(profile: Profile = 'low') -> CropLocations:
    # read yaml file
    with open(CROP_CONFIG_PATH) as file:
        # parse
        locs: list[dict[str, int]] = yaml.safe_load(file)
        # return as CropLocations
        crop_config = [CropLocation(profile=profile, **loc) for loc in locs]
        return crop_config
