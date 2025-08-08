from dataclasses import dataclass

@dataclass
class Henyey_Greenstein_Phase_Function:
    g: float
    henyey_greenstein: int = 0

Phase_Function = Henyey_Greenstein_Phase_Function

@dataclass
class Vaccum_Medium:
    vacuum: int = 0

@dataclass
class Homogeneous_Medium:
    phase: Phase_Function
    sigma_a: str
    sigma_s: str
    sigma_e: str
    homogeneous: int = 0

@dataclass
class Grid_Medium:
    path: str
    phase: Phase_Function
    sigma_a: str
    sigma_s: str
    sigma_e: str
    density_scale: float
    grid: int = 0

Medium = Vaccum_Medium | Homogeneous_Medium | Grid_Medium

@dataclass
class Medium_Instance:
    path: str
