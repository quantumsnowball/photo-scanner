from pathlib import Path
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
    line_coordinates = [(1000, 0), (1000, 1000)]
    # Draw the line on the image
    # draw.line(line_coordinates, fill=fill, width=width)
    for x in X:
        draw.line([(x, 0), (x, image.height)], fill='red', width=width)
        draw.line([(x+W, 0), (x+W, image.height)], fill='green', width=width)
    for y in Y:
        draw.line([(0, y), (image.width, y)], fill='red', width=width)
        draw.line([(0, y+H), (image.width, y+H)], fill='green', width=width)

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
    # display the preview of the crop
    # crop and save the photos
