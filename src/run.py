import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.event_system import EventSystem
from lib.engine.game import Game
from src.game import MyGame

from lib.engine.engine import Entity, EntityList
from lib.math import *
import src.globals as globals


import src.globals as globals
from config.config import Configuration

globals.config = Configuration("config/config.json")

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
p1 = Point([0, 0, 0])
cs = CoordinateSystem(p1, vs)
globals.cs = cs


g = MyGame(cs)
es = EventSystem({"move": [g.get_camera().move], "rotate": [g.get_camera().planar_rotate]})
g.es = es


canv = g.get_canvas()()

camera = g.camera(Point([0, 0, 1]), draw_distance=100, fov=100,
                                        direction=Vector([-1, -1, -1]))

# rays = camera.get_rays_matrix(globals.config["canvas"]["n"], globals.config["canvas"]["m"])

obj = g.get_hyperellipsoid()(position=Point([0, 0, 0]), 
                               direction=Vector([2, 1, 1]), 
                               semiaxes=[1, 1, 1])

obj = g.get_hyperplane()(Point([-100, 1, 2]), normal=Vector([-100, 1, 1]))

canv.update(camera)

g.run(canv, camera)










# es.trigger("move", camera, Vector([1, 1, 1]))

# print(camera.position)

# a = camera.get_rays_matrix(globals.config["canvas"]["n"], globals.config["canvas"]["m"])

# myg = MyGame(cs)

# canv = myg.get_canvas()()

# obj = myg.get_hyperellipsoid()(position=Point([0, 0, 0]), 
#                                direction=Vector([2, 1, 1]), 
#                                semiaxes=[1, 1, 1])

# obj = myg.get_hyperplane()(Point([-100, 1, 2]), normal=Vector([-100, 1, 1]))


# canv.update(camera)


'''
1. действия над камерой
    - перемещение
    - поворот в двух плоскостях
'''
