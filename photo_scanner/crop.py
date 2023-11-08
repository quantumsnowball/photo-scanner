from pathlib import Path
from PIL import Image, ImageDraw
from photo_scanner.utils import CropLocations, read_cropping_config_yaml, save_images


def read_image(name: Path | str,
               rotation: int = 270) -> Image.Image:
    # as Path
    name = Path(name) if isinstance(name, str) else name
    # open
    image = Image.open(name)
    # rotate the image
    rotated = image.rotate(rotation, expand=True)
    #
    return rotated


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
    preview.show()


def crop_images(image: Image.Image,
                crop_locs: CropLocations) -> list[Image.Image]:
    images = [image.crop((loc.x, loc.y, loc.x_, loc.y_))
              for loc in crop_locs]
    return images


if __name__ == '__main__':
    # read the raw image
    raw = read_image(Path('.lab/raw.jpg'))
    # read the user coordinate and width height info
    crop_locs = read_cropping_config_yaml('config.yaml')
    # display the preview of the crop
    preview_crop(raw, crop_locs)
    # crop and save the photos
    images = crop_images(raw, crop_locs)
    save_images(images, outdir='.lab')
