from ..metatron import compo
from ..metatron.linalg import *
from .spectrum import *
from typing import cast
import sys

textures: list[compo.json] = []
materials: list[compo.json] = []

def import_texture(json, path: str, spectype: str = '', iscolor=True, isvector=False) -> str:
    type = '' if not isinstance(json, dict) or 'type' not in json else json['type']
    spec_path = '/spectrum/' + path
    tex_path = '/texture/' + path

    if isvecable(json):
        json = cast(vecable, json)
        if isvector:
            tex=compo.Constant_Vector_Texture(
                x = to_vec4(json),
            )
        else:
            if iscolor:
                spec = compo.Rgb_Spectrum(
                    c = to_vec3(json),
                    type = spectype,
                    color_space='/spectrum/color_space/sRGB',
                )
            elif not isinstance(json, list):
                spec = compo.Constant_Spectrum(
                    x = json,
                )
            else:
                print('only accept scalar for non-color spectrum texture')
                sys.exit(1)
            spectra.append(compo.json(
                entity=spec_path,
                type='spectrum',
                serialized=spec,
            ))
            tex = compo.Constant_Spectrum_Texture(
                spectrum=spec_path,
            )
    elif isinstance(json, str) or type == 'bitmap':
        path = json if isinstance(json, str) else json['file']
        if isvector:
            tex = compo.Image_Vector_Texture(
                path=path,
            )
        else:
            tex = compo.Image_Spectrum_Texture(
                path=path,
                type=spectype,
            )
    elif type == 'checker':
        # not supported yet
        tex = compo.Constant_Spectrum_Texture(
            spectrum='/spectrum/one',
        )
    else:
        print(f'{type} texture not supported')
        print(json)
        sys.exit(1)

    textures.append(compo.json(
        entity=tex_path,
        type='texture',
        serialized=tex,
    ))
    return tex_path

def import_material(json):
    type = json['type']
    name = json['name']
    material_path = '/materials/' + name
    if type == 'lambert':
        albedo = import_texture(json['albedo'], name + '/reflectance', spectype='albedo', iscolor=True)
        materials.append(compo.json(
            entity=material_path,
            type='material',
            serialized=compo.Material(
                bsdf=compo.Lambertian_Bsdf(),
                spectrum_textures={
                    'reflectance': albedo,
                },
                vector_textures={},
            ),
        ))
    elif type == 'dieletric' or type == 'rough_dielectric':
        eta = import_texture(json['ior'], name + '/eta', spectype='unbounded')
        alpha = import_texture(json['roughness'] if 'roughness' in json else 0.001, name + '/alpha', isvector=True)
        materials.append(compo.json(
            entity=material_path,
            type='material',
            serialized=compo.Material(
                bsdf=compo.Microfacet_Bsdf(),
                spectrum_textures={
                    'eta': eta,
                },
                vector_textures={
                    'alpha': alpha,
                },
            ),
        ))
    elif type == 'conductor' or type == 'rough_conductor':
        if 'material' in json:
            eta = '/spectrum/eta/' + json['material']
            k = '/spectrum/k/' + json['material']
        else:
            eta = import_texture(json['eta'], name + '/eta', spectype='unbounded', iscolor=False)
            k = import_texture(json['k'], name + '/k', spectype='unbounded', iscolor=False)
        alpha = import_texture(json['roughness'] if 'roughness' in json else 0.001, name + '/alpha', isvector=True)
        materials.append(compo.json(
            entity=material_path,
            type='material',
            serialized=compo.Material(
                bsdf=compo.Microfacet_Bsdf(),
                spectrum_textures={
                    'eta': eta,
                    'k': k,
                },
                vector_textures={
                    'alpha': alpha,
                },
            ),
        ))
