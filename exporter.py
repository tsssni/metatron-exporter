from metatron_exporter.metatron import shared
from dataclasses import asdict
import os
import argparse
import json
import importlib

def path_norm(path: str):
    if (path.endswith(os.sep)):
        return path + os.sep
    else:
        return path

def main():
    argparser = argparse.ArgumentParser(description='export metatron scene from scene directory')
    argparser.add_argument('-s', '--scene', type=str, default = './', help='directory contains scene')
    argparser.add_argument('-o', '--output', type=str, default='./result/', help='directory to store the scene')
    argparser.add_argument('-r', '--renderer', type=str, choices=['tungsten'], default='tungsten', help='scene original renderer format')
    args = argparser.parse_args()

    shared.scene_dir = path_norm(args.scene);
    shared.output_dir = path_norm(args.output);

    renderer = importlib.import_module(f'metatron_exporter.{args.renderer}')
    scene = renderer.export()
    with open(shared.output_dir + 'scene.json', 'w') as f:
        json.dump([asdict(item) for item in scene], f, indent=4)


if __name__ == '__main__':
    main()
