from pathlib import Path
from PIL import Image, ImageDraw
from utils import CropLocations, read_cropping_config_yaml, save_images


Xs = (700, 2400)
Ys = (120, 1400)
WIDTH = 1550
HEIGHT = 1080


def read_image_array(name: Path,
                     rotation: int = 270) -> Image.Image:
    # open
    image = Image.open(name)
    # rotate the image
    rotated = image.rotate(rotation, expand=True)
    #
    return rotated


def preview_crop(image: Image.Image,
                 crop_locs: CropLocations,
                 line_width: int = 5) -> None:
    # Draw the line on the image
    draw = ImageDraw.Draw(image)
    for l in crop_locs:
        draw.line(l.top, fill='red', width=line_width)
        draw.line(l.bottom, fill='red', width=line_width)
        draw.line(l.left, fill='green', width=line_width)
        draw.line(l.right, fill='green', width=line_width)

    # show
    image.show()


def crop_images(image: Image.Image,
                Xs: tuple[int, ...],
                Ys: tuple[int, ...],
                width: int,
                height: int) -> list[Image.Image]:
    images = [image.crop((x, y, x+width, y+height)) for x in Xs for y in Ys]
    return images


if __name__ == '__main__':
    # read the raw image
    raw = read_image_array(Path('.lab/raw.jpg'))
    # read the user coordinate and width height info
    crop_locs = read_cropping_config_yaml('config.yaml')
    # display the preview of the crop
    preview_crop(raw, crop_locs)
    # crop and save the photos
    images = crop_images(raw, Xs, Ys, WIDTH, HEIGHT)
    save_images(images, outdir=Path('.lab'))
