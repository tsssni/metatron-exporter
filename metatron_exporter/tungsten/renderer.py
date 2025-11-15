from metatron_exporter.metatron.compo.renderer import LBVH, Film, Lanczos_Filter, Sobol_Sampler, Thin_Lens, Uniform_Emitter, Volume_Path_Integrator
from ..metatron import compo
from .transform import *

def import_renderer(json) -> compo.json:
    camera = json['camera']
    camera_path = '/hierarchy/camera'
    import_transform(camera['transform'], camera_path)
    return compo.json(
        entity = '/',
        type = compo.Renderer.__name__.lower(),
        serialized = compo.Renderer(
            Film(),
            Volume_Path_Integrator(),
            LBVH(),
            Uniform_Emitter(),
            Sobol_Sampler(),
            Lanczos_Filter(),
            Thin_Lens(),
        ),
    )
