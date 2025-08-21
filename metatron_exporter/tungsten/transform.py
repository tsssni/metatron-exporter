from ..metatron import compo
from ..metatron.linalg import *

transforms: dict[str, compo.json] = {}

def import_transform(json, path: str, extra_rot: vec4 = (0, 0, 0, 1)):
    t = compo.Local_Transform()
    if 'position' in json:
        # left hand z face inside
        position = json['position']
        position[2] = -position[2]
        t.translation = to_vec3(position)
    if 'scale' in json:
        t.scaling = to_vec3(json['scale'])
    if 'rotation' in json:
        # left hand x/y rotation is reversed
        rotation = json['rotation']
        rotation[0], rotation[1], rotation[2] = -rotation[0], -rotation[1], rotation[2]
        t.rotation = quat_mul(euler_yxz_to_quat(to_vec3(rotation)), extra_rot)
    if 'look_at' in json and 'up' in json:
        look_at = json['look_at']
        up = json['up']
        look_at[2] = -look_at[2]
        up[2] = -up[2]

        t = compo.Look_At_Transform(
            position = t.translation,
            look_at = to_vec3(look_at),
            up = to_vec3(up),
        )

    transforms[path] = compo.json(
        entity=path,
        type='transform',
        serialized=t,
    )
