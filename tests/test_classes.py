import os
import sys

import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.classes import *

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[2, 3], [1, 0]])
m3 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
m4 = Matrix([[1+10**(-5), 2, 3], [2, 3, 1], [5, 1, 0]])
m5 = Matrix([[1+10**(-8), 2, 3], [2, 3, 1], [5, 1, 0]])
m6 = Matrix([[1, 2], [3, 4], [5, 6]])
m7 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
m8 = Matrix([[2, 2, 3], [2, 4, 1], [5, 1, 1]])

v1 = Vector([1, 2, 3])
v2 = Vector([5, 6, 0])
v3 = Vector([[2], [3], [4]])
v4 = Vector([[0], [0], [1]])

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])

p1 = Point([1, 1, 1])

zero = Matrix.zero_matrix(2, 5)

i2 = Matrix.identity_matrix(2)
i3 = Matrix.identity_matrix(3)


class TestMatrix:
    def testInitialize(self):
        assert isinstance(m1, Matrix)
        
    def testExceptionRectangularMatrixInInit(self):
        with pytest.raises(MatrixException):
            Matrix([[1, 2], [3]])

    def testDataIsList(self):
        assert isinstance(m1.data, list)

    def testSizeAutoComplete(self):
        assert m6.rows == 3 and m6.columns == 2

    def testZeroMatrixSize(self):
        assert zero.rows == 2 and zero.columns == 5

    def testZeroMatrixData(self):
        assert all(zero[i][j] == 0 
                   for i in range(2)
                   for j in range(5))

    def testIdentityMatrixByProduct(self):
        assert m1*i2 == i2*m1 == m1

    def testTransposeByDoubleTranspose(self):
        assert m1.transpose().transpose() == m1

    def testEquationBySameMatrices(self):
        assert m3 == m5

    def testEpsilonParamInEquation(self):
        assert m3 != m4

    def testEquationByDifferentMatrices(self):
        assert m1 != m2

    def testIdentityMatrix(self):
        assert i3 == m7
        
    def testAdditionCorrect(self):
        assert m3 + m7 == m8

    def testAdditionOutType(self):
        assert isinstance(m3+m7, Matrix)
    
    def testCommutativeOfAddition(self):
        assert m1+m2 == m2+m1
        
    def testAdditionExceptionWrongSize(self):
        with pytest.raises(EngineException):
            m1+m3
        
    def testAdditionExceptionWrongUsage(self):
        with pytest.raises(EngineException):
            m1+3
            
    def testCopy(self):
        assert m1 == m1.copy()

    def testProductExceptionWrongSize(self):
        with pytest.raises(EngineException):
            m1*m3
            
    def testProductExceptionWrongUsage(self):
        with pytest.raises(EngineException):
            m1*"str"
            
    