from pathlib import Path
from typing import Literal
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


def read_cropping_config_yaml(path: Path) -> CropLocation:
    with open(path) as file:
        values = yaml.safe_load(file)
        crop_config = CropLocation(**values)
        breakpoint()
        return crop_config


if __name__ == '__main__':
    read_cropping_config_yaml(Path('config.yaml'))
