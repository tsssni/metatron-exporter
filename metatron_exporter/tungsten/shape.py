from metatron_exporter.tungsten.transform import import_transform
from ..metatron import compo
from .material import import_material, materials, import_texture
from .light import lights
from typing import cast
import copy

index: int = 0
shapes: dict[str, compo.json] = {}
shape_instances: dict[str, compo.json] = {}

def import_shape(json):
    global index
    type = json['type']
    if 'bsdf' not in json:
        material = compo.Material(
            bsdf=compo.Lambertian_Bsdf(), spectrum_textures={}, vector_textures={}
        ) 
    else:
        material = cast(compo.Material, materials[import_material(json['bsdf'], index)].serialized)

    if 'emission' in json or 'power' in json:
        emission = json['emission' if 'emission' in json else 'power']
        material = copy.deepcopy(material)
        material.spectrum_textures['emission'] = import_texture(
            emission, str(index) + '/emission', spectype='illuminant'
        )
        mat_path = '/material/' + str(index)
        if type != 'infinite_sphere':
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
    else:
        instance_path = '/hierarchy/shape/' + str(index)

    shape_path = '/shape/' + str(index)
    if type == 'mesh':
        shape = compo.Mesh(
            path = json['file'],
        )
    else:
        shape = compo.Sphere()
    shapes[shape_path] = compo.json(
        entity=shape_path,
        type='shape',
        serialized=shape,
    )

    if type != 'infinite_sphere':
        shape_instances[instance_path] = compo.json(
            entity=instance_path,
            type='shape_instance',
            serialized=compo.Shape_Instance(
                path = shape_path,
            ),
        )

    import_transform(json['transform'], instance_path)
    index = index + 1

