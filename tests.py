from classes import *

base = VectorSpace(
    initial_point=Point(0, 0, 0),
    e1=Vector(2, 3, 5),
    e2=Vector(0, 1, 0),
    e3=Vector(0, 0, 1)
    )
    

# point1 = VectorSpace().initial_point
    
point1 = Point(1, 1, 2)
point2 = Point(23, 2, 2)

vec1 = Vector(
    point1
)

vec2 = Vector(
    c1=3, c2=2, c3=2
)

vec3 = Vector(
    c1=32, c2=33, c3=21
)

obj = Object(
    position=Point(1, 1, 1 ),
    rotation = vec3,
    obj_points=[point2]
)

print(obj.contains(point2))