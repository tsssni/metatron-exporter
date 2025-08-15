from ..metatron import compo
from ..metatron.linalg import *

spectra: list[compo.json] = []

def import_spectrum(spec: int | float | list[int] | list[float], type: str):
    return compo.Rgb_Spectrum(
        c=to_vec3(spec),
        type=type,
        color_space='/color-space/sRGB',
    )
