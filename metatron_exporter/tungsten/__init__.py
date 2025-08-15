from .transform import *
from .spectrum import *
from .medium import *
from .material import *
from .. import metatron
from ..metatron import compo
import json


def export() -> list[compo.json]:
    with open(metatron.scene_dir + 'scene.json', 'r') as f:
        scene = json.load(f)
    transforms.append(compo.json(
        entity='/hierarchy',
        type='transform',
        serialized=compo.Local_Transform(),
    ))
    transforms.append(compo.json(
        entity='/hierarchy/medium',
        type='transform',
        serialized=compo.Local_Transform(),
    ))
    transforms.append(compo.json(
        entity='/hierarchy/shape',
        type='transform',
        serialized=compo.Local_Transform(),
    ))
    for m in scene['media']:
        import_medium(m)
    for b in scene['bsdfs']:
        import_material(b)
    return []\
    + transforms + spectra\
    + media + medium_instances\
    + textures + materials
