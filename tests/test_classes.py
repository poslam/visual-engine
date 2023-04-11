import os
import sys

import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.classes import *

m3 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])


class TestMatrix:
    def testInitialize(self):
        m1 = Matrix([[1, 2], [3, 4]])
        assert isinstance(m1, Matrix)
        
    def testExceptionRectangularMatrixInInit(self):
        with pytest.raises(MatrixException):
            Matrix([[1, 2], [3]])

    def testDataIsList(self):
        m1 = Matrix([[1, 2], [3, 4]])
        assert isinstance(m1.data, list)

    def testSizeAutoComplete(self):
        m = Matrix([[1, 2], [3, 4], [5, 6]])
        assert m.rows == 3 and m.columns == 2

    def testZeroMatrixSize(self):
        zero = Matrix.zero_matrix(2, 5)
        assert zero.rows == 2 and zero.columns == 5

    def testZeroMatrixData(self):
        zero = Matrix.zero_matrix(2, 5)
        assert all(zero[i][j] == 0 
                   for i in range(2)
                   for j in range(5))

    def testIdentityMatrixByProduct(self):
        i = Matrix.identity_matrix(2)
        m1 = Matrix([[1, 2], [3, 4]])
        assert m1*i == i*m1 == m1

    def testTransposeByDoubleTranspose(self):
        m1 = Matrix([[1, 2], [3, 4]])
        assert m1.transpose().transpose() == m1

    def testEquationBySameMatrices(self):
        m = Matrix([[1+10**(-8), 2, 3], [2, 3, 1], [5, 1, 0]])
        assert m3 == m

    def testEpsilonParamInEquation(self):
        m = Matrix([[1+10**(-5), 2, 3], [2, 3, 1], [5, 1, 0]])
        assert m3 != m

    def testEquationByDifferentMatrices(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        assert m1 != m2

    def testIdentityMatrix(self):
        m7 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        i3 = Matrix.identity_matrix(3)
        assert i3 == m7
        
    def testAdditionCorrect(self):
        m7 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        m8 = Matrix([[2, 2, 3], [2, 4, 1], [5, 1, 1]])
        assert m3 + m7 == m8

    def testAdditionOutType(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        assert isinstance(m1+m2, Matrix)
    
    def testCommutativeOfAddition(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        assert m1+m2 == m2+m1
        
    def testAdditionExceptionWrongSize(self):
        with pytest.raises(EngineException):
            m1 = Matrix([[1, 2], [3, 4]])
            m1+m3
        
    def testAdditionExceptionWrongUsage(self):
        with pytest.raises(EngineException):
            m1 = Matrix([[1, 2], [3, 4]])
            m1+3
            
    def testCopy(self):
        m1 = Matrix([[1, 2], [3, 4]])
        assert m1 == m1.copy()

    def testProductExceptionWrongSize(self):
        with pytest.raises(EngineException):
            m1 = Matrix([[1, 2], [3, 4]])
            m1*m3
            
    def testProductExceptionWrongUsage(self):
        with pytest.raises(EngineException):
            m1 = Matrix([[1, 2], [3, 4]])
            m1*"str"
            
    def testProductOutType(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        assert isinstance(m1*m2, Matrix)
        
    def testProductWithScalarOutType(self):
        m1 = Matrix([[1, 2], [3, 4]])
        assert isinstance(m1*4, Matrix)        
            
    def testProductMatrices(self):
        m6 = Matrix([[1, 2], [3, 4], [5, 6]])
        m9 = Matrix([[23, 30], [19, 26], [13, 20]])
        m8 = Matrix([[2, 2, 3], [2, 4, 1], [5, 1, 1]])
        assert m8*m6 == m9
        
    def testProductWithScalar(self):
        m10 = Matrix([[4, 8, 12], [8, 12, 4], [20, 4, 0]])
        assert m3*4 == m10
        
    def testProductWithScalarCommutative(self):
        assert m3*4 == 4*m3
        
    def testSubtraction(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        m3 = Matrix([[-1, -1], [2, 4]])
        assert m1-m2 == m3
        
    def testTranspose(self):
        m1 = Matrix([[1, 2, 3], [5, 1, 7], [1, 3, 5]])
        m2 = Matrix([[1, 5, 1], [2, 1, 3], [3, 7, 5]])
        assert m1.transpose() == m2
        
    def testDeterminant(self):
        m = Matrix([[4, 5, 7], [1, 7, 3], [9, 4, 1]])
        assert m.determinant() == -303
        
    def testInverse(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        assert m1 * m1.copy().inverse() == Matrix.identity_matrix(2) and \
            m2.copy().inverse() * m2 == Matrix.identity_matrix(2)

    def testGram(self):
        m = Matrix([[1, 2], [3, 4]])
        assert m.gram() == Matrix([[5, 11], [11, 25]])
        
    def testDivisionWithScalar(self):
        m = Matrix([[1, 2], [3, 4]])
        m1 = Matrix([[0.5, 1], [1.5, 2]])
        assert m/2 == m1
    
    def testDivisionWithMatrix(self):
        m = Matrix([[1, 2], [3, 4]])
        m1 = Matrix([[6, 7], [4, 1]])
        assert m/m1 == Matrix([[7/22, -5/22], [13/22, -3/22]])
        
    def testDivisionExceptionNotCommutative(self):
        m = Matrix([[1, 2], [3, 4]])
        with pytest.raises(EngineException):
            2/m
            
    def testRotate(self):
        m = Matrix([[1, 2], [3, 4]])
        assert m.rotate([0, 1], 90) == Matrix([[2, -1], [4, -3]])
        

class TestVector:
    def testInitializeByMatrixHorizontalValues(self):
        m = Matrix([[1, 2, 3]])
        v = Vector(m)
        assert v.values == [1, 2, 3]
        
    def testInitializeByMatrixHorizontalAsMatrix(self):
        m = Matrix([[1, 2, 3]])
        v = Vector(m)
        assert v.as_matrix == m
        
    def testInitializeByMatrixHorizontalSize(self):
        m = Matrix([[1, 2, 3]])
        v = Vector(m)
        assert v.size == 3
        
    def testInitializeByMatrixHorizontalIsTransposed(self):
        m = Matrix([[1, 2, 3]])
        v = Vector(m)
        assert v.is_transposed == False
        
    def testInitializeByMatrixVerticalValues(self):
        m = Matrix([[2], [3], [4]])
        v = Vector(m)
        assert v.values == [[2], [3], [4]]
        
    def testInitializeByMatrixVerticalAsMatrix(self):
        m = Matrix([[2], [3], [4]])
        v = Vector(m)
        assert v.as_matrix == m
        
    def testInitializeByMatrixVerticalSize(self):
        m = Matrix([[2], [3], [4]])
        v = Vector(m)
        assert v.size == 3
        
    def testInitializeByMatrixVerticalIsTransposed(self):
        m = Matrix([[2], [3], [4]])
        v = Vector(m)
        assert v.is_transposed == True
        
    def testTranspose(self):
        v = Vector([1, 2, 3])
        assert v.transpose() == Vector([[1], [2], [3]])
        
    def testTransposeParamIsTransposedHorizontal(self):
        v = Vector([1, 2, 3])
        assert v.transpose().is_transposed == True
        
    def testTransposeParamIsTransposedVertical(self):
        v = Vector([[1], [2], [3]])
        assert v.transpose().is_transposed == False