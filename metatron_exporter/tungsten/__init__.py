from .transform import transforms
from .spectrum import spectra
from .medium import import_medium, media, medium_instances
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
    return transforms + spectra + media + medium_instances
