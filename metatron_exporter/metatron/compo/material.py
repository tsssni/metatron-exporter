from dataclasses import dataclass

@dataclass
class Interface_Bsdf:
    interface: int = 0

@dataclass
class Physical_Bsdf:
    physical: int = 0

Bsdf = Interface_Bsdf | Physical_Bsdf

@dataclass
class Material:
    bsdf: Bsdf
    spectrum_textures: dict[str, str]
    vector_textures: dict[str, str]
