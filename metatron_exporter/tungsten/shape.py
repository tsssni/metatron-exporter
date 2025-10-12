from ..metatron import compo, shared
from ..metatron.linalg import *
from .material import import_material, materials, import_texture
from .light import lights
from .transform import import_transform, transforms
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
    light_types = ('infinite_sphere', 'infinite_sphere_cap', 'skydome')
    type = json['type']
    if 'bsdf' in json:
        mat_path = import_material(json['bsdf'], index)

    if type != 'infinite_sphere_cap' and 'power' in json:
        if type == 'infinite_sphere':
            emission_scale = 1 / (4 * math.pi)
        else:
            emission_scale = 0
        json['emission'] = json['power'] * emission_scale

    if 'emission' in json:
        emission = import_texture(
            json['emission'],
            str(index) + '/emission',
            spectype='illuminant',
            isenv=type=='infinite_sphere'
        )
        if type not in light_types:
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
        instance_path = '/hierarchy/light/sky'
        import_transform(json['transform'], instance_path)
        t = transforms[instance_path].serialized

        direction = (0, 0)
        aperture = 0
        if isinstance(t, compo.Local_Transform):
            rotation = t.rotation
            t.rotation = (0, 0, 0, 1)
            position = quat_mul(quat_mul(rotation, (0, 1, 0, 0)), quat_conj(rotation))
            position = normalize(vec3(position))
            theta = math.acos(position[1])
            phi = math.atan2(position[2], position[0])
            if phi < 0:
                phi += 2 * math.pi
            direction = (theta, phi)
        if 'cap_angle' in json:
            aperture = math.radians(json['cap_angle']) * 2

        if instance_path in lights:
            light = lights[instance_path].serialized
            if isinstance(light, compo.Sunsky_Light):
                light.direction = direction
                light.aperture = aperture
            lights[instance_path].serialized = light
        else:
            lights[instance_path] = compo.json(
                entity=instance_path,
                type='light',
                serialized=compo.Sunsky_Light(
                    direction=direction,
                    turbidity=1,
                    albedo=0,
                    aperture=aperture,
                    temperature=6504,
                    intensity=1,
                ),
            )
        return
    elif type == 'skydome':
        instance_path = '/hierarchy/light/sky'
        if instance_path in lights:
            light = lights[instance_path].serialized
            if isinstance(light, compo.Sunsky_Light):
                light.turbidity = json['turbidity']
                light.albedo = 0.2
                light.temperature = json['temperature']
                light.intensity = json['intensity']
            lights[instance_path].serialized = light
        else:
            lights[instance_path] = compo.json(
                entity=instance_path,
                type='light',
                serialized=compo.Sunsky_Light(
                    direction=(0,0),
                    turbidity=json['turbidity'],
                    albedo=0.2,
                    aperture=0,
                    temperature=json['temperature'],
                    intensity=json['intensity'],
                ),
            )
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

