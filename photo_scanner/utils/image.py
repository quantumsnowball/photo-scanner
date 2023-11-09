from pathlib import Path
from PIL import Image
from typing import Literal
import cv2
import numpy as np
import photo_scanner.utils.message as msg
from photo_scanner.utils import highest_filename


ImageFormats = Literal['jpg', 'png']


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
        filename = Path(f'{highest+i+1}.{ext}')
        image.save(filename, quality=quality)
        msg.success(f'Saved: {filename}')


def show_image(image: Image.Image,
               *,
               name: str = 'Image',
               x: int = 100,
               y: int = 100,
               width: int = 1024,
               height: int = 768,) -> None:
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(name, x, y)
    cv2.resizeWindow(name, width, height)
    cv2.imshow(name, cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
