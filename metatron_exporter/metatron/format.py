import json


def compress(data, is_top_level: bool = True):
    if isinstance(data, list):
        if is_top_level:
            return [compress(item, False) for item in data]
        else:
            return [compress(item, False) for item in data]
    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, str) and value == "":
                continue
            if (
                key in ("int_medium", "ext_medium")
                and value == "/hierarchy/medium/vaccum"
            ):
                continue
            result[key] = compress(value, False)
        return result
    else:
        return data


class MetatronJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_indent_level = 0
        self.is_top_level_array = True

    def encode(self, o):
        if isinstance(o, list) and self.is_top_level_array:
            return self._encode_top_level_array(o)
        else:
            return super().encode(o)

    def _encode_top_level_array(self, array):
        if not array:
            return "[]"

        lines = ["["]
        for i, item in enumerate(array):
            item_json = self._encode_item(item, indent_level=1)
            if i < len(array) - 1:
                lines.append(f"    {item_json},")
            else:
                lines.append(f"    {item_json}")
        lines.append("]")
        return "\n".join(lines)

    def _encode_item(self, obj, indent_level: int = 0):
        if isinstance(obj, dict):
            return self._encode_dict(obj, indent_level)
        elif isinstance(obj, list):
            if len(obj) > 1:
                return json.dumps(obj, separators=(", ", ": "))
            else:
                return json.dumps(obj, separators=(",", ": "))
        else:
            return json.dumps(obj)

    def _encode_dict(self, obj, indent_level: int):
        if not obj:
            return "{}"

        indent = "    " * indent_level
        next_indent = "    " * (indent_level + 1)

        lines = ["{"]
        items = list(obj.items())
        for i, (key, value) in enumerate(items):
            value_str = self._encode_item(value, indent_level + 1)
            if i < len(items) - 1:
                lines.append(f'{next_indent}"{key}": {value_str},')
            else:
                lines.append(f'{next_indent}"{key}": {value_str}')
        lines.append(f"{indent}}}")
        return "\n".join(lines)
