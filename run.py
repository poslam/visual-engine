from random import randint
from lib.engine.game import Game
from src.game import MyGame

from lib.engine.engine import Entity, EntityList
from lib.math import *
import src.globals as globals

import curses
from curses import wrapper

n, m = 60, 200
# n, m = 10, 10

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
p1 = Point([0, 0, 0])
cs = CoordinateSystem(p1, vs)

globals.cs = cs

g = Game(cs, EntityList(Entity))

camera = g.camera(Point([-1000, -1000, -1000]), draw_distance=100, fov=100,
                                        direction=Vector([-1, -1, -1]))

a = camera.get_rays_matrix(n, m)

x = Entity(cs)
x.pravo = "slavno"

myg = MyGame(cs)

canv = myg.get_canvas()(n, m)


obj = myg.get_hyperellipsoid()(position=Point([0, 0, 0]), 
                               direction=Vector([2, 1, 1]), 
                               semiaxes=[1, 1, 1])

# obj = myg.get_hyperplane()(Point([-100, -100, -100]), normal=Vector([1, 1, 1]))


canv.update(camera)

matr = canv.distances.copy()

print(matr)

out_matr = Matrix.zero_matrix(n, m)

for i in range(n):
    for j in range(m):
        x = matr[i][j]
        if x == 0:
            out_matr[i][j] = ' '
        elif x < 10:
            out_matr[i][j] = '+'
        elif x < 20:
            out_matr[i][j] = '*'
        elif x < 30:
            out_matr[i][j] = '%'
        else:
            out_matr[i][j] = ';'

def main(stdscr):
    stdscr.clear()
    
    for i in range(n):
        for j in range(m):
            stdscr.addch(i, j, out_matr[i][j])
            
    # key = stdscr.getkey()
    # if key == 'd' or key == 'в':
    #     for i in range(n):
    #         for j in range(m):
    #             stdscr.addch(i, j, matr2[i][j])
    # stdscr.addch(59, 0, key)
    
    stdscr.refresh()
    stdscr.getch()

wrapper (main)