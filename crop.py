from pathlib import Path
from PIL import Image
import numpy as np


def read_image_array(name: Path) -> np.ndarray:
    image = Image.open(name)
    arr = np.array(image)
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
