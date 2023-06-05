from random import randint
from lib.engine.game import Game
from src.game import MyGame

from lib.engine.engine import Entity, EntityList
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

g = Game(cs, EntityList(Entity))

camera = g.camera(Point([0, 0, 0]), draw_distance=100, fov=100,
                                        direction=Vector([1, 1, 1]))

a = camera.get_rays_matrix(10, 10)

myg = MyGame(cs, EntityList(Entity))

# obj = myg.get_hyperellipsoid()(position=Point([200, 200, 200]), 
#                                direction=Vector([2, 1, 89]), 
#                                semiaxes=[100, 200, 50])

obj = myg.get_hyperplane()(Point([1000, 1000, 1000]), normal=Vector([1, 1, 1]))

for i in a:
    for j in i:
        x = obj.intersection_distance(j)
        print(j.direction, x)


# for i in a:
#     for j in i:
#         print(j.direction)

# r = Ray(globals.cs, p1, Vector([1, 1, 1]))
# print(r.direction)