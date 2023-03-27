from classes import *

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[2, 3], [1, 0]])
m3 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
m4 = Matrix([[1+10**(-5), 2, 3], [2, 3, 1], [5, 1, 0]])

v1 = Vector([1, 2, 3])
v2 = Vector([5, 6, 0])
v3 = Vector([[2], [3], [4]])
v4 = Vector([[0], [0], [1]])

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])

p1 = Point([1, 1, 1])

print("m1", m1)
print("m2", m2)
print("m3", m3)
print("m4", m4, '\n')

print("v1", v1)
print("v2", v2)
print("v3", v3)
print("v4", v4, '\n')

print("vs", "VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])\n")

print("p1", p1, '\n')

zero = Matrix.zero_matrix(2, 5)
print("zero = Matrix.zero_matrix(2, 5)", zero)

i = Matrix.identity_matrix(2)
print("i = Matrix.identity_matrix(2)", i)
print("m1*i", m1*i)

print("m1+m2", m1+m2)

print("m2.copy()", m2.copy())

print("m1*m2", m1*m2)

print("m2-m1", m2-m1)

print("m1*3", m1*3, "3*m1", 3*m1)

print("m3 == m4", m3 == m4)

print("m1.transpose()", m1.transpose())

print("m3.determinant()", m3.determinant())

print("m1.inverse()", m1.inverse())
print("m1*m1.inverse()", m1*m1.inverse(),
      "m1.inverse()*m1", m1.inverse()*m1)

print("m1/m2", m1/m2)

print("m1.gram()", m1.gram())

print("m1/2", m1/2)

print("v1.transpose()", v1.transpose())

print("v3.transpose()", v3.transpose())

print("v1+v2", v1+v2)

print("v3+v4", v3+v4)

print("v2-v1", v2-v1)

print("v4-v3", v4-v3)

print("v1*2", v1*2)

print("v1*2", v3*2)

print("v1/2", v1/2)

print("v3/2", v3/2)

print("v1&v2", v1&v2)

print("v1&v4", v1&v4)

print("v3&v4", v3&v4)

print("v1**v2", v1**v2)

print("v1**v4", v1**v4)

print("v1.len()", v1.len())

print("BilinearForm(m3, v1, v2)", BilinearForm(m3, v1, v2))

print("vs.scalar_product(v3, v4)", vs.scalar_product(v3, v4))

print("v1+p1", v1+p1)

print("p1+v1", p1+v1)

print("p1-v1", p1-v1)

print("vs.as_vector(p1)", vs.as_vector(p1))