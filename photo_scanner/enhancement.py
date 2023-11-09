from pathlib import Path
from PIL import Image
import PIL.ImageOps as ops
from photo_scanner.utils.image import read_image, show_image
import numpy as np


def apply_autocontrast(image: Image.Image) -> Image.Image:
    '''
    PIL.ImageOps.autocontrast(image, cutoff=0, ignore=None, mask=None, preserve_tone=False)[source]
    Maximize (normalize) image contrast. This function calculates a histogram of the input image (or mask region), removes cutoff percent of the lightest and darkest pixels from the histogram, and remaps the image so that the darkest pixel becomes black (0), and the lightest becomes white (255).

    PARAMETERS:
    image – The image to process.

    cutoff – The percent to cut off from the histogram on the low and high ends. Either a tuple of (low, high), or a single number for both.

    ignore – The background pixel value (use None for no background).

    mask – Histogram used in contrast operation is computed using pixels within the mask. If no mask is given the entire image is used for histogram computation.

    preserve_tone –

    Preserve image tone in Photoshop-like style autocontrast.

    New in version 8.2.0.

    RETURNS:
    An image.0
    '''
    return ops.autocontrast(image)


def apply_equalize(image: Image.Image) -> Image.Image:
    '''
    PIL.ImageOps.equalize(image, mask=None)[source]
    Equalize the image histogram. This function applies a non-linear mapping to the input image, in order to create a uniform distribution of grayscale values in the output image.

    PARAMETERS:
    image – The image to equalize.

    mask – An optional mask. If given, only the pixels selected by the mask are included in the analysis.

    RETURNS:
    An image.
    '''
    return ops.equalize(image)


def show_diff(original: Path | str, target: Path | str) -> None:
    # read both images
    original_image = read_image(original, rotation=0)
    target_image = read_image(target, rotation=0)
    # calc diff
    diff = np.array(target_image) - np.array(original_image)
    # display
    show_image(diff)
