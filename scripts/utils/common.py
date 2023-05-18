import os
import math
from typing import Dict, Tuple


def to_vector_rgb(rgb_8bit: Tuple[int]) -> Tuple[int|float]:
    return tuple(x / 255 for x in rgb_8bit)


def to_radians_xyz(degree_xyz: Tuple[int|float]) -> Tuple[int|float]:
    return tuple(math.radians(rot) for rot in degree_xyz)