from pathlib import Path
from typing import Literal
from PIL import Image
from dataclasses import dataclass
import yaml


def save_images(images: list[Image.Image],
                *,
                outdir: Path | str,
                prefix: str = 'IMG',
                ext: Literal['jpg', 'png'] = 'jpg') -> None:
    # as Path
    outdir = Path(outdir) if isinstance(outdir, str) else outdir
    # save
    for i, image in enumerate(images):
        image.save(outdir / f'{prefix}_{i}.{ext}')


@dataclass
class CropLocation:
    x: int
    y: int
    width: int
    height: int
    high_dpi: bool

    def __post_init__(self):
        if self.high_dpi:
            self.x *= 4
            self.y *= 4
            self.width *= 4
            self.height *= 4

    @property
    def x_(self):
        return self.x+self.width

    @property
    def y_(self):
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


CropLocations = list[CropLocation]


def read_cropping_config_yaml(path: Path | str, high_dpi: bool = False) -> CropLocations:
    # as Path
    path = Path(path) if isinstance(path, str) else path
    # read yaml file
    with open(path) as file:
        # parse
        locs: list[dict[str, int]] = yaml.safe_load(file)
        # return as CropLocations
        crop_config = [CropLocation(high_dpi=high_dpi, **loc) for loc in locs]
        return crop_config


if __name__ == '__main__':
    info = read_cropping_config_yaml(Path('config.yaml'), high_dpi=True)
    print(info)
