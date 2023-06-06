from typing import Union

import src.globals as globals
from lib.engine.engine import EntityList, Ray
from lib.engine.game import Game
from lib.exceptions.engine_exc import EngineException
from lib.math.cs import CoordinateSystem
from lib.math.matrix_vector import Matrix, Vector
from lib.math.point import Point


@property
def restricted(self):
    raise AttributeError(f'{self.__class__} does not have this attribite')


class MyGame(Game):
    def __init__(self, cs: CoordinateSystem, entities: EntityList=None):
        if entities == None:
            entities = EntityList()
        super().__init__(cs, entities)

    def run(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass

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

                return round(temp_vec.len(), globals.precision)

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
                p2 = sum(2*pos[i]*dir[i]/self.semiaxes[i]**2 for i in range(dim))
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

                return round((intersection_vec-temp).len(), globals.precision)

        return HyperEllipsoid

    def get_canvas(self):
        class Canvas:
            def __init__(self, n: int, m: int):
                self.n = n
                self.m = m
                self.distances = Matrix.zero_matrix(n, m)

            def draw(self):
                pass

            def update(pself, camera: self.get_camera()):
                rays = camera.get_rays_matrix(pself.n, pself.m)
                    
                for i in range(pself.n):
                    for j in range(pself.m):
                        result = []
                        for ent in self.entities:
                            result.append(ent.intersection_distance(rays[i][j]))
                        y = [z for z in result if z > 0]
                        if len(y) == 0:
                            y = 0
                        else:
                            y = min(y)
                        pself.distances[i][j] = y    
                
        return Canvas
