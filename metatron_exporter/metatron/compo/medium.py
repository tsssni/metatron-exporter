from dataclasses import dataclass
from ..linalg import vec3, Bounding_Box


@dataclass
class Uniform_Volume:
    bbox: Bounding_Box
    dimensions: vec3


@dataclass
class Nanovdb_Volume:
    path: str


Volume = Uniform_Volume | Nanovdb_Volume


@dataclass
class Phase:
    function: str
    g: float


@dataclass
class Homogeneous_Medium:
    phase: Phase
    sigma_a: str = ""
    sigma_s: str = ""
    sigma_e: str = ""


@dataclass
class Heterogeneous_Medium:
    phase: Phase
    sigma_a: str = ""
    sigma_s: str = ""
    sigma_e: str = ""
    dimensions: vec3 = (0, 0, 0)
    density: str = ""
    density_scale: float = 1.0


@dataclass
class Vaccum_Medium: ...


Medium = Homogeneous_Medium | Heterogeneous_Medium | Vaccum_Medium
