# from random import randint
# from lib.engine.game import Game
# from src.game import MyGame

# from lib.engine.engine import Entity, EntityList
# from lib.math import *
# import src.globals as globals

# vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
# p1 = Point([0, 0, 0])
# cs = CoordinateSystem(p1, vs)

# globals.cs = cs



# g = Game(cs, EntityList(Entity))

# camera = g.camera(Point([0, 0, 0]), draw_distance=100, fov=100,
#                                         direction=Vector([200, 20, 1]))

# a = camera.get_rays_matrix(10, 10)

# x = Entity(cs)
# x.pravo = "slavno"

# myg = MyGame(cs)

# canv = myg.get_canvas()(10, 10)


# obj = myg.get_hyperellipsoid()(position=Point([1000, 200, 200]), 
#                                direction=Vector([2, 1, 89]), 
#                                semiaxes=[100, 200, 50])
# # for i in a:
# #     for j in i:
# #         print(obj.intersection_distance(j))

# # print("xyz")

# obj = myg.get_hyperplane()(Point([-100, -100, -100]), normal=Vector([1, 1, 1]))

# # for i in a:
# #     for j in i:
# #         print(obj.intersection_distance(j))

# canv.update(camera)

# print(canv.distances)


# # for i in myg.entities:
# #     print(i.intersection_distance(a[0][0]))

# # print(myg.entities))

from config.config import Configuration

c = Configuration(filepath="config/config.json")

