import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.event_system import EventSystem    
from src.game import MyGame

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
es = EventSystem({"move": [g.get_camera().move], "rotate_hor": [g.get_camera().planar_rotate],
                  "rotate_ver": [g.camera.set_direction]})
g.es = es


canv = g.get_canvas()()

camera = g.camera(Point([0, 0, 5]), draw_distance=100, fov=100,
                                        direction=Vector([1, 1, 0.1]))

obj = g.get_hyperellipsoid()(position=Point([1, 1, 10]), 
                               direction=Vector([2, 1, 1]), 
                               semiaxes=[10, 50, 20])

obj = g.get_hyperplane()(Point([0, 0, 0 ]), normal=Vector([0, 1, 1]))

canv.update(camera)

# print(canv.distances)
# g.run(canv, camera)

print(Vector([-0.95399, 0.29166, 0.06954]).vector_product(Vector([0, 0, 1])))