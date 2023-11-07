from pathlib import Path
from PIL import Image, ImageDraw


def read_image_array(name: Path,
                     rotation: int = 270) -> Image.Image:
    # open
    image = Image.open(name)
    # rotate the image
    rotated = image.rotate(rotation, expand=True)
    #
    return rotated


def preview_crop(image: Image.Image,
                 fill: tuple[int, int, int] = (0, 255, 0, ),
                 width: int = 5) -> None:
    draw = ImageDraw.Draw(image)
    # Define the coordinates of the line
    line_coordinates = [(1000, 0), (1000, 1000)]
    # Draw the line on the image
    draw.line(line_coordinates, fill=fill, width=width)
    # show
    image.show()


if __name__ == '__main__':
    # read the raw image
    raw = read_image_array(Path('.lab/raw.jpg'))
    # read the user coordinate and width height info
    preview_crop(raw)
    # import matplotlib.pyplot as plt
    # plt.imshow(np.array(raw))
    # plt.show()
    breakpoint()
    # display the preview of the crop
    # crop and save the photos
