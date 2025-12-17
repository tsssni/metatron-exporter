from dataclasses import dataclass

from .transform import Transform
from .spectrum import Spectrum
from .shape import Shape
from .medium import Volume, Medium
from .material import Vector_Texture, Spectrum_Texture, Material, Divider
from .light import Light
from .renderer import Renderer

Component = (
    Transform
    | Spectrum
    | Shape
    | Volume
    | Medium
    | Vector_Texture
    | Spectrum_Texture
    | Material
    | Divider
    | Light
    | Renderer
)


@dataclass
class json:
    entity: str
    type: str
    serialized: Component | dict
