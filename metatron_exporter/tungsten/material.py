from ..metatron import compo, shared
from ..metatron.linalg import *
from .spectrum import *
from typing import cast
import sys
import os
import re
import shutil

textures: dict[str, compo.json] = {}
materials: dict[str, compo.json] = {}

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
                    color_space='/color-space/sRGB',
                )
            elif not isinstance(json, list):
                spec = compo.Constant_Spectrum(
                    x = json,
                )
            else:
                print('only accept scalar for non-color spectrum texture')
                sys.exit(1)
            spectra[spec_path] = compo.json(
                entity=spec_path,
                type='spectrum',
                serialized=spec,
            )
            tex = compo.Constant_Spectrum_Texture(
                spectrum=spec_path,
            )
    elif isinstance(json, str) or type == 'bitmap':
        input_path = json if isinstance(json, str) else json['file']
        output_path = re.sub(r'textures', 'texture', input_path)
        os.makedirs(shared.output_dir + 'texture', exist_ok=True)
        shutil.copy(shared.scene_dir + input_path, shared.output_dir + 'texture/')
        if isvector:
            tex = compo.Image_Vector_Texture(
                path=output_path,
            )
        else:
            tex = compo.Image_Spectrum_Texture(
                path=output_path,
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

    textures[tex_path] = compo.json(
        entity=tex_path,
        type='texture',
        serialized=tex,
    )
    return tex_path

def import_material(json, index: int=0) -> str:
    if isinstance(json, str):
        mat_path = '/material/' + json
        return mat_path
    elif 'name' in json:
        name = json['name']
    else:
        name = str(index)
    mat_path = '/material/' + name
    type = json['type']

    if type == 'lambert':
        albedo = import_texture(json['albedo'], name + '/reflectance', spectype='albedo', iscolor=True)
        materials[mat_path] = compo.json(
            entity=mat_path,
            type='material',
            serialized=compo.Material(
                bsdf=compo.Lambertian_Bsdf(),
                spectrum_textures={
                    'reflectance': albedo,
                },
                vector_textures={},
            ),
        )
    elif type == 'dielectric' or type == 'rough_dielectric':
        eta = import_texture(json['ior'], name + '/eta', spectype='unbounded')
        alpha = import_texture(json['roughness'] if 'roughness' in json else 0.001, name + '/alpha', isvector=True)
        materials[mat_path] = compo.json(
            entity=mat_path,
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
        )
    elif type == 'conductor' or type == 'rough_conductor':
        if 'material' in json:
            eta = '/texture/eta/' + json['material']
            k = '/texture/k/' + json['material']
        else:
            eta = import_texture(json['eta'], name + '/eta', spectype='unbounded', iscolor=False)
            k = import_texture(json['k'], name + '/k', spectype='unbounded', iscolor=False)
        alpha = import_texture(json['roughness'] if 'roughness' in json else 0.001, name + '/alpha', isvector=True)
        materials[mat_path] = compo.json(
            entity=mat_path,
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
        )
    else:
        albedo = import_texture([1.0, 1.0, 1.0], name + '/reflectance', spectype='albedo', iscolor=True)
        materials[mat_path] = compo.json(
            entity=mat_path,
            type='material',
            serialized=compo.Material(
                bsdf=compo.Lambertian_Bsdf(),
                spectrum_textures={
                    'reflectance': albedo,
                },
                vector_textures={},
            ),
        )

    return mat_path
