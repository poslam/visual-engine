import os
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.game import Game
from lib.exceptions.engine_exc import EngineException
from lib.engine.basic import Entity, EntityList
from lib.math.cs import CoordinateSystem
from lib.math.matrix_vector import Vector
from lib.math.point import Point
from lib.math.vs import VectorSpace
import src.globals as globals

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
p1 = Point([0, 0, 0])
cs = CoordinateSystem(p1, vs)
globals.cs = cs

class TestEntity:
    def test_set_property1(self):
        en = Entity(cs)
        
        en.set_property("Rossiya", "pravoslavno")
        act = (en["Rossiya"] == "pravoslavno")
        
        assert act
        
    def test_get_property1(self):
        en = Entity(cs)
        
        en.set_property("Rossiya", "pravoslavno")
        act = (en["Rossiya"] == "pravoslavno")
        
        assert act    
        
    def test_set_property2(self):
        en = Entity(cs)
        
        en["Rossiya"] = "pravoslavno"
        act = (en["Rossiya"] == "pravoslavno")
        
        assert act

    def test_get_property2(self):
        en = Entity(cs)
        en.set_property("Rossiya", "pravoslavno")
        
        act = (en.get_property("Rossiya") == "pravoslavno")
        
        assert act
        
    def test_remove_property(self):
        en = Entity(cs)
        en.set_property("Rossiya", "pravoslavno")
        
        en.remove_property("Rossiya")
        
        with pytest.raises(EngineException):
            en.get_property("Rossiya")
        
class TestEntityList:
    def test_append(self):
        en_l = EntityList([Entity(cs), Entity(cs)])
        
        en_l.append(Entity(cs))
        
        act = (len(en_l.entities) == 3)
        
        assert act
        
    def test_remove(self):
        en_l = EntityList([Entity(cs), Entity(cs)])
        
        en1 = en_l.entities[0]
        en_l.remove(en1.id)
        
        act = (en1 not in en_l.entities)
        
        assert act
        
    def test_get(self):
        en_l = EntityList([Entity(cs), Entity(cs)])
        
        en1 = en_l.entities[0]
        
        act = (en1 == en_l.get(en1.id))
        
        assert act
    
    def test_exec(self):
        en_l = EntityList([Entity(cs), Entity(cs)])
        
        en_l.exec(Entity.set_property, "test", "123")
        act = all(en_l.entities[i]["test"] == "123" for i in range(len(en_l.entities)))
        
        assert act
        
class TestGameObject:
    def test_move(self):
        game = Game(cs, EntityList(Entity(cs)))
        object = game.get_object()(Point([0, 0, 0]), Vector([1, 1, 1]))
        
        object.move(Vector([1, 1, 2]))
        act = (object["position"] == Point([1, 1, 2]))

        assert act
        