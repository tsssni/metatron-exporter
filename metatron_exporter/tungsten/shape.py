from ..metatron import compo, shared
from .material import import_material, materials, import_texture, textures
from .light import lights
from .transform import import_transform
from typing import cast
import math
import copy
import re
import os

index: int = 0
shapes: dict[str, compo.json] = {}
shape_instances: dict[str, compo.json] = {}
dividers: dict[str, compo.json] = {}

def import_shape(json):
    global index
    type = json['type']
    if 'bsdf' in json:
        mat_path = import_material(json['bsdf'], index)

    if type == 'skydome':
        json['emission'] = [0.03, 0.07, 0.23]
        type = 'infinite_sphere'

    if 'power' in json:
        if type == 'infinite_sphere':
            emission_scale = 1 / (4 * math.pi)
        elif type == 'infinite_sphere_cap':
            emission_scale = 1 / (2 * math.pi * (1 - math.cos(json['cap_angle'])))
        else:
            emission_scale = 0
        json['emission'] = json['power'] * emission_scale

    if 'emission' in json:
        emission = import_texture(
            json['emission'],
            str(index) + '/emission',
            spectype='illuminant',
        )
        if type == 'infinite_sphere_cap':
            textures.pop('/texture/' + str(index) + '/emission')
        elif type != 'infinite_sphere':
            material = copy.deepcopy(cast(compo.Material, materials[mat_path].serialized))
            material.spectrum_textures['emission'] = emission
            mat_path = '/material/' + str(index)
            materials[mat_path] = compo.json(
                entity=mat_path,
                type='material',
                serialized=material,
            )

    if type == 'infinite_sphere':
        instance_path = '/hierarchy/light/' + str(index)
        lights[instance_path] = compo.json(
            entity=instance_path,
            type='light',
            serialized=compo.Environment_Light(
                env_map='/texture/' + str(index) + '/emission',
            ),
        )
        import_transform(json['transform'], instance_path)
        index = index + 1
        return
    elif type == 'infinite_sphere_cap':
        instance_path = '/hierarchy/light/' + str(index)
        lights[instance_path] = compo.json(
            entity=instance_path,
            type='light',
            serialized=compo.Parallel_Light(
                spectrum='/spectrum/' + str(index) + '/emission',
            ),
        )
        import_transform(json['transform'], instance_path, (0.7071, 0, 0, 0.7071))
        index = index + 1
        return
    else:
        instance_path = '/hierarchy/shape/' + str(index)

    shape_path = '/shape/' + str(index)
    if type == 'mesh':
        os.makedirs(shared.output_dir + 'model', exist_ok=True)
        input_path = json['file']
        output_path = re.sub(r'wo3', 'obj', input_path)
        output_path = re.sub(r'models', 'model', output_path)
        shape = compo.Mesh(
            path = output_path,
        )
    else:
        return
    shapes[shape_path] = compo.json(
        entity=shape_path,
        type='shape',
        serialized=shape,
    )

    shape_instances[instance_path] = compo.json(
        entity=instance_path,
        type='shape_instance',
        serialized=compo.Shape_Instance(
            path = shape_path,
        ),
    )

    div = compo.Divider(
        shape=instance_path,
        material=mat_path,
    )
    if 'int_medium' in json:
        div.int_medium = '/hierarchy/medium/' + json['int_medium']
    if 'ext_medium' in json:
        div.ext_medium = '/hierarchy/medium/' + json['ext_medium']

    div_path = '/divider/' + str(index)
    dividers[div_path] = compo.json(
        entity=div_path,
        type='divider',
        serialized=div,
    )

    import_transform(json['transform'], instance_path)
    index = index + 1

