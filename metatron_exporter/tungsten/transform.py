from ..metatron import compo
from ..metatron.linalg import *

transforms: dict[str, compo.json] = {}

def import_transform(json, path: str):
    t = compo.Local_Transform()
    if 'position' in json:
        # left hand z face inside
        json['position'][2] = -json['position'][2]
        t.translation = to_vec3(json['position'])
    if 'scale' in json:
        t.scaling = to_vec3(json['scale'])
    if 'rotation' in json:
        # left hand x/y rotation is reversed
        json['rotation'][0] = -json['rotation'][0]
        json['rotation'][1] = -json['rotation'][1]
        t.rotation = euler_yxz_to_quat(to_vec3(json['rotation']))
    if 'look_at' in json and 'up' in json:
        json['look_at'][2] = -json['look_at'][2]
        json['up'][2] = -json['up'][2]

        t = compo.Look_At_Transform(
            position = t.translation,
            look_at = to_vec3(json['look_at']),
            up = to_vec3(json['up']),
        )

    transforms[path] = compo.json(
        entity=path,
        type='transform',
        serialized=t,
    )
