from random import randint
from src.game import Game
from lib.engine.engine import Entity, EntityList, Ray
from lib.math import *
import src.globals as globals

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
p1 = Point([0, 0, 0])
cs = CoordinateSystem(p1, vs)

globals.cs = cs

# v1 = Vector([1, 1, 1])
# for i in range(5):
#     vec = v1.copy()
#     vec.rotate([0, 1], i*10)
#     print(vec, v1)

camera = Game(cs, EntityList(Entity)).camera(p1, draw_distance=100, fov=120,
                                        direction=Vector([2, 3, 1]))

a = camera.get_rays_matrix(10, 10)


for i in a:
    for j in i:
        print(j.initpoint, j.direction) 


# r = Ray(globals.cs, p1, Vector([1, 1, 1]))
# print(r.direction)