from ..metatron import compo
from .transform import import_transform

cameras: dict[str, compo.json] = {
    '/hierarchy/camera': compo.json(
        entity='/hierarchy/camera',
        type='camera',
        serialized={},
    ),
}

tracers: dict[str, compo.json] = {
    '/tracer': compo.json(
        entity='/tracer',
        type='tracer',
        serialized={},
    ),
}

def import_camera(json):
    camera_path = '/hierarchy/camera'
    import_transform(json['camera']['transform'], camera_path)
