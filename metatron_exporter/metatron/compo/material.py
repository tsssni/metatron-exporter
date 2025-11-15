from dataclasses import dataclass
from ..linalg import *

@dataclass
class Constant_Vector_Texture:
    x: vec4

@dataclass
class Image_Vector_Texture:
    path: str
    distr: str = ''

Vector_Texture = Constant_Vector_Texture | Image_Vector_Texture

@dataclass
class Constant_Spectrum_Texture:
    x: str

@dataclass
class Image_Spectrum_Texture:
    path: str
    type: str
    distr: str = ''
    color_space: str = ''

@dataclass
class Checkerboard_Texture:
    x: str
    y: str
    uv_scale: vec2

Spectrum_Texture = Constant_Spectrum_Texture | Image_Spectrum_Texture | Checkerboard_Texture

@dataclass
class Physical_Material:
    reflectance: str = ''
    eta: str = ''
    k: str = ''
    emission: str = ''

    alpha: str = ''
    alpha_u: str = ''
    alpha_v: str = ''
    normal: str = ''

@dataclass
class Interface_Material:
    ...

Material = Physical_Material | Interface_Material

@dataclass
class Divider:
    shape: str = ''
    int_medium: str = ''
    ext_medium: str = ''
    material: str = ''
    local_to_render: str = ''
    int_to_render: str = ''
    ext_to_render: str = ''
