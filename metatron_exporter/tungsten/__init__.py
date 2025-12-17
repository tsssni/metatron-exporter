from .transform import *
from .medium import *
from .bsdf import *
from .primitive import *
from .renderer import *
from ..metatron import compo, shared
import json


def export() -> list[compo.json]:
    with open(shared.scene_dir + "scene.json", "r") as f:
        scene = json.load(f)
    for m in scene["media"]:
        import_medium(m)
    for b in scene["bsdfs"]:
        import_bsdf(b)
    for s in scene["primitives"]:
        import_primitve(s)
    renderer = import_renderer(scene)

    def to_list(ds: list[dict[str, compo.json]]) -> list[compo.json]:
        l: list[compo.json] = []
        for d in ds:
            l = l + list(d.values())
        return l

    return to_list(
        [
            transforms,
            spectra,
            shapes,
            media,
            textures,
            materials,
            dividers,
            lights,
        ]
    ) + [renderer]
