from PIL import Image, ImageDraw
from photo_scanner.utils.config import CropLocations
from photo_scanner.utils.image import show_image


def preview_crop(image: Image.Image,
                 crop_locs: CropLocations) -> None:
    # Draw the line on the image
    preview = image.copy()
    draw = ImageDraw.Draw(preview)
    for i, l in enumerate(crop_locs):
        draw.line(l.top_line, fill='red', width=l.line_width)
        draw.line(l.bottom_line, fill='red', width=l.line_width)
        draw.line(l.left_line, fill='green', width=l.line_width)
        draw.line(l.right_line, fill='green', width=l.line_width)
        draw.text(xy=(l.x0, l.y0-27*l.factor),
                  text=f'Image {i+1}: {l.width} x {l.height} ({l.pixel:,} px)',
                  fill=(50, 50, 50), font_size=20*l.factor)

    # show
    show_image(preview, name='Preview')


def crop_images(image: Image.Image,
                crop_locs: CropLocations) -> list[Image.Image]:
    images = [image.crop((loc.x0, loc.y0, loc.x1, loc.y1))
              for loc in crop_locs]
    return images
