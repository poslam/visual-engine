from src.classes import *
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
globals.vs_space = vs

p1 = Point([1, 1, 1])

# print("m1", m1)
# print("m2", m2)
# print("m3", m3)
# print("m4", m4, '\n')

# print("v1", v1)
# print("v2", v2)
# print("v3", v3)
# print("v4", v4, '\n')

# print("vs", "VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])\n")

# print("p1", p1, '\n')

# zero = Matrix.zero_matrix(2, 5)
# print("zero = Matrix.zero_matrix(2, 5)", zero)

# i = Matrix.identity_matrix(2)
# print("i = Matrix.identity_matrix(2)", i)
# print("m1*i", m1*i)

# print("m1+m2", m1+m2)

# print("m2.copy()", m2.copy())

# print("m1*m2", m1*m2)

# print("m2-m1", m2-m1)

# print("m1*3", m1*3, "3*m1", 3*m1)

# print("m3 == m4", m3 == m4)

# print("m1.transpose()", m1.transpose())

# print("m3.determinant()", m3.determinant())

# print("m1.inverse()", m1.inverse())
# print("m1*m1.inverse()", m1*m1.inverse(),
#       "m1.inverse()*m1", m1.inverse()*m1)

# print("m1/m2", m1/m2, "(m1/m2)*m2", (m1/m2)*m2)

# print("m1.gram()", m1.gram())

# print("m1/2", m1/2)

# print("v1.transpose()", v1.transpose())

# print("v3.transpose()", v3.transpose())

# print("v1+v2", v1.transpose()+v2)

# print("v3+v4", v3.transpose()+v4)

# print("v2-v1", v2-v1)

# print("v4-v3", v4-v3)

# print("v1*2", v1*2)

# print("v1*2", v3*2)

# print("v1/2", v1/2)

# print("v3/2", v3/2)

# print("v1&v2", v1&v2)

# print("v1&v4", v1&v4)

# print("v3&v4", v3&v4)

# print("v1**v2", v1**v2)

# print("v1**v4", v1**v4)

# print("v1.len()", v1.len())

# print("BilinearForm(m3, v1, v2)", BilinearForm(m3, v1, v2))

# print("vs.scalar_product(v3, v4)", vs.scalar_product(v3, v4))

# print("v1+p1", v1+p1)

# print("p1+v1", p1+v1)

# print("p1-v1", p1-v1)

# print("vs.as_vector(p1)", vs.as_vector(p1))

# print("v1.rotate([1, 2], 20).rotate([0, 2], 20).rotate([0, 1], 20)", v1.rotate([1, 2], 20).rotate([0, 2], 20).rotate([0, 1], 20))

# print(v3.rotate([1, 2], 90))

# m1010 = Matrix([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#                 [2, 1, 4, 1, 6, 1, 2, 2, 3, 4],
#                 [4, 1, 34, 90, 1, 3, 11, 1, 3, 0],
#                 [3, 3, 8, 1, 17, 4, 1, 9, 0, 5],
#                 [3, 1, 8, 20, 18, 4, 1, 1, 4, 0],
#                 [6, 3, 7, 14, 17, 5, 1, 25, 4, 5],
#                 [4, 3, 8, 13, 11, 1, 1, 4, 88, 9],
#                 [10, 3, 1, 18, 17, 0, 1, 3, 44, 51],
#                 [3, 3, 0, 4, 9, 4, 23, 31, 0, 0],
#                 [0, 1, 8, 14, 17, 4, 19, 30, 4, 5]])

# print(m1010.determinant())

print(m1)
print(m1.rotate([0, 1], 90))