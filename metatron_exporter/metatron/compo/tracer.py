from dataclasses import dataclass, field

@dataclass
class Divider:
    shape: str
    int_medium: str = '/hierarchy/medium/vaccum'
    ext_medium: str = '/hierarchy/medium/vaccum'
    material: str = ''

@dataclass
class Uniform_Emitter:
    uniform: int = 0

Emitter = Uniform_Emitter

@dataclass
class LBVH:
    lbvh: int = 0

Acceleration = LBVH

@dataclass
class Volume_Path_Integrator:
    volume_path_integration: int = 0

Integrator = Volume_Path_Integrator

@dataclass
class Tracer:
    emitter: Emitter
    accel: Acceleration
    integrator: Integrator
