from math import atan, pi, tan
from typing import Union
from config.config import Configuration
from src.event_system import EventSystem
from lib.exceptions.math_exc import MathException

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
    def __init__(self, cs: CoordinateSystem, es: EventSystem=None, entities: EntityList=None):
        if not (isinstance(cs, CoordinateSystem)):
            raise EngineException(EngineException.WRONG_INPUT("CoordinateSystem"))

        if entities == None:
            entities = EntityList()

        self.es = es
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
    
    def get_event_system(self):
        return self.es

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

                position = Point([round(x, globals.config["precision"])
                                 for x in position.values])

                pself.set_direction(direction)
                pself.set_position(position)

            def move(self, direction: Vector):
                self.set_position(self["position"] + direction)

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
                position = Point([round(x, globals.config["precision"])
                                 for x in position.values])

                self["position"] = position

            def set_direction(self, direction: Vector):
                if direction != None and direction != Vector([0, 0, 0]):
                    direction = Vector([round(x, globals.config["precision"])
                                        for x in direction.norm().values])

                self.set_property("direction", direction)
                
            def intersection_distance(self, ray: Ray):
                return 0

        return Object

    def get_camera(self):
        class Camera(self.object):
            def __init__(self, position: Point, draw_distance: Union[int, float]=None,
                         fov: Union[int, float]=None, direction: Vector = None,
                         vfov: Union[int, float] = None,
                         look_at: Point = None):
                super().__init__(position, direction)
                    
                if draw_distance == None:
                    draw_distance = globals.config["camera"]["draw_distance"]
                else:
                    raise Exception("draw distance is null")
                    
                if fov == None:
                    fov = globals.config["camera"]["fov"]
                else:
                    raise Exception("fov is null")
                
                draw_distance = round(draw_distance, globals.config["precision"])
                fov = round(fov*pi/180, globals.config["precision"])
                
                if vfov == None:
                    vfov = round(atan(globals.config["canvas"]["m"]/globals.config["canvas"]["n"]*tan(fov/2)), globals.config["precision"])
                else:
                    vfov = round(vfov, globals.config["precision"])

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
                            if (vec&temp_vec) == 0:
                                raise MathException(MathException.ZERO_DIVISION)
                            temp_vec = (temp_vec*(vec.len()**2/(vec&temp_vec)))
                            temp_vec.values = [round(x, globals.config["precision"]) for x in temp_vec.values]
                            result[i][j] = Ray(self.cs, self.position, temp_vec)
                    
                    return result
                                                     
                if self.look_at != None:
                    look_at_vec = Vector([x for x in self.look_at.values])
                    position_vec = Vector([x for x in self.position.values])
                    
                    vec = (look_at_vec-position_vec).norm()
                    
                    alpha, beta = self.fov, self.vfov
                    dalpha, dbeta = alpha/n, beta/m
                    
                    for i in range(n):
                        for j in range(m):
                            temp_vec = vec.copy()
                            temp_vec.rotate([0, 1], dalpha*i-alpha/2)
                            temp_vec.rotate([0, 2], dbeta*j-beta/2)
                            if (vec&temp_vec) == 0:
                                raise MathException(MathException.ZERO_DIVISION)
                            temp_vec = (temp_vec*(vec.len()**2/(vec&temp_vec)))
                            temp_vec.values = [round(x, globals.config["precision"]) for x in temp_vec.values]
                            result[i][j] = Ray(self.cs, self.position, temp_vec)
                    
                    return result
                    
                
        return Camera 
    
    