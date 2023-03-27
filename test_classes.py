from classes import *

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[2, 3], [1, 0]])
m3 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
m4 = Matrix([[1+10**(-5), 2, 3], [2, 3, 1], [5, 1, 0]])
m5 = Matrix([[1+10**(-8), 2, 3], [2, 3, 1], [5, 1, 0]])

v1 = Vector([1, 2, 3])
v2 = Vector([5, 6, 0])
v3 = Vector([[2], [3], [4]])
v4 = Vector([[0], [0], [1]])

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])

p1 = Point([1, 1, 1])

zero = Matrix.zero_matrix(2, 5)

i = Matrix.identity_matrix(2)


class TestMatrixOperations:
    def test_matrix_product_identity_matrix(self):
        assert m1*i == i*m1 == m1
        
    def test_commutative_of_addition(self):
        assert m1+m2 == m2+m1
        
    def test_transpose(self):
        assert m1.transpose().transpose() == m1
        
    def test_equation_of_matrices1(self):
        assert m3 != m4
        
    def test_eqation_of_matrices2(self):
        assert m3 == m5
        
    def test_eqation_of_matrices3(self):
        assert m1 != m2