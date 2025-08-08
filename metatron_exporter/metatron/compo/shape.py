from dataclasses import dataclass

@dataclass
class Sphere:
    sphere: int = 0

@dataclass
class Mesh:
    path: str
    mesh: int = 0

Shape = Sphere | Mesh

@dataclass
class Shape_Instance:
    path: str
