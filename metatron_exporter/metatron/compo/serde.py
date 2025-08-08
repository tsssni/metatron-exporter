from dataclasses import dataclass

from .camera import Camera
from .light import Light
from .material import Material
from .medium import Medium, Medium_Instance
from .shape import Shape, Shape_Instance
from .spectrum import Spectrum
from .texture import Texture
from .tracer import Divider, Tracer
from .transform import Transform

Component = (
    Camera | Light | Material |
    Medium | Medium_Instance |
    Shape | Shape_Instance |
    Spectrum | Texture |
    Divider | Tracer | Transform
)

@dataclass
class json:
    entity: str
    type: str
    serialized: Component
