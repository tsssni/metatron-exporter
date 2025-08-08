from dataclasses import dataclass
from ..linalg import *

@dataclass
class Local_Transform:
    translation: vec3 = (0.0, 0.0, 0.0)
    scaling: vec3 = (1.0, 1.0, 1.0)
    rotation: vec4 = (0.0, 0.0, 0.0, 1.0)

@dataclass
class Matrix_Transform:
    matrix: mat4 = (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )

Transform = Local_Transform | Matrix_Transform
