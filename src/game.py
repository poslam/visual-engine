from math import pi
from typing import Union
from lib.engine.basic import Entity, EntityList, Ray
from lib.exceptions.engine_exc import EngineException
from lib.math.cs import CoordinateSystem
from lib.math.point import Point
from lib.math.matrix_vector import Vector
import src.globals as globals


class Game:
    def __init__(self, cs: CoordinateSystem, entities: 'EntityList'):
        self.cs = cs
        self.entities = entities

        globals.cs = cs

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
        class GameObject(self.get_entity()):
            def __init__(self, position: Point, direction: Vector = None):
                position = Point([round(x, globals.precision) for x in position.values])
                if isinstance(direction, Vector):
                    direction = Vector([round(x, globals.precision)
                                    for x in direction.norm().values])

                self.entity = Game.get_entity()
                self.entity.set_property("position", position)
                self.entity.set_property("direction", direction)

            def move(self, direction: Vector):
                self.entity["position"] = self.entity["position"] + direction

            def planar_rotate(self, inds: list[int], angle: float):
                if not isinstance(self.entity["direction"], Vector):
                    raise EngineException(EngineException.DIRECTION_ERROR)
                
                direction = self.entity["direction"]
                self.set_direction(direction.rotate(inds, angle))

            def rotate_3d(self, angles: list[Union[int, float]]):
                if not isinstance(self.entity["direction"], Vector):
                    raise EngineException(EngineException.DIRECTION_ERROR)
                
                direction = self.entity["direction"]
                self.set_direction(direction.rotate_3d(angles))

            def set_position(self, position: Point):
                position = Point([round(x, globals.precision) for x in position.values])

                self.entity.set_property("position", position)

            def set_direction(self, direction: Vector):
                direction = Vector([round(x, globals.precision)
                                for x in direction.norm().values])

                self.entity.set_property("direction", direction)
        
    def get_camera(self):
        class GameCamera(self.get_object()):
            def __init__(self, position: Point, draw_distance: float,
                        fov: Union[int, float], direction: Vector = None, vfov: Union[int, float] = None,
                        look_at: Point = None):
                if not isinstance(look_at, Point):
                    super().__init__(position, direction)
                else:
                    super().__init__(position)

                fov = round(fov*pi/180, globals.precision)
                vfov = round(2/3*fov, globals.precision)
                draw_distance = round(draw_distance, globals.precision)

                self.entity.set_property("fov", fov)
                if vfov == None:
                    # self.entity.set_property("vfov", vfov)
                    pass
                else:
                    self.entity.set_property("vfov", vfov)
                self.entity.set_property("draw_distance", draw_distance)
