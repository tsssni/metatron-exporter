from dataclasses import dataclass

@dataclass
class Mesh:
    path: str

@dataclass
class Sphere:
    ...

Shape = Mesh | Sphere
