from ..metatron import compo, shared
from ..metatron.linalg import vec3, quat_mul, quat_conj, normalize
from .bsdf import Texture_Attribute, import_bsdf, import_texture, materials
from .transform import import_transform, transforms
from typing import cast
import math
import re
import os

index: int = 0
shapes: dict[str, compo.json] = {}
lights: dict[str, compo.json] = {}
dividers: dict[str, compo.json] = {}


def import_primitve(json):
    global index
    name = (
        json["bsdf"] if "bsdf" in json and isinstance(json["bsdf"], str) else str(index)
    )
    if "/divider/" + name in dividers:
        for i in range(0, 100):
            if "/divider/" + name + str(i) not in dividers:
                name = name + str(i)
                break

    prim_type = json["type"]
    index = index + 1 if name == str(index) else index
    mat_path = (
        import_bsdf(json["bsdf"], name) if "bsdf" in json else "/material/" + name
    )

    if prim_type != "infinite_sphere_cap" and "power" in json:
        if prim_type == "infinite_sphere":
            emission_scale = 1 / (4 * math.pi)
        else:
            emission_scale = 0
        json["emission"] = json["power"] * emission_scale

    if "emission" in json:
        emission = import_texture(
            json["emission"],
            name + "/emission",
            Texture_Attribute(
                type="illuminant",
                distr="illuminant" if prim_type == "infinite_sphere" else "uniform",
            ),
        )
        if prim_type not in ("infinite_sphere", "infinite_sphere_cap", "skydome"):
            material = cast(compo.Material, materials[mat_path].serialized)
            if isinstance(material, compo.Physical_Material):
                material.emission = emission
            else:
                print(f"material of primitive {name} does not support emisson")

    if prim_type == "infinite_sphere":
        light_path = "/hierarchy/light/env"
        lights[light_path] = compo.json(
            entity=light_path,
            type=compo.Environment_Light.__name__.lower(),
            serialized=compo.Environment_Light(
                env_map="/texture/" + name + "/emission",
            ),
        )
        import_transform(json["transform"], light_path)
        return
    elif prim_type == "infinite_sphere_cap":
        light_path = "/hierarchy/light/sky"
        import_transform(json["transform"], light_path)
        t = transforms[light_path].serialized

        direction = (0, 0)
        aperture = 0
        if isinstance(t, compo.Local_Transform):
            rotation = t.rotation
            t.rotation = (0, 0, 0, 1)
            position = quat_mul(quat_mul(rotation, (0, 1, 0, 0)), quat_conj(rotation))
            position = normalize(position[:3])
            theta = math.acos(position[1])
            phi = math.atan2(position[2], position[0])
            phi += 2 * math.pi if phi < 0 else 0
            direction = (theta, phi)
        if "cap_angle" in json:
            aperture = math.radians(json["cap_angle"]) * 2

        if light_path in lights:
            light = lights[light_path].serialized
            if isinstance(light, compo.Sunsky_Light):
                light.direction = direction
                light.aperture = aperture
        else:
            light = compo.Sunsky_Light(
                direction=direction,
                turbidity=1,
                albedo=0,
                aperture=aperture,
                temperature=6504,
                intensity=1,
            )
            lights[light_path] = compo.json(
                entity=light_path,
                type=type(light).__name__.lower(),
                serialized=light,
            )
        return
    elif prim_type == "skydome":
        light_path = "/hierarchy/light/sky"
        if light_path in lights:
            light = cast(compo.Sunsky_Light, lights[light_path].serialized)
            light.turbidity = json["turbidity"]
            light.albedo = 0.2
            light.temperature = json["temperature"]
            light.intensity = json["intensity"]
        else:
            light = compo.Sunsky_Light(
                direction=(0, 0),
                turbidity=json["turbidity"],
                albedo=0.2,
                aperture=0,
                temperature=json["temperature"],
                intensity=json["intensity"],
            )
            lights[light_path] = compo.json(
                entity=light_path,
                type=type(light).__name__.lower(),
                serialized=light,
            )
        return

    shape_path = "/shape/" + name
    if prim_type == "mesh":
        os.makedirs(shared.output_dir + "model", exist_ok=True)
        input_path = json["file"]
        output_path = re.sub(r"wo3", "obj", input_path)
        output_path = re.sub(r"models", "model", output_path)
        shape = compo.Mesh(
            path=output_path,
        )
    else:
        print(f"primitive {name} with type {prim_type} not supported")
        return
    shapes[shape_path] = compo.json(
        entity=shape_path,
        type=type(shape).__name__.lower(),
        serialized=shape,
    )

    transform_path = "/hierarchy/shape/" + name
    import_transform(json["transform"], transform_path)
    div = compo.Divider(
        shape=shape_path,
        material=mat_path,
        local_to_render=transform_path,
    )
    if "int_medium" in json:
        div.int_medium = "/medium/" + json["int_medium"]
        div.int_to_render = "/hierarchy/medium/" + json["int_medium"]
    if "ext_medium" in json:
        div.ext_medium = "/medium/" + json["ext_medium"]
        div.ext_to_render = "/hierarchy/medium/" + json["ext_medium"]

    div_path = "/divider/" + name
    dividers[div_path] = compo.json(
        entity=div_path,
        type="divider",
        serialized=div,
    )
