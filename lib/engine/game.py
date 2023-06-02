from math import atan, pi, tan
from typing import Union

import src.globals as globals
from lib.engine.engine import Entity, EntityList, Ray
from lib.exceptions.engine_exc import EngineException
from lib.math.cs import CoordinateSystem
from lib.math.matrix_vector import Matrix, Vector
from lib.math.point import Point

@property
def restricted(self):
    raise AttributeError(f'{self.__class__} does not have this attribite')

class Game:
    def __init__(self, cs: CoordinateSystem, entities: EntityList):
        if not (isinstance(cs, CoordinateSystem)):
            raise EngineException(EngineException.WRONG_INPUT("CoordinateSystem"))
        
        if not isinstance(entities, EntityList):
            raise EngineException(EngineException.WRONG_INPUT("EntityList"))

        self.cs = cs
        self.entities = entities
        self.entity = self.get_entity()
        self.ray = self.get_ray()
        self.object = self.get_object()
        self.camera = self.get_camera()

    def run(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass

    def get_entity(self):
        class GameEntity(Entity):
            def __init__(pself):
                super().__init__(self.cs)

        return GameEntity

    def get_ray(self):
        class GameRay(Ray):
            def __init__(pself):
                super().__init__(self.cs)
            
        return GameRay

    def get_object(self):
        class Object(self.entity):
            def __init__(pself, position: Point,
                         direction: Union[Vector, list[int, float], None] = None):
                super().__init__()
                if not (isinstance(position, Point)):
                    raise EngineException(EngineException.WRONG_INPUT("Point"))
                
                if not isinstance(direction, Union[Vector, list, None]):
                    raise EngineException(EngineException.WRONG_INPUT("(Vector, list, None)"))

                position = Point([round(x, globals.precision)
                                 for x in position.values])

                if direction is not None:
                    direction = Vector([round(x, globals.precision)
                                        for x in direction.norm().values])

                pself.set_direction(direction)
                pself.set_position(position)

            def move(self, direction: Vector):
                self["position"] = self["position"] + direction

            def planar_rotate(self, inds: list[int], angle: float):
                if not isinstance(self["direction"], Vector):
                    raise EngineException(EngineException.DIRECTION_ERROR)

                direction = self["direction"].rotate(inds, angle)
                self.set_direction(direction)

            def rotate_3d(self, angles: list[Union[int, float]]):
                if not isinstance(self["direction"], Vector):
                    raise EngineException(EngineException.DIRECTION_ERROR)

                direction = self["direction"].rotate_3d(angles)
                self.set_direction(direction)

            def set_position(self, position: Point):
                position = Point([round(x, globals.precision)
                                 for x in position.values])

                self.set_property("position", position)

            def set_direction(self, direction: Vector):
                if direction != None:
                    direction = Vector([round(x, globals.precision)
                                        for x in direction.norm().values])

                self.set_property("direction", direction)
                
            def intersection_distance(self, ray: Ray):
                return 0

        return Object

    def get_camera(self):
        class Camera(self.object):
            def __init__(self, position: Point, draw_distance: Union[int, float],
                         fov: Union[int, float], direction: Vector = None,
                         vfov: Union[int, float] = None,
                         look_at: Point = None):
                super().__init__(position, direction)

                draw_distance = round(draw_distance, globals.precision)
                fov = round(fov*pi/180, globals.precision)

                if vfov == None:
                    vfov = round(atan(globals.display_size*tan(fov/2)), globals.precision)
                else:
                    vfov = round(vfov, globals.precision)

                self.set_property("fov", fov)
                self.set_property("vfov", vfov)
                self.set_property("draw_distance", draw_distance)
                self.set_property("look_at", look_at)
                
            def get_rays_matrix(self, n: int, m: int):
                if self.direction != None:
                    result = Matrix.zero_matrix(n, m)
                    
                    alpha, beta = self.fov, self.vfov
                    dalpha, dbeta = alpha/n, beta/m
                    vec = self.direction
                    
                    for i in range(n):
                        for j in range(m):
                            temp_vec = vec.copy()
                            temp_vec.rotate([0, 1], dalpha*i-alpha/2)
                            temp_vec.rotate([0, 2], dbeta*j-beta/2)
                            temp_vec.values = [round(x, globals.precision) for x in temp_vec.values]
                            result[i][j] = Ray(self.cs, self.position, temp_vec)
                    
                    return result
                                                     
                if self.look_at != None:
                    pass
                
        return Camera 