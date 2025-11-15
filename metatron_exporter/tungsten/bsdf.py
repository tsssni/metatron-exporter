from ..metatron import compo, shared
from ..metatron.linalg import *
import sys
import os
import re
import shutil

spectra: dict[str, compo.json] = {}
textures: dict[str, compo.json] = {}
materials: dict[str, compo.json] = {}

@dataclass
class Texture_Attribute:
    vector: bool = False
    color: bool = True
    type: str = 'albedo'
    distr: str = 'none'

def import_texture(json, path: str, attr: Texture_Attribute) -> str:
    tex_type = '' if not isinstance(json, dict) or 'type' not in json else json['type']
    spec_path = '/spectrum/' + path
    tex_path = '/texture/' + path

    if isvecable(json):
        json = cast(vecable, json)
        if attr.vector:
            tex = compo.Constant_Vector_Texture(
                x = to_vec4(json),
            )
        else:
            if attr.color:
                spec = compo.Rgb_Spectrum(
                    c = to_vec3(json),
                    type = attr.type,
                )
            elif not isinstance(json, list):
                spec = compo.Constant_Spectrum(
                    x = json,
                )
            else:
                print('only accept scalar for non-color spectrum texture')
                sys.exit(1)
            spectra[spec_path] = compo.json(
                entity = spec_path,
                type = type(spec).__name__.lower(),
                serialized = spec,
            )
            tex = compo.Constant_Spectrum_Texture(
                x=spec_path,
            )
    elif isinstance(json, str) or tex_type == 'bitmap':
        input_path = json if isinstance(json, str) else json['file']
        output_path = re.sub(r'textures', 'texture', input_path)
        os.makedirs(shared.output_dir + 'texture', exist_ok=True)
        shutil.copy(shared.scene_dir + input_path, shared.output_dir + 'texture/')
        if attr.vector:
            tex = compo.Image_Vector_Texture(
                path = output_path,
                distr = attr.distr,
            )
        else:
            tex = compo.Image_Spectrum_Texture(
                path = output_path,
                type = attr.type,
                distr = attr.distr,
            )
    elif tex_type == 'checker':
        x = compo.Rgb_Spectrum(
            c = to_vec3(json['on_color']),
            type = attr.type,
        )
        y = compo.Rgb_Spectrum(
            c = to_vec3(json['off_color']),
            type = attr.type,
        )
        spectra[spec_path + '/x'] = compo.json(
            entity = spec_path + '/x',
            type = type(x).__name__.lower(),
            serialized = x,
        );
        spectra[spec_path + '/y'] = compo.json(
            entity = spec_path + '/y',
            type = type(x).__name__.lower(),
            serialized = y,
        );
        tex = compo.Checkerboard_Texture(
            x = spec_path + '/x',
            y = spec_path + '/y',
            uv_scale = to_vec2([json['res_u'], json['res_v']]),
        )
    else:
        print(f'{tex_type} texture not supported')
        print(json)
        sys.exit(1)

    textures[tex_path] = compo.json(
        entity = tex_path,
        type = type(tex).__name__.lower(),
        serialized = tex,
    )
    return tex_path

def import_bsdf(json, name: str = '') -> str:
    if isinstance(json, str):
        return '/material/' + json

    mat_name = json['name'] if 'name' in json else name
    mat_type = json['type']
    if mat_type == 'lambert':
        reflectance = import_texture(json['albedo'], mat_name + '/reflectance', Texture_Attribute())
        mat = compo.Physical_Material(reflectance = reflectance)
    elif mat_type == 'dielectric' or mat_type == 'rough_dielectric':
        eta = import_texture(json['ior'], mat_name + '/eta', Texture_Attribute(color = False))
        alpha = import_texture(json['roughness'], mat_name + '/alpha', Texture_Attribute(vector = True)) if 'roughness' in json else ''
        mat = compo.Physical_Material(eta = eta, alpha = alpha)
    elif mat_type == 'conductor' or mat_type == 'rough_conductor':
        if 'material' in json:
            eta = '/texture/eta/' + json['material']
            k = '/texture/k/' + json['material']
        else:
            eta = import_texture(json['ior'], mat_name + '/eta', Texture_Attribute(color = False))
            k = import_texture(json['k'], mat_name + '/k', Texture_Attribute(color = False))
        alpha = import_texture(json['roughness'], mat_name + '/alpha', Texture_Attribute(vector = True)) if 'roughness' in json else ''
        mat = compo.Physical_Material(eta = eta, k = k, alpha = alpha)
    elif mat_type == 'plastic' or mat_type == 'rough_plastic':
        reflectance = import_texture(json['albedo'], mat_name + '/reflectance', Texture_Attribute())
        eta = import_texture(json['ior'], mat_name + '/eta', Texture_Attribute(color = False))
        alpha = import_texture(json['roughness'], mat_name + '/alpha', Texture_Attribute(vector = True)) if 'roughness' in json else ''
        mat = compo.Physical_Material(reflectance = reflectance, eta = eta, alpha = alpha)
    else:
        print(f'material {mat_name} with type {mat_type} not supported')
        sys.exit(1)

    mat_path = '/material/' + mat_name
    materials[mat_path] = compo.json(
        entity = mat_path,
        type = type(mat).__name__.lower(),
        serialized = mat
    )
    return mat_path

