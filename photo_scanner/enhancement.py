from PIL import Image
import PIL.ImageOps as ops


def auto_contrast(image: Image.Image) -> Image.Image:
    return ops.autocontrast(image)


if __name__ == '__main__':
    from photo_scanner.utils.image import read_image
    import numpy as np
    import cv2
    from photo_scanner.utils.image import show_image
    original = read_image('.lab/1.jpg', rotation=0)
    enhanced = read_image('.lab/5.jpg', rotation=0)
    diff = np.array(enhanced) - np.array(original)
    show_image(diff)
