from dataclasses import dataclass
from ..linalg import *

@dataclass
class Pinhole_Lens:
    focal_length: float
    pinhole: int = 0

@dataclass
class Thin_Lens:
    aperture: float
    focal_length: float
    focus_distance: float
    thin: int = 0

Lens = Pinhole_Lens | Thin_Lens

@dataclass
class Independent_Sampler:
    independent: int = 0

@dataclass
class Halton_Sampler:
    halton: int = 0

Sampler = Independent_Sampler | Halton_Sampler

@dataclass
class Box_Filter:
    radius: vec2 = (0.5, 0.5)
    box: int = 0

@dataclass
class Gaussian_Filter:
    radius: vec2 = (1.5, 1.5)
    sigma: float = 0.5
    gaussian: int = 0

@dataclass
class Lanczos_Filter:
    radius: vec2 = (0.5, 0.5)
    tau: float = 3.0
    lanczos: int = 0

Filter = Box_Filter | Gaussian_Filter | Lanczos_Filter

@dataclass
class Camera:
    film_size: vec2
    image_size: vec2
    spp: int
    depth: int
    lens: Lens
    sampler: Sampler
    filter: Filter
    initial_medium: str = "/hierarchy/medium/vaccum"
    color_space: str = "/color-space/sRGB"
