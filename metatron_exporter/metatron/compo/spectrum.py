from dataclasses import dataclass
from ..linalg import *

@dataclass
class Constant_Spectrum:
    x: float
    constant: int = 0

@dataclass
class Rgb_Spectrum:
    c: vec3
    type: str
    color_space: str
    rgb: int = 0

Spectrum = Constant_Spectrum | Rgb_Spectrum
