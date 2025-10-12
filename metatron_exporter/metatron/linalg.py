from typing import cast
import math

vec2 = tuple[float, float]
vec3 = tuple[float, float, float]
vec4 = tuple[float, float, float, float]
mat2 = tuple[vec2, vec2]
mat3 = tuple[vec3, vec3, vec3]
mat4 = tuple[vec4, vec4, vec4, vec4]

vecable = int | float | list[int] | list[float]
vec = vec2 | vec3 | vec4
mat = mat2 | mat3 | mat4

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

def to_vec(x: vecable, n: int = 1):
    if isinstance(x, list):
        n = len(x)
    return tuple(to_list(x, n))

def to_vec2(x: vecable) -> vec2:
    return cast(vec2, to_vec(x, 2))

def to_vec3(x: vecable) -> vec3:
    return cast(vec3, to_vec(x, 3))

def to_vec4(x: vecable) -> vec4:
    return cast(vec4, to_vec(x, 4))

def plus(x, y):
    n = len(x)
    return to_vec([x[i] + y[i] for i in range(n)])

def minus(x, y):
    n = len(x)
    return to_vec([x[i] - y[i] for i in range(n)])

def normalize(x):
    l = sum([s**2 for s in x])
    return to_vec([s / l for s in x]) if l > 0.0 else x

def cross(x, y):
    return (
        x[1] * y[2] - x[2] * y[1],
        x[2] * y[0] - x[0] * y[2],
        x[0] * y[1] - x[1] * y[0],
    )

def quat_mul(q0: vec4, q1: vec4) -> vec4:
    x, y, z, w = q0
    rx, ry, rz, rw = q1
    return (
        w * rx + x * rw + y * rz - z * ry,
        w * ry + y * rw + z * rx - x * rz,
        w * rz + z * rw + x * ry - y * rx,
        w * rw - x * rx - y * ry - z * rz,
    )

def quat_conj(q: vec4) -> vec4:
    return (-q[0], -q[1], -q[2], q[3])

def euler_yxz_to_quat(euler: vec3) -> vec4:
    hx, hy, hz = (math.radians(euler[i]) * 0.5 for i in range(3))
    qx = (math.sin(hx), 0.0, 0.0, math.cos(hx))
    qy = (0.0, math.sin(hy), 0.0, math.cos(hy))
    qz = (0.0, 0.0, math.sin(hz), math.cos(hz))
    return quat_mul(qz, quat_mul(qx, qy))
