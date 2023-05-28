from lib.math.matrix_vector import Matrix, Vector

m = Matrix([[1, 2], [3, 4]])
        
act = m.rotate([0, 1], 90)

print(act)

v = Vector([1, 1, 1]).rotate([0, 1], 90)
v1 = Vector([[1], [1], [1]]).rotate([0, 1], 90)
print(v)
print(v1)

v = Vector([1, 1, 1]).rotate_3d([0, 0, 90])
v1 = Vector([[1], [1], [1]]).rotate_3d([0, 0, 90])
print(v)
print(v1)