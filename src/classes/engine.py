import hashlib
from datetime import datetime
from math import pi
from typing import Union

import src.globals as globals
from src.classes.math import CoordinateSystem, Point, Vector
from src.exceptions import GameException

precision = 4


class Ray:
    def __init__(self, cs: CoordinateSystem, initpoint: Point = None,
                 direction: Vector = None):
        initpoint = Point([round(x, precision) for x in initpoint.values])
        direction = Vector([round(x, precision) for x in direction.values])

        self.cs = cs
        self.initpoint = initpoint
        self.direction = direction


def __generate_id__():
    id = str(hashlib.md5(
        bytes(str(datetime.utcnow()), 'UTF-8')).digest())[2:-2]
    return id


class Entity:
    def __init__(self, cs: CoordinateSystem):
        self.cs = cs
        self.id = __generate_id__()
        self.properties = dict()
        
        globals.identifiers.add(self.id)

    def set_property(self, property: str, value):
        self.properties[property] = value

    def get_property(self, property: str):
        if not (property in self.properties):
            raise GameException(GameException.NOT_FOUND_ERROR("property"))

        return self.properties[property]

    def remove_property(self, property: str):
        if not (property in self.properties):
            raise GameException(GameException.NOT_FOUND_ERROR("property"))

        self.properties.__delitem__(property)

    def __getitem__(self, property: str):
        return self.get_property(property)

    def __setitem__(self, property: str, value):
        return self.set_property(property, value)

    def __getattr__(self, property: str):
        return self.get_property(property)


class EntityList:
    def __init__(self, entities: list):
        self.entities = entities

    def append(self, entity: 'Entity'):
        self.entities.append(entity)

    def remove(self, entity: 'Entity'):
        self.entities.remove(entity)

    def get(self, id: str):
        entity = [entity for entity in self.entities
                  if entity.id == id]
        if len(entity) > 1:
            raise GameException(GameException.COLLISION_ERROR)
        if len(entity) == 0:
            raise GameException(GameException.NOT_FOUND_ERROR("entity"))

        return entity[0]

    def exec(self, func: callable):
        if len(self.entities) == 0:
            raise GameException(GameException.NOT_FOUND_ERROR("entities"))

        self.entities = list(map(lambda obj: func(obj), self.entities))
        return self.entities

    def __getitem__(self, id: str):
        return self.get(id)


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

    def get_entity():
        return Entity(globals.cs)

    def get_ray():
        return Ray(globals.cs)

    class Object(Entity):
        def __init__(self, position: Point, direction: Vector = None):
            position = Point([round(x, precision) for x in position.values])
            if isinstance(direction, Vector):
                direction = Vector([round(x, precision)
                                for x in direction.norm().values])

            self.entity = Game.get_entity()
            self.entity.set_property("position", position)
            self.entity.set_property("direction", direction)

        def move(self, direction: Vector):
            self.entity["position"] = self.entity["position"] + direction

        def planar_rotate(self, inds: list[int], angle: float):
            if not isinstance(self.entity["direction"], Vector):
                raise GameException(GameException.DIRECTION_ERROR)
            
            direction = self.entity["direction"]
            self.set_direction(direction.rotate(inds, angle))

        def rotate_3d(self, angles: list[Union[int, float]]):
            if not isinstance(self.entity["direction"], Vector):
                raise GameException(GameException.DIRECTION_ERROR)
            
            direction = self.entity["direction"]
            self.set_direction(direction.rotate_3d(angles))

        def set_position(self, position: Point):
            position = Point([round(x, precision) for x in position.values])

            self.entity.set_property("position", position)

        def set_direction(self, direction: Vector):
            direction = Vector([round(x, precision)
                               for x in direction.norm().values])

            self.entity.set_property("direction", direction)

    class Camera(Object):
        def __init__(self, position: Point, draw_distance: float,
                    fov: Union[int, float], direction: Vector = None, vfov: Union[int, float] = None,
                    look_at: Point = None):
            if not isinstance(look_at, Point):
                super().__init__(position, direction)
            else:
                super().__init__(position)

            fov = round(fov*pi/180, precision)
            vfov = round(2/3*fov, precision)
            draw_distance = round(draw_distance, precision)

            self.entity.set_property("fov", fov)
            if vfov == None:
                self.entity.set_property("vfov", vfov)
            else:
                self.entity.set_property("vfov", vfov)
            self.entity.set_property("draw_distance", draw_distance)
