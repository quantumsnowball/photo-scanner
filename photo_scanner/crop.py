import numpy as np
from PIL import Image, ImageDraw
import cv2
from photo_scanner.utils import CropLocations


def preview_crop(image: Image.Image,
                 crop_locs: CropLocations) -> None:
    # Draw the line on the image
    preview = image.copy()
    draw = ImageDraw.Draw(preview)
    for l in crop_locs:
        draw.line(l.top, fill='red', width=l.line_width)
        draw.line(l.bottom, fill='red', width=l.line_width)
        draw.line(l.left, fill='green', width=l.line_width)
        draw.line(l.right, fill='green', width=l.line_width)

    # show
    # bug: window not showing if main program still running
    # preview.show()
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image', 1024, 768)
    cv2.moveWindow('Image', 100, 100)
    cv2.imshow('Image', cv2.cvtColor(np.array(preview), cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crop_images(image: Image.Image,
                crop_locs: CropLocations) -> list[Image.Image]:
    images = [image.crop((loc.x, loc.y, loc.x_, loc.y_))
              for loc in crop_locs]
    return images
