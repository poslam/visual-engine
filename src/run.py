import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from lib.engine.engine import Ray


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

camera = g.camera(position=Point([-100, -100, 1]), direction=Vector([1, 1, 0]))

obj = g.get_hyperellipsoid()(position=Point([200, 200, 5]), 
                               direction=Vector([2, 1, 1]), 
                               semiaxes=[1, 1, 1])

obj2 = g.get_hyperellipsoid()(position=Point([198, 204, -10]), 
                               direction=Vector([2, 1, 1]), 
                               semiaxes=[1, 4, 3])

obj3 = g.get_hyperellipsoid()(position=Point([500, 500, -2]), 
                               direction=Vector([2, 5, 2]), 
                               semiaxes=[1, 5, 2])

canv.update(camera)

g.run(canv, camera)