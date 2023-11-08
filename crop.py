from pathlib import Path
from typing import Literal
from PIL import Image, ImageDraw


X = (700, 2400)
Y = (120, 1400)
W = 1550
H = 1080


def read_image_array(name: Path,
                     rotation: int = 270) -> Image.Image:
    # open
    image = Image.open(name)
    # rotate the image
    rotated = image.rotate(rotation, expand=True)
    #
    return rotated


def preview_crop(image: Image.Image,
                 width: int = 5) -> None:
    draw = ImageDraw.Draw(image)
    # Define the coordinates of the line
    # Draw the line on the image
    for x in X:
        draw.line([(x, 0), (x, image.height)], fill='red', width=width)
        draw.line([(x+W, 0), (x+W, image.height)], fill='green', width=width)
    for y in Y:
        draw.line([(0, y), (image.width, y)], fill='red', width=width)
        draw.line([(0, y+H), (image.width, y+H)], fill='green', width=width)

    # show
    image.show()


def crop_images(image: Image.Image,
                x: tuple[int, ...],
                y: tuple[int, ...],
                width: int,
                height: int) -> list[Image.Image]:
    images = [image.crop((x, y, x+width, y+height)) for x in X for y in Y]
    return images


def save_images(images: list[Image.Image],
                *,
                outdir: Path,
                prefix: str = 'IMG',
                ext: Literal['jpg', 'png'] = 'jpg') -> None:
    for i, image in enumerate(images):
        image.save(outdir / f'{prefix}_{i}.jpg')


if __name__ == '__main__':
    # read the raw image
    raw = read_image_array(Path('.lab/raw.jpg'))
    # read the user coordinate and width height info
    # display the preview of the crop
    # preview_crop(raw)
    # crop and save the photos
    images = crop_images(raw, X, Y, W, H)
    save_images(images, outdir=Path('.lab'))
