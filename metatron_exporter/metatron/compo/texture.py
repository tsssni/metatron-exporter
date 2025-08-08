from dataclasses import dataclass

@dataclass
class Constant_Spectrum_Texture:
    spectrum: str
    constant_spectrum: int = 0

@dataclass
class Image_Spectrum_Texture:
    path: str
    type: str
    image_spectrum: int = 0

@dataclass
class Constant_Vector_Texture:
    x: list[float]
    constant_vector: int = 0

@dataclass
class Image_Vector_Texture:
    path: str
    image_vector: int = 0

Texture = Constant_Spectrum_Texture | Image_Spectrum_Texture | Constant_Vector_Texture | Image_Vector_Texture
