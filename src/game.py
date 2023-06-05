from typing import Union

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
    def __init__(self, cs: CoordinateSystem, entities: EntityList):
        super().__init__(cs, entities)

    def run(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass

    def get_hyperplane(self):
        class HyperPlane(self.object):
            def __init__(self, position: Point, normal: Vector):
                if not isinstance(position, Point):
                    raise EngineException(EngineException.WRONG_INPUT("Point"))

                if not isinstance(normal, Vector):
                    raise EngineException(
                        EngineException.WRONG_INPUT("Vector"))

                super().__init__(position)

                self.position = position
                self.normal = normal.norm()

            def planar_rotate(self, inds: list[int], angle: float):
                normal = self.normal.rotate(inds, angle)
                self.normal = normal

            def rotate_3d(self, angles: list[Union[int, float]]):
                normal = self.normal.rotate_3d(angles)
                self.normal = normal

            def intersection_distance(self, ray: Ray):
                ray_inp_vec = Vector([x for x in ray.initpoint.values])
                pos_vec = Vector([x for x in self.position.values])
                t = -((self.normal & (ray_inp_vec-pos_vec)) /
                      (self.normal & ray.direction))

                temp_vec = Vector([ray_inp_vec[0]+ray.direction[0]*t,
                                   ray_inp_vec[1]+ray.direction[1]*t,
                                   ray_inp_vec[2]+ray.direction[2]*t])

                return temp_vec.len()

            move = restricted

        return HyperPlane

    def get_hyperellipsoid(self):
        class HyperEllipsoid(self.object):
            def __init__(self, position: Point, direction: Vector, semiaxes: list[float]):
                if not isinstance(position, Point):
                    raise EngineException(EngineException.WRONG_INPUT(Point))

                if not isinstance(direction, Vector):
                    raise EngineException(EngineException.WRONG_INPUT(Vector))

                super().__init__(position, direction)
                self.semiaxes = semiaxes

            def intersection_distance(self, ray: Ray):
                dir, pos = ray.direction, ray.initpoint-self.position

                a, b, c = self.semiaxes[0]**2, self.semiaxes[1]**2, self.semiaxes[2]**2

                p1 = dir[0]**2/a + dir[1]**2/b + dir[2]**2/c
                p2 = 2*pos[0]*dir[0]/a + 2*pos[1]*dir[1]/b + 2*pos[2]*dir[2]/c
                p3 = -1 + pos[0]**2/a + pos[1]**2/b + pos[2]**2/c

                t1 = (-p2 + (p2**2-4*p1*p3)**0.5)/2*p1
                t2 = (-p2 - (p2**2-4*p1*p3)**0.5)/2*p1

                t = [x for x in [y for y in [t1, t2]
                                 if isinstance(y, (int, float))] if x > 0]

                if len(t) == 0:
                    return -1

                t = min(t)

                intersection_vec = Vector([ray.initpoint[0]+dir[0]*t,
                                           ray.initpoint[1]+dir[1]*t,
                                           ray.initpoint[2]+dir[2]*t])

                temp = Vector([pos[0], pos[1], pos[2]])

                return (intersection_vec-temp).len()

        return HyperEllipsoid


class Canvas:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.distances = Matrix.zero_matrix(n, m)

    def draw(self):
        pass

    def update(self, camera):
        pass
