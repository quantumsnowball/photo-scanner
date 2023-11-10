from pathlib import Path
from dataclasses import dataclass
import yaml
from photo_scanner.utils import Profile


Point = tuple[int, int]
Line = tuple[Point, Point]


@dataclass
class CropLocation:
    x: int
    y: int
    width: int
    height: int
    profile: Profile

    def __post_init__(self):
        # scale the factor according to profile
        self.x = round(self.x*self.factor)
        self.y = round(self.y*self.factor)
        self.width = round(self.width*self.factor)
        self.height = round(self.height*self.factor)

    @property
    def factor(self) -> float:
        factors = {
            'lowest': 1,
            'low': 3,
            'middle': 6,
            'high': 12,
        }
        return factors[self.profile]

    @property
    def x_(self) -> int:
        return self.x+self.width

    @property
    def y_(self) -> int:
        return self.y+self.height

    @property
    def top(self) -> Line:
        return ((self.x, self.y), (self.x_, self.y))

    @property
    def bottom(self) -> Line:
        return ((self.x, self.y_), (self.x_, self.y_))

    @property
    def left(self) -> Line:
        return ((self.x, self.y), (self.x, self.y_))

    @property
    def right(self) -> Line:
        return ((self.x_, self.y), (self.x_, self.y_))

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
