import hashlib
from datetime import datetime

from src.classes.math import CoordinateSystem, Matrix, Point, Vector
from src.exceptions import GameException
import src.globals as globals

class Engine:
    class Ray:
        def __init__(self, cs: CoordinateSystem, initpoint: Point = None,
                     direction: Vector = None):
            self.cs = cs
            self.initpoint = initpoint
            self.direction = direction
    class Identifier:
        def __init__(self):
            self.identifiers = set()
            self.value = None

        def get_value(self):
            return self.value

        def __generate__():
            id = str(hashlib.md5(
                bytes(str(datetime.utcnow()), 'UTF-8')).digest())[2:-2]
            return id

    class Entity:
        def __init__(self, cs: CoordinateSystem):
            self.cs = cs
            self.id = Engine.Identifier.__generate__()
            self.properties = dict()

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
            
        def append(self, entity: 'Engine.Entity'):
            self.entities.append(entity)
            
        def remove(self, entity: 'Engine.Entity'):
            self.entities.remove(entity)
            
        def get(self, id: 'Engine.Identifier'):
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
        
        def __getitem__(self, id: 'Engine.Identifier'):
            return self.get(id)
            

    class Game:
        def __init__(self, cs: CoordinateSystem, entities: 'Engine.EntityList'):
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
            return Engine.Entity(globals.cs)
            
        def get_ray():
            return Engine.Ray(globals.cs)
        
        class Object:
            def __init__(self, position: Point, direction: Vector):
                self.entity = Engine.Game.get_entity()
                self.entity.set_property("position", position)
                self.entity.set_property("direction", direction.norm())
                
            def move(self, direction: Vector):
                pass
            
            def planar_rotate(self, inds: list[int], angle: float):
                pass
            
            def rotate_3d(self, angles: list[float]):
                pass
            
            def set_position(self, position: Point):
                self.entity.set_property("position", position)
                
            def set_direction(self, direction: Vector):
                self.entity.set_property("direction", globals.cs.vs.norm(direction))
                
            
                
        
                
                