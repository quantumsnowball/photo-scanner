import cv2
from cv2.typing import MatLike
import imutils
from pathlib import Path


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


def find_largest_contours(src: MatLike,
                          n: int = 4) -> list[MatLike]:
    '''
    find largest contours in an image
    '''
    # find threshold
    _, thresh = cv2.threshold(src, 200, 255, cv2.THRESH_BINARY_INV)

    # find contours
    contours = cv2.findContours(thresh,
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contours = contours[:n]
    #
    return contours


def crop_images(src: MatLike,
                contours: list[MatLike],
                ) -> list[MatLike]:
    '''
    crop images into sub-images
    '''
    cropped_images = []
    for contour in contours:
        # Get the bounding rectangle for the contour
        x, y, w, h = cv2.boundingRect(contour)

        # crop the image
        cropped = src[y:y+h, x:x+w]
        image_out = cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR)
        cropped_images.append(image_out)
    # return list of cropped images
    return cropped_images


def save_images(images: list[MatLike],
                root: Path = Path('.'),
                prefix: str = 'IMG') -> None:
    '''
    save images into files
    '''
    for i, image in enumerate(images):
        image_path = str(root / Path(f'{prefix}_{i+1}.jpg'))
        cv2.imwrite(image_path, image)


if __name__ == '__main__':
    raw = read_rgb_image(Path('.lab/raw.jpg'))
    gray = convert_to_gray_scale(raw)
    contours = find_largest_contours(gray, 4)
    images = crop_images(raw, contours)
    save_images(images, root=Path('.lab'))
