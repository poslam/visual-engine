import hashlib
from datetime import datetime
from math import pi
from typing import Union

import src.globals as globals
from lib.math.matrix_vector import CoordinateSystem, Point, Vector
from lib.exceptions.engine_exc import EngineException

precision = 4


class Ray:
    def __init__(self, cs: CoordinateSystem, initpoint: Point = None,
                 direction: Vector = None):
        initpoint = Point([round(x, precision) for x in initpoint.values])
        direction = Vector([round(x, precision) for x in direction.values])

        self.cs = cs
        self.initpoint = initpoint
        self.direction = direction


class Identifier:
    def __generate_id__():
        id = str(hashlib.md5(
            bytes(str(datetime.utcnow()), 'UTF-8')).digest())[2:-2]
        return id
    
    def __init__(self):
        self.val = self.__generate_id__()
        globals.identifiers.add(self.val)


class Entity:
    def __init__(self, cs: CoordinateSystem):
        self.cs = cs
        self.id = Identifier
        self.__dict__["properties"] = set()
        
    def get_property(self, prop: str):
        if prop not in self.__dict__["properties"]:
            return EngineException(EngineException.NOT_FOUND_ERROR("property"))

        return self.__dict__[prop]
    
    def set_property(self, prop: str, value: any):
        if prop == "properties":
            raise EngineException(EngineException.ROOT_PROPERTY)
        
        self.__dict__[prop] = value
        self.__dict__["properties"].add(prop)
        
    def remove_property(self, prop):
        if prop == "properties":
            raise EngineException(EngineException.ROOT_PROPERTY)
        
        self.__delattr__(prop)
        self.__dict__["properties"].remove(prop)
        
    def __getitem__(self, prop):
        return self.get_property(prop)
    
    def __setitem__(self, prop, value):
        self.set_property(prop, value)
   
    def __getattr__(self, prop):
        return self.get_property(prop)
   
    def __setattr__(self, prop, value):
        self.set_property(prop, value)


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
            raise EngineException(EngineException.COLLISION_ERROR)
        if len(entity) == 0:
            raise EngineException(EngineException.NOT_FOUND_ERROR("entity"))

        return entity[0]

    def exec(self, func: callable):
        if len(self.entities) == 0:
            raise EngineException(EngineException.NOT_FOUND_ERROR("entities"))

        self.entities = list(map(lambda obj: func(obj), self.entities))
        return self.entities

    def __getitem__(self, id: str):
        return self.get(id)


