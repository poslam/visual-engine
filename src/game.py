from typing import Union

import src.globals as globals
from lib.engine.engine import Entity, EntityList, Ray
from lib.engine.game import Game
from lib.exceptions.engine_exc import EngineException
from lib.math.matrix_vector import Matrix, Vector
from lib.math.point import Point

@property
def restricted(self):
    raise AttributeError(f'{self.__class__} does not have this attribite')

class MyGame(Game):
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
                    raise EngineException(EngineException.WRONG_INPUT("Vector"))
                
                self.position = position
                self.normal = normal.norm()
                
            def planar_rotate(self, inds: list[int], angle: float):
                normal = self.normal.rotate(inds, angle)
                self.normal = normal

            def rotate_3d(self, angles: list[Union[int, float]]):
                normal = self.normal.rotate_3d(angles)
                self.normal = normal
                
            def intersection_distance(self, ray: Ray):
                pass
        
            move = restricted
            set_direction = restricted
        
        return HyperPlane
    
    def get_hyperellipsoid(self):
        class HyperEllipsoid(self.object):
            def __init__(self, position: Point, direction: Vector, semiaxes: list[float]):
                if not isinstance(position, Point):
                    raise EngineException(EngineException.WRONG_INPUT(Point))
                
                if not isinstance(direction, Vector):
                    raise EngineException(EngineException.WRONG_INPUT(Vector))
                
                self.set_position(position)
                self.set_direction(direction)
                self.semiaxes = semiaxes
                
        return HyperEllipsoid


class Canvas:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.distances = Matrix.zero_matrix(n, m)
        
    def draw(self):
        pass
    
    def update(self, camera: Game.get_camera()):
        pass