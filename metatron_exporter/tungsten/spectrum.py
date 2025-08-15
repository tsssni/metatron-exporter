from ..metatron import compo

spectra: list[compo.json] = []

def import_spectrum(spec: int | float | list[int] | list[float], type: str):
    if isinstance(spec, int) or isinstance(spec, float):
        spec = [float(spec) for _ in range(3)]
    return compo.Rgb_Spectrum(
        c=list[float](spec),
        type=type,
        color_space='/color-space/sRGB',
    )
