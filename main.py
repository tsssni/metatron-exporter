from metatron_exporter import metatron
from metatron_exporter.metatron.compo import *
from dataclasses import asdict
import os
import argparse
import json
import importlib

class Metatron_Encoder(json.JSONEncoder):
    def default(self, o):
        return super().default(o)
    
    def encode(self, o):
        def preprocess(obj):
            if isinstance(obj, float) and obj.is_integer():
                return int(obj)
            elif isinstance(obj, list):
                return [preprocess(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: preprocess(v) for k, v in obj.items()}
            return obj
        
        processed = preprocess(o)
        result = super().encode(processed)
        
        import re
        def compress_numeric_arrays(text):
            pattern = r'\[\s*\n\s*((?:[0-9.\-+e]+(?:,\s*\n\s*)?)*[0-9.\-+e]+)\s*\n\s*\]'
            def replace_array(match):
                content = match.group(1)
                numbers = re.findall(r'[0-9.\-+e]+', content)
                processed_numbers = []
                for num in numbers:
                    if '.' in num and float(num).is_integer():
                        processed_numbers.append(str(int(float(num))))
                    else:
                        processed_numbers.append(num)
                return '[' + ', '.join(processed_numbers) + ']'
            return re.sub(pattern, replace_array, text)
        
        return compress_numeric_arrays(result)

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

    metatron.scene_dir = path_norm(args.scene);
    metatron.output_dir = path_norm(args.output);

    renderer = importlib.import_module(f'metatron_exporter.{args.renderer}')
    scene = renderer.export()
    print(json.dumps([asdict(item) for item in scene], cls=Metatron_Encoder, indent=4))


if __name__ == '__main__':
    main()
