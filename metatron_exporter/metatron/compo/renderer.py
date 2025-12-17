from dataclasses import dataclass
from ..linalg import vec2


@dataclass
class Film:
    spp: int = 16
    depth: int = 64
    film_size: vec2 = (0.036, 0.024)
    image_size: vec2 = (1280, 720)
    r: str = ""
    g: str = ""
    b: str = ""
    color_space: str = ""


@dataclass
class Volume_Path_Integrator:
    variant: str = "volume_path"


Integrator = Volume_Path_Integrator


@dataclass
class LBVH:
    variant: str = "lbvh"
    num_guide_leaf_prims: int = 4


Acceleration = LBVH


@dataclass
class Uniform_Emitter:
    variant: str = "uniform"


Emitter = Uniform_Emitter


@dataclass
class Independent_Sampler:
    variant: str = "independent"


@dataclass
class Halton_Sampler:
    variant: str = "halton"
    scale_exponential: vec2 = (7, 4)


@dataclass
class Sobol_Sampler:
    variant: str = "sobol"


Sampler = Independent_Sampler | Halton_Sampler | Sobol_Sampler


@dataclass
class Box_Filter:
    variant: str = "box"
    radius: vec2 = (0.5, 0.5)


@dataclass
class Gaussian_Filter:
    variant: str = "gaussian"
    radius: vec2 = (1.5, 1.5)
    sigma: float = 0.5


@dataclass
class Lanczos_Filter:
    variant: str = "lanczos"
    radius: vec2 = (0.5, 0.5)
    tau: float = 3


Filter = Box_Filter | Gaussian_Filter | Lanczos_Filter


@dataclass
class Pinhole_Lens:
    variant: str = "pinhole"
    focal_distance: float = 0.035


@dataclass
class Thin_Lens:
    variant: str = "thin"
    aperture: float = 5.6
    focal_length: float = 0.035
    focus_distance: float = 10


Lens = Pinhole_Lens | Thin_Lens


@dataclass
class Renderer:
    film: Film
    integrator: Integrator
    accel: Acceleration
    emitter: Emitter
    sampler: Sampler
    filter: Filter
    lens: Lens
