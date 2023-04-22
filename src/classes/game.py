from src.classes.math import (CoordinateSystem, EngineException, Matrix, Point,
                              Vector, VectorSpace)
from src.exceptions import GameException

class Engine:
    class Ray:
        def __init__(self, cs: CoordinateSystem, initpoint: Point,
                     direction: Vector):
            self.cs = cs
            self.initpoint = initpoint
            self.direction = direction
            
    class Indentifier:
        def __init__(self):
            self.identifiers = set()
            self.value = None
            
        def get_value(self):
            return self.value
        
        def __generate__(self):
            pass

    class Entity:
        def __init__(self, cs: CoordinateSystem):
            self.cs = cs
            self.identifier = None
            self.properties = dict()
            
        def set_property(self, property: str, value):
            self.properties[property] = value
            
        def get_property(self, property: str):
            return self.properties[property]
        
        def remove_property(self, property: str):
            if not (property in self.properties):
                raise GameException(GameException.PROPERTY_GET_ERROR)
            
            self.properties.__delitem__(property)
            
        def __getitem__(self, property: str):
            return self.get_property(property)
        
        def __setitem__(self, value):
            return self.set_property()
                    
        def __getattribute__(self, property: str, value):
            return self.properties[property]

    class EntityList:
        pass

    class Game:
        pass
