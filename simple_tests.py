from src.classes.math import *
from src.classes.game import *
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

x = Game(cs, ent_l)
obj = x.Object(p1, v1)

obj.set_direction(v1)


cam = x.Camera(p2, v1, 2.4555556, 30)
# print(cam.entity.properties)

print(type(m1[1]))
