from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np


def read_image_array(name: Path,
                     rotation: int = 270) -> Image.Image:
    image = Image.open(name)
    rotated = image.rotate(rotation, expand=True)
    return rotated


def preview_crop(image) -> None:
    draw = ImageDraw.Draw(image)
    image.show()


if __name__ == '__main__':
    # read the raw image
    raw = read_image_array(Path('.lab/raw.jpg'))
    # read the user coordinate and width height info
    preview_crop(raw)
    # import matplotlib.pyplot as plt
    # plt.imshow(np.array(raw))
    # plt.show()
    breakpoint()
    # display the preview of the crop
    # crop and save the photos
