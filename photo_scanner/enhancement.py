from pathlib import Path
from PIL import Image
import PIL.ImageOps as ops
from photo_scanner.utils.image import read_image, show_image
import numpy as np


def auto_contrast(image: Image.Image) -> Image.Image:
    return ops.autocontrast(image)


def show_diff(original: Path | str, target: Path | str) -> None:
    # read both images
    original_image = read_image(original, rotation=0)
    target_image = read_image(target, rotation=0)
    # calc diff
    diff = np.array(target_image) - np.array(original_image)
    # display
    show_image(diff)
