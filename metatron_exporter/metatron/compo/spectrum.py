from dataclasses import dataclass
from ..linalg import vec3


@dataclass
class Constant_Spectrum:
    x: float


@dataclass
class Rgb_Spectrum:
    c: vec3
    type: str
    color_space: str = ""


@dataclass
class Blackbody_Spectrum:
    T: float


@dataclass
class Visible_Spectrum:
    path: str


@dataclass
class Discrete_Spectrum:
    path: str


Spectrum = (
    Constant_Spectrum
    | Rgb_Spectrum
    | Blackbody_Spectrum
    | Visible_Spectrum
    | Discrete_Spectrum
)
