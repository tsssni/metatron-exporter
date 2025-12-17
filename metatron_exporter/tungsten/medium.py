from .transform import transforms
from .bsdf import spectra
from ..metatron import compo
from ..metatron.linalg import to_vec3
import sys

media: dict[str, compo.json] = {}


def import_spectrum(spec: int | float | list[int] | list[float], type: str):
    return compo.Rgb_Spectrum(
        c=to_vec3(spec),
        type=type,
    )


def import_phase(json) -> compo.Phase:
    type = json["type"]
    if type == "isotropic":
        return compo.Phase(function="henyey_greenstein", g=0.0)
    elif type == "henyey_greenstein":
        return compo.Phase(function="henyey_greenstein", g=json["g"])
    else:
        print(f"phase function with type {type} not supported")
        sys.exit(1)


def import_medium(json):
    name = json["name"]

    sigma_a = import_spectrum(json["sigma_a"], "unbounded")
    sigma_s = import_spectrum(json["sigma_s"], "unbounded")
    sigma_a_path = "/spectrum/" + name + "/sigma-a"
    sigma_s_path = "/spectrum/" + name + "/sigma-s"
    spectra[sigma_a_path] = compo.json(
        entity=sigma_a_path,
        type=type(sigma_a).__name__.lower(),
        serialized=sigma_a,
    )
    spectra[sigma_s_path] = compo.json(
        entity=sigma_s_path,
        type=type(sigma_s).__name__.lower(),
        serialized=sigma_s,
    )

    med_type = json["type"]
    if med_type == "homogeneous":
        phase = import_phase(json["phase_function"])
        medium_path = "/medium/" + name
        medium = compo.Homogeneous_Medium(
            phase=phase,
            sigma_a=sigma_a_path,
            sigma_s=sigma_s_path,
        )
        media[medium_path] = compo.json(
            entity=medium_path,
            type=type(medium).__name__.lower(),
            serialized=medium,
        )
    else:
        print(f"medium with type {type} not supported")
        sys.exit(1)

    transform_path = "/hierarchy/medium/" + json["name"]
    transforms[transform_path] = compo.json(
        entity=transform_path,
        type=compo.Local_Transform.__name__.lower(),
        serialized=compo.Local_Transform(),
    )
