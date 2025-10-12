from metatron_exporter.metatron.format import compress, MetatronJSONEncoder
import os
import argparse
import json

def path_norm(path: str):
    if path.endswith(os.sep):
        return path
    else:
        return path + os.sep

def main():
    argparser = argparse.ArgumentParser(description='format scene.json file in scene directory')
    argparser.add_argument('-s', '--scene', type=str, default='./', help='directory contains scene.json')
    args = argparser.parse_args()

    scene_dir = path_norm(args.scene)
    scene_file = os.path.join(scene_dir, 'scene.json')

    with open(scene_file, 'r') as f:
        data = json.load(f)
    processed_data = compress(data)

    encoder = MetatronJSONEncoder()
    formatted_json = encoder.encode(processed_data)

    with open(scene_file, 'w') as f:
        f.write(formatted_json)

if __name__ == '__main__':
    main()
