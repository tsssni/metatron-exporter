from dataclasses import dataclass
from ..linalg import vec3, vec4


@dataclass
class Local_Transform:
    translation: vec3 = (0.0, 0.0, 0.0)
    scaling: vec3 = (1.0, 1.0, 1.0)
    rotation: vec4 = (0.0, 0.0, 0.0, 1.0)


@dataclass
class Look_At_Transform:
    position: vec3 = (0.0, 0.0, 0.0)
    look_at: vec3 = (0.0, 0.0, 1.0)
    up: vec3 = (0.0, 1.0, 0.0)


Transform = Local_Transform | Look_At_Transform
