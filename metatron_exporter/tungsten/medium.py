from .spectrum import *
from .transform import *
from ..metatron import compo
import sys

media: dict[str, compo.json] = {}
medium_instances: dict[str, compo.json] = {}

def import_phase(json) -> compo.Phase_Function:
    if json['type'] == 'isotropic':
        return compo.Henyey_Greenstein_Phase_Function(g=0.0)
    elif json['type'] == 'henyey_greenstein':
        return compo.Henyey_Greenstein_Phase_Function(g=json['g'])
    else:
        print(f"{json['type']} phase function not supported")
        sys.exit(1)

def import_medium(json):
    sigma_a = import_spectrum(json['sigma_a'], 'unbounded')
    sigma_s = import_spectrum(json['sigma_s'], 'unbounded')
    sigma_e = import_spectrum([0,0,0], 'illuminant')

    sigma_a_path = '/spectrum/' + json['name'] + '/sigma-a'
    sigma_s_path = '/spectrum/' + json['name'] + '/sigma-s'
    sigma_e_path = '/spectrum/' + json['name'] + '/sigma-e'

    spectra[sigma_a_path] = compo.json(
        entity=sigma_a_path,
        type='spectrum',
        serialized=sigma_a,
    )
    spectra[sigma_s_path] = compo.json(
        entity=sigma_s_path,
        type='spectrum',
        serialized=sigma_s,
    )
    spectra[sigma_e_path] = compo.json(
        entity=sigma_e_path,
        type='spectrum',
        serialized=sigma_e,
    )

    if json['type'] == 'homogeneous':
        phase = import_phase(json['phase_function'])
        medium_path = '/medium/' + json['name']
        media[medium_path] = compo.json(
            entity=medium_path,
            type='medium',
            serialized=compo.Homogeneous_Medium(
                phase=phase,
                sigma_a=sigma_a_path,
                sigma_s=sigma_s_path,
                sigma_e=sigma_e_path,
            ),
        )
    else:
        print(f"{json['type']} medium not supported")
        sys.exit(1)

    instance_path = '/hierarchy/medium/' + json['name']
    medium_instances[instance_path] = compo.json(
        entity=instance_path,
        type = 'medium_instance',
        serialized=compo.Medium_Instance(
            path='/medium/' + json['name'],
        )
    )
    transforms[instance_path] = compo.json(
        entity=instance_path,
        type = 'transform',
        serialized=compo.Local_Transform(),
    )
