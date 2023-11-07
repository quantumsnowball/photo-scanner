import cv2
from cv2.typing import MatLike
import imutils
from pathlib import Path
import numpy as np
import itertools


def read_rgb_image(name: Path) -> MatLike:
    '''
    load the image into an RGB nd-array
    '''
    # read image
    raw = cv2.imread(str(name))
    # correct to RGB
    image = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
    #
    return image


def convert_to_gray_scale(image: MatLike) -> MatLike:
    '''
    convert to gray scale
    '''
    # convert to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #
    return gray


def manually_split(image: MatLike,
                   x: int, y: int) -> list[MatLike]:
    '''
    manually split image into 4 sub-images
    '''
    images = [
        image[0:y, 0:x],
        image[0:y, x:],
        image[y:, 0:x],
        image[y:, x:],
    ]
    # Display the sub-images
    # cv2.imshow("Sub-Image 0", images[0])
    # cv2.imshow("Sub-Image 1", images[1])
    # cv2.imshow("Sub-Image 2", images[2])
    # cv2.imshow("Sub-Image 3", images[3])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # return list
    return images


def find_largest_contour(src: MatLike,
                         target_aspect_ratio: float = 5/3.5) -> MatLike:
    '''
    find the largest contour in an image
    '''

    # test metrics
    def how_close_to_aspect_ratio(contour) -> float:
        rect = cv2.boundingRect(contour)
        aspect_ratio = rect[-2] / rect[-1]
        diff = abs(aspect_ratio - target_aspect_ratio)
        return diff

    # extract
    def extract(thresh_value: int,
                erode_size: int,
                dilate_size: int,
                erode_iteration: int,
                dilate_iteration: int) -> tuple[MatLike, float]:
        # find threshold
        _, thresh = cv2.threshold(src, thresh_value, 255, cv2.THRESH_BINARY_INV)
        # thresh = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 5)

        # clean threshold
        thresh = cv2.erode(thresh, kernel=np.ones((erode_size, erode_size,),), iterations=erode_iteration)
        thresh = cv2.dilate(thresh, kernel=np.ones((dilate_size, dilate_size,),), iterations=dilate_iteration)

        # find contours
        contours = cv2.findContours(thresh,
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contour = max(contours, key=cv2.contourArea)

        # calc metrics
        aspect_ratio_diff = how_close_to_aspect_ratio(contour)

        # return
        return contour, aspect_ratio_diff

    # try different params to find the best
    args_combos = itertools.product(
        (128, 196, 230),
        (3, 5, 8),
        (5, 10, 20, ),
        (5, 8),
        (3, 5,),
    )
    contours = [extract(*args) for args in args_combos]
    best_contour = min(contours, key=lambda x: x[-1])[0]

    return best_contour


def crop_images(src: list[MatLike],
                contours: list[MatLike],
                ) -> list[MatLike]:
    '''
    crop images into sub-images
    '''
    cropped_images = []
    for image, contour in zip(src, contours):
        # Get the bounding rectangle for the contour
        x, y, w, h = cv2.boundingRect(contour)

        # crop the image
        cropped = image[y:y+h, x:x+w]
        image_out = cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR)
        cropped_images.append(image_out)
    # return list of cropped images
    return cropped_images


def save_images(images: list[MatLike],
                root: Path = Path('.'),
                prefix: str = 'IMG',
                quality: int = 90) -> None:
    '''
    save images into files
    '''
    for i, image in enumerate(images):
        image_path = str(root / Path(f'{prefix}_{i+1}.jpg'))
        cv2.imwrite(image_path, image, (cv2.IMWRITE_JPEG_QUALITY, quality, ))


if __name__ == '__main__':
    raw = read_rgb_image(Path('.lab/raw.jpg'))
    images = manually_split(raw, 2300, 1200)
    gray_images = [convert_to_gray_scale(image) for image in images]
    contours = [find_largest_contour(gray) for gray in gray_images]
    cropped_images = crop_images(images, contours)
    save_images(cropped_images, root=Path('.lab'), quality=75)
