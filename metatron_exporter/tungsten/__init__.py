from .transform import *
from .spectrum import *
from .shape import *
from .medium import *
from .light import *
from .material import *
from .. import metatron
from ..metatron import compo
import json


def export() -> list[compo.json]:
    with open(metatron.scene_dir + 'scene.json', 'r') as f:
        scene = json.load(f)
    for m in scene['media']:
        import_medium(m)
    for b in scene['bsdfs']:
        import_material(b)
    for s in scene['primitives']:
        import_shape(s)

    def to_list(ds: list[dict[str, compo.json]]) -> list[compo.json]:
        l: list[compo.json] = []
        for d in ds:
            l = l + list(d.values())
        return l
    return to_list([
        transforms,
        spectra,
        shapes, shape_instances,
        media, medium_instances,
        lights,
        textures, materials,
        dividers,
    ])
