from dataclasses import dataclass
from ..linalg import *

@dataclass
class Parallel_Light:
    L: str

@dataclass
class Point_Light:
    L: str

@dataclass
class Spot_Light:
    L: str
    falloff_start_theta: float
    falloff_end_theta: float

@dataclass
class Environment_Light:
    env_map: str

@dataclass
class Sunsky_Light:
    direction: vec2
    turbidity: float
    albedo: float
    aperture: float
    temperature: float
    intensity: float

Light = Parallel_Light | Point_Light | Spot_Light | Environment_Light | Sunsky_Light
