vec2 = tuple[float, float]
vec3 = tuple[float, float, float]
vec4 = tuple[float, float, float, float]
mat2 = tuple[vec2, vec2]
mat3 = tuple[vec3, vec3, vec3]
mat4 = tuple[vec4, vec4, vec4, vec4]

vecable = int | float | list[int] | list[float]

def isvecable(value):
      return isinstance(value, (int, float)) or (
          isinstance(value, list) and
          len(value) > 0 and
          all(isinstance(x, (int, float)) for x in value)
      )

def to_list(x: vecable, n: int) -> list[float]:
    if not isinstance(x, list):
        return [float(x) for _ in range(n)]
    else:
        return [float(y) for y in x]

def to_vec2(x: vecable) -> vec2:
    return vec2(to_list(x, 2))
def to_vec3(x: vecable) -> vec3:
    return vec3(to_list(x, 3))
def to_vec4(x: vecable) -> vec4:
    return vec4(to_list(x, 4))
