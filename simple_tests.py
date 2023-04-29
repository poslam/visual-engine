from src.classes.engine import Entity, EntityList, Game
from src.classes.math import *
import src.globals as globals

globals.init()

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[2, 3], [1, 0]])
m3 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
m4 = Matrix([[1+10**(-5), 2, 3], [2, 3, 1], [5, 1, 0]])

v1 = Vector([1, 2, 3])
v2 = Vector([5, 6, 0])
v3 = Vector([[2], [3], [4]])
v4 = Vector([[0], [0], [1]])

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])

p1 = Point([0, 0, 0])
p2 = Point([2.543245345, 33.12341234, 1.1231231])

cs = CoordinateSystem(p1, vs)
globals.cs = cs


ent1 = Entity(cs)
ent2 = Entity(cs)
ent_l = EntityList([ent1, ent2])

ent1['pr1'] = 1
ent2['pr2'] = 2345
ent2['pr3'] = 234
print(ent1.pr1)
ent1.pr1 = 2
ent1.set_property("pr1", 4)
print(ent1.pr1)

# print(globals.identifiers)

class NewEntity:
    def __init__(self):
        self.__dict__["properties"] = set()
        
    def get_property(self, prop: str, default = None):
        if prop not in self.__dict__["properties"]:
            return default

        return self.__dict__[prop]
    
    def set_property(self, prop: str, value: any):
        if prop == "properties":
            raise Exception
        
        self.__dict__[prop] = value
        self.__dict__["properties"].add(prop)
        
    def remove_property(self, prop):
        if prop == "properties":
            raise Exception
        
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
        
    
x = NewEntity()

print()
print(x.val1)
print(x["val1"])
print(x.get_property("val1"))

x.val1 = "Cringe"

print()
print(x.val1)
print(x["val1"])
print(x.get_property("val1"))

x["val1"] = "Oh no"

print()
print(x.val1)
print(x["val1"])
print(x.get_property("val1"))

x.set_property("val1", "Welcum")

print()
print(x.val1)
print(x["val1"])
print(x.get_property("val1"))

x.val2 = "1e"

print()
print(x.val2)
print(x["val2"])
print(x.get_property("val2"))

print(x.properties)

x.remove_property("val2")
print(x.properties)

print()
print(x.val2)
print(x["val2"])
print(x.get_property("val2"))
