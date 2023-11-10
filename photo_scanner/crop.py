from PIL import Image, ImageDraw
from photo_scanner.utils.config import CropLocations
from photo_scanner.utils.image import show_image


def preview_crop(image: Image.Image,
                 crop_locs: CropLocations) -> None:
    # Draw the line on the image
    preview = image.copy()
    draw = ImageDraw.Draw(preview)
    for l in crop_locs:
        draw.line(l.top_line, fill='red', width=l.line_width)
        draw.line(l.bottom_line, fill='red', width=l.line_width)
        draw.line(l.left_line, fill='green', width=l.line_width)
        draw.line(l.right_line, fill='green', width=l.line_width)

    # show
    show_image(preview, name='Preview')


def crop_images(image: Image.Image,
                crop_locs: CropLocations) -> list[Image.Image]:
    images = [image.crop((loc.x, loc.y, loc.x_, loc.y_))
              for loc in crop_locs]
    return images
