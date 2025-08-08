from dataclasses import dataclass

@dataclass
class Interface_Bsdf:
    interface: int = 0

@dataclass
class Lambertian_Bsdf:
    lambertian: int = 0

@dataclass
class Microfacet_Bsdf:
    microfacet: int = 0

Bsdf = Interface_Bsdf | Lambertian_Bsdf | Microfacet_Bsdf

@dataclass
class Material:
    bsdf: Bsdf
    spectrum_textures: dict[str, str]
    vector_textures: dict[str, str]
