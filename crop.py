from pathlib import Path
from PIL import Image
import numpy as np


def read_image_array(name: Path,
                     rotation: int = 270) -> np.ndarray:
    image = Image.open(name)
    rotated = image.rotate(rotation, expand=True)
    arr = np.array(rotated)
    return arr


if __name__ == '__main__':
    # read the raw image
    raw = read_image_array(Path('.lab/raw.jpg'))
    # read the user coordinate and width height info
    import matplotlib.pyplot as plt
    plt.imshow(raw)
    plt.show()
    breakpoint()
    # display the preview of the crop
    # crop and save the photos
