from pathlib import Path
from dataclasses import dataclass
import yaml
from photo_scanner.utils import Profile


Point = tuple[int, int]
Line = tuple[Point, Point]


@dataclass
class CropLocation:
    x0: int
    y0: int
    x1: int
    y1: int
    profile: Profile

    def __post_init__(self):
        # scale the factor according to profile
        self.x0 *= self.factor
        self.y0 *= self.factor
        self.x1 *= self.factor
        self.y1 *= self.factor

    @property
    def factor(self) -> int:
        factors = {
            'lowest': 1,
            'low': 3,
            'middle': 6,
            'high': 12,
        }
        return factors[self.profile]

    @property
    def width(self) -> int:
        return self.x1-self.x0

    @property
    def height(self) -> int:
        return self.y1-self.y0

    @property
    def pixel(self) -> int:
        return self.width*self.height

    @property
    def top_line(self) -> Line:
        return ((self.x0, self.y0), (self.x1, self.y0))

    @property
    def bottom_line(self) -> Line:
        return ((self.x0, self.y1), (self.x1, self.y1))

    @property
    def left_line(self) -> Line:
        return ((self.x0, self.y0), (self.x0, self.y1))

    @property
    def right_line(self) -> Line:
        return ((self.x1, self.y0), (self.x1, self.y1))

    @property
    def line_width(self) -> int:
        return round(2 * self.factor)


CropLocations = list[CropLocation]
LAYOUT_CONFIG_PATH = Path.home() / '.config/photo-scanner/layout.yaml'


def read_crop_config(profile: Profile = 'low') -> CropLocations:
    # read yaml file
    with open(LAYOUT_CONFIG_PATH) as file:
        # parse
        locs: list[dict[str, int]] = yaml.safe_load(file)
        # return as CropLocations
        crop_config = [CropLocation(profile=profile, **loc) for loc in locs]
        return crop_config
