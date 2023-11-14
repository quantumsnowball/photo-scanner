from pathlib import Path
from PIL import Image
from typing import Literal
import cv2
from cv2.typing import MatLike
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
    # detect highest filename
    highest = highest_filename(ext)
    # save each
    for i, image in enumerate(images):
        filename = Path(f'{highest+i+1}.{ext}')
        image.save(filename, quality=quality)
        msg.success(f'Saved: {filename}')


def show_image(image: Image.Image | MatLike,
               *,
               name: str = 'Image',
               x: int = 100,
               y: int = 100,
               width: int = 1024,
               height: int = 768,) -> None:
    # ensure nd array
    image = np.array(image) if isinstance(image, Image.Image) else image
    # display
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(name, x, y)
    cv2.resizeWindow(name, width, height)
    cv2.imshow(name, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    # wait for discard keypress
    cv2.waitKey(0)
    cv2.destroyAllWindows()
