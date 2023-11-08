from pathlib import Path
from typing import Any, Literal, get_type_hints
from PIL import Image
from dataclasses import dataclass
import yaml


def save_images(images: list[Image.Image],
                *,
                outdir: Path,
                prefix: str = 'IMG',
                ext: Literal['jpg', 'png'] = 'jpg') -> None:
    for i, image in enumerate(images):
        image.save(outdir / f'{prefix}_{i}.{ext}')


@dataclass
class CropLocation:
    x: int
    y: int
    width: int
    height: int


CropLocations = list[CropLocation]


def read_cropping_config_yaml(path: Path | str) -> CropLocations:
    # as Path
    path = Path(path) if isinstance(path, str) else path
    # read yaml file
    with open(path) as file:
        # parse
        locs: list[dict[str, int]] = yaml.safe_load(file)
        # return as CropLocations
        crop_config = [CropLocation(**loc) for loc in locs]
        return crop_config


if __name__ == '__main__':
    read_cropping_config_yaml(Path('config.yaml'))
