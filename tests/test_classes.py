import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.classes import *

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[2, 3], [1, 0]])
m3 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
m4 = Matrix([[1+10**(-5), 2, 3], [2, 3, 1], [5, 1, 0]])
m5 = Matrix([[1+10**(-8), 2, 3], [2, 3, 1], [5, 1, 0]])
m6 = Matrix([[1, 2], [3, 4], [5, 6]])

v1 = Vector([1, 2, 3])
v2 = Vector([5, 6, 0])
v3 = Vector([[2], [3], [4]])
v4 = Vector([[0], [0], [1]])

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])

p1 = Point([1, 1, 1])

zero = Matrix.zero_matrix(2, 5)

i = Matrix.identity_matrix(2)


class TestMatrix:
    def testInitialise(self):
        f = isinstance(m1, Matrix)
        assert f

    def testDataIsList(self):
        f = isinstance(m1.data, list)
        print(f)
        assert f

    def testSizeAutoComplete(self):
        assert m6.rows == 3 and m6.columns == 2

    def testZeroMatrixSize(self):
        assert zero.rows == 2 and zero.columns == 5

    def testZeroMatrixData(self):
        pass

    def testIdentityMatrixByProduct(self):
        assert m1*i == i*m1 == m1

    def testCommutativeOfAddition(self):
        assert m1+m2 == m2+m1

    def testTransposeByDoubleTranspose(self):
        assert m1.transpose().transpose() == m1

    def testEquationBySameMatrices(self):
        assert m3 == m5

    def testEpsilonParamInEquation(self):
        assert m3 != m4

    def testEquationByDifferentMatrices(self):
        assert m1 != m2
        
