from curses import wrapper
from typing import Union

import src.globals as globals
from lib.engine.engine import EntityList, Ray
from lib.engine.game import Game
from lib.exceptions.engine_exc import EngineException
from lib.math.cs import CoordinateSystem
from lib.math.matrix_vector import Matrix, Vector
from lib.math.point import Point
from src.event_system import EventSystem


@property
def restricted(self):
    raise AttributeError(f'{self.__class__} does not have this attribite')


class MyGame(Game):
    def __init__(self, cs: CoordinateSystem, es: EventSystem = None, entities: EntityList = None):
        if entities == None:
            entities = EntityList()
        super().__init__(cs, es, entities)

    def run(self, canvas, camera):        
        def main(stdscr):
            stdscr.clear() 
            
            k, p = 0, 0
                    
            while True:
                stdscr.addstr(61, 200, f"camera at: {str(camera.position.values)}")
                stdscr.addstr(62, 200, f"camera direction: {str(camera.direction.values)}")
                
                canvas.update(camera)
                
                matr = canvas.out_matr
                
                for i in range(matr.rows):
                    for j in range(matr.columns):
                        stdscr.addch(i, j, matr[i][j]) 
            
                key = stdscr.getkey() 
                if key == "l":
                    break
                if key == "w":
                    dist = camera.direction*10
                    dist[2] = 0
                    self.es.trigger("move", camera, dist)
                    k += 1
                    stdscr.addstr(59, 200, f"{k} move complete")
                elif key == "s":
                    dist = (-1)*camera.direction*10
                    dist[2] = 0
                    self.es.trigger("move", camera, dist)
                    k += 1
                    stdscr.addstr(59, 200, f"{k} move complete")
                elif key == "a":
                    self.es.trigger("move", camera, 10*Vector.vector_product(camera.direction, Vector([0, 0, -1])))
                    k += 1
                    stdscr.addstr(59, 200, f"{k} move complete")
                elif key == "d":
                    self.es.trigger("move", camera, 10*Vector.vector_product(camera.direction, Vector([0, 0, 1])))
                    k += 1
                    stdscr.addstr(59, 200, f"{k} move complete")
                elif key == "KEY_UP":
                    self.es.trigger("rotate", camera, [0, 2], 20)
                    self.es.trigger("rotate", camera, [1, 2], 20)
                    p += 1
                    stdscr.addstr(60, 200, f"{p} rotate complete")
                elif key == "KEY_DOWN":
                    self.es.trigger("rotate", camera, [0, 2], -20)
                    self.es.trigger("rotate", camera, [1, 2], -20)
                    p += 1
                    stdscr.addstr(60, 200, f"{p} rotate complete")
                elif key == "KEY_RIGHT":
                    self.es.trigger("rotate", camera, [0, 1], -30)
                    p += 1
                    stdscr.addstr(60, 200, f"{p} rotate complete")
                elif key == "KEY_LEFT":
                    self.es.trigger("rotate", camera, [0, 1], 30)
                    p += 1
                    stdscr.addstr(60, 200, f"{p} rotate complete")
                

        wrapper (main)

    def get_hyperplane(self):
        class HyperPlane(self.object):
            def __init__(pself, position: Point, normal: Vector):
                if not isinstance(position, Point):
                    raise EngineException(EngineException.WRONG_INPUT("Point"))

                if not isinstance(normal, Vector):
                    raise EngineException(
                        EngineException.WRONG_INPUT("Vector"))

                super().__init__(position)

                pself.position = position
                pself.normal = normal.norm()

                self.entities.append(pself)

            def planar_rotate(self, inds: list[int], angle: Union[int, float]):
                normal = self.normal.rotate(inds, angle)
                self.normal = normal

            def rotate_3d(self, angles: list[Union[int, float]]):
                normal = self.normal.rotate_3d(angles)
                self.normal = normal

            def intersection_distance(self, ray: Ray):
                ray_inp_vec = Vector([x for x in ray.initpoint.values])
                pos_vec = Vector([x for x in self.position.values])
                dim = ray.direction.size

                t = -((self.normal & (ray_inp_vec-pos_vec)) /
                      (self.normal & ray.direction))

                temp_vec = Vector([ray_inp_vec[i]+ray.direction[i]*t
                                   for i in range(dim)])

                return round(temp_vec.len(), globals.config["precision"])

            move = restricted

        return HyperPlane

    def get_hyperellipsoid(self):
        class HyperEllipsoid(self.object):
            def __init__(pself, position: Point, direction: Vector, semiaxes: list[float]):
                if not isinstance(position, Point):
                    raise EngineException(EngineException.WRONG_INPUT(Point))

                if not isinstance(direction, Vector):
                    raise EngineException(EngineException.WRONG_INPUT(Vector))

                super().__init__(position, direction)
                pself.semiaxes = semiaxes
                self.entities.append(pself)

            def planar_rotate(self, inds: list[int], angle: Union[int, float]):
                direction = self.direction.rotate(inds, angle)
                self.set_direction(direction)

            def rotate_3d(self, angles: list[Union[int, float]]):
                direction = self.direction.rotate_3d(angles)
                self.set_direction(direction)

            def intersection_distance(self, ray: Ray):
                dir, pos = ray.direction, ray.initpoint-self.position
                dim = ray.direction.size

                p1 = sum(dir[i]**2/self.semiaxes[i]**2 for i in range(dim))
                p2 = sum(2*pos[i]*dir[i]/self.semiaxes[i]
                         ** 2 for i in range(dim))
                p3 = sum(pos[i]**2/self.semiaxes[i]**2 for i in range(dim)) - 1

                t1 = (-p2 + (p2**2-4*p1*p3)**0.5)/2*p1
                t2 = (-p2 - (p2**2-4*p1*p3)**0.5)/2*p1

                t = [x for x in [y for y in [t1, t2]
                                 if isinstance(y, (int, float))] if x > 0]

                if len(t) == 0:
                    return 0

                t = min(t)

                intersection_vec = Vector([ray.initpoint[i]+dir[i]*t
                                           for i in range(dim)])

                temp = pos.as_vector()

                return round((intersection_vec-temp).len(), globals.config["precision"])

        return HyperEllipsoid

    def get_canvas(self):
        class Canvas:
            def __init__(self, n: int = None, m: int = None):
                if n != None:
                    self.n = n
                else:
                    self.n = globals.config["canvas"]["n"]
                if m != None:
                    self.m = m
                else:
                    self.m = globals.config["canvas"]["m"]
                self.distances = Matrix.zero_matrix(self.n, self.m)
                self.out_matr = None

            def update(pself, camera: self.get_camera()):
                rays = camera.get_rays_matrix(pself.n, pself.m)

                for i in range(pself.n):
                    for j in range(pself.m):
                        result = []
                        for ent in self.entities:
                            result.append(
                                ent.intersection_distance(rays[i][j]))
                        y = [z for z in result if z > 0]
                        if len(y) == 0:
                            y = 0
                        else:
                            y = min(y)
                        pself.distances[i][j] = y
                        
                charmap = globals.config["charmap"]
                l = len(charmap)
                draw_distance = globals.config["camera"]["draw_distance"]
                
                step = draw_distance / l    
                list_steps = [step*i for i in range(l)]
                
                matr = pself.distances
                
                out_matr = Matrix.zero_matrix(pself.n, pself.m)
                
                for i in range(pself.n):
                    for j in range(pself.m):
                        for k in range(l):
                            if matr[i][j] == 0 or \
                                matr[i][j] > draw_distance:
                                out_matr[i][j] = ' '
                                break
                            if matr[i][j] < list_steps[k]:
                                out_matr[i][j] = charmap[k]
                                break
                            
                pself.out_matr = out_matr

        return Canvas