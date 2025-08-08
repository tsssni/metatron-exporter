from dataclasses import dataclass

@dataclass
class Parallel_Light:
    spectrum: str
    parallel: int = 0

@dataclass
class Point_Light:
    spectrum: str
    parallel: int = 0

@dataclass
class Spot_Light:
    spectrum: str
    falloff_start_theta: float
    falloff_end_theta: float
    parallel: int = 0

@dataclass
class Environment_Light:
    env_map: str
    environment: int = 0

Light = Parallel_Light | Point_Light | Spot_Light | Environment_Light
