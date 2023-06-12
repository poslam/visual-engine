from curses import wrapper
from math import sqrt
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
                stdscr.addstr(61, 180, f"camera at: {str(camera.position.values)}")
                stdscr.addstr(62, 180, f"camera direction: {str(camera.direction.values)}")
                
                canvas.update(camera)
                
                matr = canvas.out_matr
                
                for i in range(matr.rows):
                    for j in range(matr.columns):
                        stdscr.addch(i, j, matr[i][j]) 
            
                key = stdscr.getkey() 
                if key == "l":
                    open('log.txt', 'w').close()
                    break
                if key == "w":
                    dist = camera.direction
                    self.es.trigger("move", camera, dist.norm()*30)
                    k += 1
                    stdscr.addstr(59, 180, f"{k} move complete")
                elif key == "s":
                    dist = (-1)*camera.direction
                    self.es.trigger("move", camera, dist.norm()*30)
                    k += 1
                    stdscr.addstr(59, 180, f"{k} move complete")
                elif key == "a":
                    self.es.trigger("move", camera, 5*Vector.vector_product(camera.direction, Vector([0, 0.2, 0])))
                    k += 1
                    stdscr.addstr(59, 180, f"{k} move complete")
                elif key == "d":
                    self.es.trigger("move", camera, 5*Vector.vector_product(camera.direction, Vector([0, -0.2, 0])))
                    k += 1
                    stdscr.addstr(59, 180, f"{k} move complete")
                elif key == "KEY_UP":
                    self.es.trigger("rotate_ver", camera, camera.direction-Vector([0, 0.005, 0]))
                    p += 1
                    stdscr.addstr(60, 180, f"{p} rotate complete")
                elif key == "KEY_DOWN":
                    self.es.trigger("rotate_ver", camera, camera.direction+Vector([0, 0.005, 0]))
                    p += 1
                    stdscr.addstr(60, 180, f"{p} rotate complete")
                elif key == "KEY_RIGHT":
                    self.es.trigger("rotate_hor", camera, [1, 2], -0.2)
                    p += 1
                    stdscr.addstr(60, 180, f"{p} rotate complete")
                elif key == "KEY_LEFT":
                    self.es.trigger("rotate_hor", camera, [1, 2], 0.2)
                    p += 1
                    stdscr.addstr(60, 180, f"{p} rotate complete")
                # with open("log.txt", 'w') as f:
                #     for i in canvas.distances:
                #         f.write(str(i)+'\n')
                #     f.close()
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
                ray_inp_vec = ray.initpoint.as_vector() # x^1
                pos_vec = self.position.as_vector() # x^0
                dim = ray.direction.size

                if (self.normal & ray.direction) == 0:
                    return 0

                t = -((self.normal & (ray_inp_vec-pos_vec)) /
                      (self.normal & ray.direction))
                
                if t <= 0:
                    return 0

                temp_vec = Vector([ray_inp_vec[i]+ray.direction[i]*t
                                   for i in range(dim)])

                return round(temp_vec.len(), globals.config["precision"])/2

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
                A, B, C, D = [0 for _ in range(4)]
                for i in range(len(self.semiaxes)):
                    A += ray.direction[i]**2
                    B += (ray.initpoint[i] - self.position[i]) * ray.direction[i]
                    C += (ray.initpoint[i] - self.position[i])**2
                    D += self.semiaxes[i]**2

                B *= 2
                C -= D

                discr = B**2 - 4 * A * C
                if discr < 0:
                    return 0

                sol1, sol2 = (-B - sqrt(discr)) / (2 * A), (-B + sqrt(discr)) / (2 * A)

                if sol1 < 0:
                    if sol2 < 0:
                        return 0
                    return sol2
                if sol2 < 0:
                    return sol1
                return round(min(sol1, sol2), globals.config["precision"])


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
                        result = [x for x in result if x > 0]
                        if len(result) == 0:
                            result = 0
                        else:
                            result = min(result)
                        pself.distances[i][j] = result
                        
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
                                out_matr[i][j] = '.'
                                break
                            if matr[i][j] < list_steps[k]:
                                out_matr[i][j] = charmap[k]
                                break
                            
                pself.out_matr = out_matr

        return Canvas