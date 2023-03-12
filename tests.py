from classes import *

base = VectorSpace(
    initial_point=Point(0, 0, 0),
    e1=Vector(2, 3, 5),
    e2=Vector(0, 1, 0),
    e3=Vector(0, 0, 1)
)
    
point1 = Point(1, 1, 1)
point2 = Point(2, 2, 2)
point3 = Point(23, 2, 2)

vec1 = Vector(point1)
vec2 = Vector(c1=3, c2=2, c3=2)
vec3 = Vector(31, 32, 33)

obj = Object(
    position=Point(1, 1, 1),
    rotation = vec3,
    obj_points=[point2]
)


# distance
print("distance:", Point.distance(point1, point3))

# point + point
point = point1+point2
print("add of points:", point.as_list())

# point * scalar
point = point1*33
print("point * scalar:", point.as_list())

# point - point
point = point1 - point2
print("point - point: ", point.as_list())

# point / scalar
point = point1 / 3
print("point / scalar: ", point.as_list())

# length of vec
vec = vec1.len(base)
print("length of vec: ", vec)

# vec + vec
vec = vec1 + vec2
print("vec + vec: ", vec.as_list())

# vec * scalar
vec = vec1 * 2
print("vec * scalar: ", vec.as_list())

# vec * vec, скалярное произведение
vec = vec1 * vec2
print("vec * vec, скалярное произведение: ", vec)

# vec ** vec, векторное произведение
vec = vec1 ** vec2
print("vec ** vec, векторное произведение: ", vec.as_list())

# mixed_mul, смешанное произведение
print("смешанное произведение: ", Vector.mixed_mul(vec1, vec2, vec3))

# нормирование вектора
vec3 = vec3.norm(base)
print("нормирование вектора: ", vec3.as_list(), vec3.len(base))