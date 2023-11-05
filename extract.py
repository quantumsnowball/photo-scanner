import cv2
from cv2.typing import MatLike
import imutils
from pathlib import Path


def read_rgb_image(name: Path) -> MatLike:
    ''' load the image into an RGB nd-array '''
    raw = cv2.imread(str(name))
    image = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
    return image


def convert_to_gray_scale(image: MatLike) -> MatLike:
    '''
    convert to gray scale
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray


def find_largest_contours(n: int = 4) -> list[MatLike]:
    # find threshold
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # find contours
    contours = cv2.findContours(thresh,
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    contours = contours[:n]

    return contours


def crop_images(contours: list[MatLike],
                root: Path = Path('.'),
                prefix: str = 'IMG') -> None:
    # extract photos
    for i, contour in enumerate(contours):
        # Get the bounding rectangle for the contour
        x, y, w, h = cv2.boundingRect(contour)

        # save the sub-images
        cropped = image[y:y+h, x:x+w]
        image_out = cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR)
        image_path = root / Path(f'{prefix}_{i+1}.jpg')
        cv2.imwrite(str(image_path), image_out)


if __name__ == '__main__':
    image = read_rgb_image(Path('.lab/raw.jpg'))
    gray = convert_to_gray_scale(image)
    contours = find_largest_contours(4)
    crop_images(contours, root=Path('.lab'))
