from pathlib import Path
from dataclasses import dataclass
from typing import Self, TypedDict
import yaml
from photo_scanner.utils import Layout, Profile


Point = tuple[int, int]
Line = tuple[Point, Point]


@dataclass
class CropLocation:
    x0: int
    y0: int
    x1: int
    y1: int
    profile: Profile

    def __post_init__(self) -> None:
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


CropInfo = list[dict[str, int]]


class LayoutInfoItem(TypedDict):
    rotation: int
    crop: CropInfo


LayoutInfo = dict[str, LayoutInfoItem]


CropLocations = list[CropLocation]
LAYOUT_CONFIG_PATH = Path.home() / '.config/photo-scanner/layout.yaml'


def read_layout_config(layout: Layout = 'four', profile: Profile = 'low') -> tuple[int, CropLocations]:
    # read yaml file
    with open(LAYOUT_CONFIG_PATH) as file:
        # parse
        layout_info: LayoutInfo = yaml.safe_load(file)
        rotation: int = layout_info[layout]['rotation']
        crop_info: CropInfo = layout_info[layout]['crop']
        # return as CropLocations
        crop_location = [CropLocation(profile=profile, **loc) for loc in crop_info]
        return rotation, crop_location
