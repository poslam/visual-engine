from lib.math.cs import CoordinateSystem
from lib.math.matrix_vector import Vector
from lib.math.point import Point
from lib.math.vs import VectorSpace
import src.globals as globals

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
p1 = Point([0, 0, 0])
cs = CoordinateSystem(p1, vs)
globals.cs = cs


# print(globals.identifiers)


        
    
# x = NewEntity()

# print()
# print(x.val1)
# print(x["val1"])
# print(x.get_property("val1"))

# x.val1 = "Cringe"

# print()
# print(x.val1)
# print(x["val1"])
# print(x.get_property("val1"))

# x["val1"] = "Oh no"

# print()
# print(x.val1)
# print(x["val1"])
# print(x.get_property("val1"))

# x.set_property("val1", "Welcum")

# print()
# print(x.val1)
# print(x["val1"])
# print(x.get_property("val1"))

# x.val2 = "1e"

# print()
# print(x.val2)
# print(x["val2"])
# print(x.get_property("val2"))

# print(x.properties)

# x.remove_property("val2")
# print(x.properties)

# print()
# print(x.val2)
# print(x["val2"])
# print(x.get_property("val2"))
