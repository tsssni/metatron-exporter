from .. import metatron
from ..metatron import compo
import json

def export() -> list[compo.json]:
    with open(metatron.scene_dir + 'scene.json', 'r') as f:
        s = json.load(f)
    return [
        compo.json(
            entity='/spectrum/white',
            type="spectrum",
            serialized=compo.Rgb_Spectrum(
                c = [1.0, 1.0, 1.0],
                type = 'illluminant',
                color_space = '/color-space/sRGB',
            )
        ),
        compo.json(
            entity='/texture/white',
            type='texture',
            serialized=compo.Constant_Spectrum_Texture(
                spectrum = '/spectrum/white',
            ),
        ),
        compo.json(
            entity='/material/diffuse',
            type='material',
            serialized=compo.Material(
                bsdf = compo.Lambertian_Bsdf(),
                spectrum_textures={
                    'reflectance': '/texture/white',
                },
                vector_textures={},
            ),
        ),
        compo.json(
            entity='/hierarchy/camera',
            type='transform',
            serialized=compo.Matrix_Transform(),
        ),
    ]
