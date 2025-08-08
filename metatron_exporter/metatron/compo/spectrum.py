from dataclasses import dataclass

@dataclass
class Constant_Spectrum:
    x: float
    constant: int = 0

@dataclass
class Rgb_Spectrum:
    c: list[float]
    type: str
    color_space: str
    rgb: int = 0

Spectrum = Constant_Spectrum | Rgb_Spectrum
