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

cs = CoordinateSystem(p1, vs)
globals.coord_system = cs


ent1 = Engine.Entity(cs)
ent2 = Engine.Entity(cs)
ent_l = Engine.EntityList([ent1, ent2])

# ent1['pr1'] = 1
# ent2['pr2'] = 2345
# ent2['pr3'] = 234

print(ent_l[ent1.id])

# print(ent_l.exec(lambda x: x.properties))
