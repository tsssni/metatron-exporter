from .. import metatron
import json

def export():
    with open(metatron.scene_dir + 'scene.json', 'r') as f:
        return json.load(f)
