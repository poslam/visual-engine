import os
import sys

import pytest
from lib.math.cs import CoordinateSystem
from lib.math.point import Point
from lib.math.vs import VectorSpace

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import src.globals as globals
from lib.math.matrix_vector import Matrix, Vector
from lib.exceptions.math_exc import MathException


class TestMatrix:
    def testInitialize(self):
        m = Matrix([[1, 2], [3, 4]])
        
        act = isinstance(m, Matrix)
        
        assert act
        
    def testExceptionRectangularMatrixInInit(self):
        with pytest.raises(MathException):
            act = Matrix([[1, 2], [3]])

    def testDataIsList(self):
        m = Matrix([[1, 2], [3, 4]])
        
        act = isinstance(m.data, list)
        
        assert act

    def testSizeAutoComplete(self):
        m = Matrix([[1, 2], [3, 4], [5, 6]])
        
        act = (m.rows == 3 and m.columns == 2)
        
        assert act

    def testZeroMatrixSize(self):
        zero = Matrix.zero_matrix(2, 5)
        
        act = (zero.rows == 2 and zero.columns == 5)
        
        assert act

    def testZeroMatrixData(self):
        zero = Matrix.zero_matrix(2, 5)
        
        act = all(zero[i][j] == 0 
                   for i in range(2)
                   for j in range(5))
        
        assert act

    def testIdentityMatrixByProduct(self):
        i = Matrix.identity_matrix(2)
        m = Matrix([[1, 2], [3, 4]])
        
        act = (m*i == i*m == m)
        
        assert act

    def testIdentityMatrixByDeterminant(self):
        i = Matrix.identity_matrix(2)
        
        act = (i.determinant() == 1)
        
        assert act

    def testTransposeByDoubleTranspose(self):
        m = Matrix([[1, 2], [3, 4]])
        
        act = (m.transpose().transpose() == m)
        
        assert act

    def testEquationBySameMatrices(self):
        m1 = Matrix([[1 + 10**(-8), 2, 3], [2, 3, 1], [5, 1, 0]])
        m2 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
        
        act = (m1 == m2)
        
        assert act

    def testEpsilonParamInEquation(self):
        m1 = Matrix([[1+10**(-5), 2, 3], [2, 3, 1], [5, 1, 0]])
        m2 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
        
        act = (m1 != m2)
        
        assert act

    def testEquationByDifferentMatrices(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        
        act = (m1 != m2)
        
        assert act

    def testIdentityMatrix(self):
        m = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        i = Matrix.identity_matrix(3)
        
        act = (i == m)
        
        assert act
        
    def testAdditionCorrect(self):
        m1 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
        m2 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        m3 = Matrix([[2, 2, 3], [2, 4, 1], [5, 1, 1]])
        
        act = (m1 + m2 == m3)
        
        assert act

    def testAdditionOutType(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        
        act = isinstance(m1+m2, Matrix)
        
        assert act
    
    def testCommutativeOfAddition(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        
        act = (m1+m2 == m2+m1)
        
        assert act
        
    def testAdditionExceptionWrongSize(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
        
        with pytest.raises(MathException):
            act = m1+m2
        
    def testAdditionExceptionWrongUsage(self):
        m = Matrix([[1, 2], [3, 4]])
        
        with pytest.raises(MathException):
            act = m+3
            
    def testCopy(self):
        m = Matrix([[1, 2], [3, 4]])
        
        act = (m == m.copy())
        
        assert act

    def testProductExceptionWrongSize(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
        
        with pytest.raises(MathException):
            act = m1*m2
            
    def testProductOutType(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        
        act = isinstance(m1*m2, Matrix)
        
        assert act
        
    def testProductWithScalarOutType(self):
        m = Matrix([[1, 2], [3, 4]])
        
        act = isinstance(m*4, Matrix) 
        
        assert act
            
    def testProductMatrices(self):
        m1 = Matrix([[1, 2], [3, 4], [5, 6]])
        m2 = Matrix([[23, 30], [19, 26], [13, 20]])
        m3 = Matrix([[2, 2, 3], [2, 4, 1], [5, 1, 1]])
        
        act = (m3*m1 == m2)
        
        assert act
        
    def testProductWithScalar(self):
        m1 = Matrix([[4, 8, 12], [8, 12, 4], [20, 4, 0]])
        m2 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
        
        act = (m2*4 == m1)
        
        assert act
        
    def testProductWithScalarCommutative(self):
        m1 = Matrix([[1, 2, 3], [2, 3, 1], [5, 1, 0]])
        
        act = (m1*4 == 4*m1)
        
        assert act
        
    def testSubtraction(self):
        m1= Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        m3 = Matrix([[-1, -1], [2, 4]])
        
        act = (m1-m2 == m3)
        
        assert act
        
    def testTranspose(self):
        m1 = Matrix([[1, 2, 3], [5, 1, 7], [1, 3, 5]])
        m2 = Matrix([[1, 5, 1], [2, 1, 3], [3, 7, 5]])
        
        act = (m1.transpose() == m2)
        
        assert act
        
    def testDeterminant(self):
        m = Matrix([[4, 5, 7], [1, 7, 3], [9, 4, 1]])
        
        act = m.determinant() == -303
        
        assert act
        
    def testInverse(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[2, 3], [1, 0]])
        
        act = (m1 * m1.copy().inverse() == Matrix.identity_matrix(2) and \
            m2.copy().inverse() * m2 == Matrix.identity_matrix(2))
        
        assert act

    def testGram(self):
        m = Matrix([[1, 2], [3, 4]])
        
        act = (m.gram() == Matrix([[5, 11], [11, 25]]))
        
        assert act
        
    def testDivisionWithScalar(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[0.5, 1], [1.5, 2]])
        
        act = (m1/2 == m2)
        
        assert act
    
    def testDivisionWithMatrix(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[6, 7], [4, 1]])
        
        act = (m1/m2 == Matrix([[7/22, -5/22], [13/22, -3/22]]))
        
        assert act
        
    def testDivisionExceptionNotCommutative(self):
        m = Matrix([[1, 2], [3, 4]])
        
        with pytest.raises(MathException):
            act = 2/m
            
    def testRotate(self):
        m = Matrix([[1, 2], [3, 4]])
        
        act = (m.rotate([0, 1], 90) == Matrix([[-2, 1], [-4, 3]]))
        
        assert act
        

class TestVector:
    def testInitializeByMatrixHorizontalValues(self):
        m = Matrix([[1, 2, 3]])
        v = Vector(m)
        
        act = (v.values == [1, 2, 3])
        
        assert act
        
    def testInitializeByMatrixHorizontalAsMatrix(self):
        m = Matrix([[1, 2, 3]])
        v = Vector(m)
        
        act = (v.as_matrix() == m)
        
        assert act
        
    def testInitializeByMatrixHorizontalSize(self):
        m = Matrix([[1, 2, 3]])
        v = Vector(m)
        
        act = (v.size == 3)
        
        assert act
        
    def testInitializeByMatrixHorizontalIsTransposed(self):
        m = Matrix([[1, 2, 3]])
        v = Vector(m)
        
        act = (v.is_transposed == False)
        
        assert act
        
    def testInitializeByMatrixVerticalValues(self):
        m = Matrix([[2], [3], [4]])
        v = Vector(m)
        
        act = (v.values == [[2], [3], [4]])
        
        assert act
        
    def testInitializeByMatrixVerticalAsMatrix(self):
        m = Matrix([[2], [3], [4]])
        v = Vector(m)
        
        act = (v.as_matrix() == m)
        
        assert act
        
    def testInitializeByMatrixVerticalSize(self):
        m = Matrix([[2], [3], [4]])
        v = Vector(m)
        
        act = (v.size == 3)
        
        assert act
        
    def testInitializeByMatrixVerticalIsTransposed(self):
        m = Matrix([[2], [3], [4]])
        v = Vector(m)
        
        act = (v.is_transposed == True)
        
        assert act
        
    def testInitializeExceptionWrongSize(self):
        with pytest.raises(MathException):
            act = Vector([[2, 1], [1], [1]])
        
    def testTranspose(self):
        v = Vector([1, 2, 3])
        
        act = (v.transpose() == Vector([[1], [2], [3]]))
        
        assert act
        
    def testTransposeParamIsTransposedHorizontal(self):
        v = Vector([1, 2, 3])
        
        act = (v.transpose().is_transposed == True)
        
        assert act
        
    def testTransposeParamIsTransposedVertical(self):
        v = Vector([[1], [2], [3]])
        
        act = (v.transpose().is_transposed == False)
        
        assert act
        
    def testAdditionHorizontal(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([3, 4, 5])
        v3 = v1+v2
        
        act = (v3.values == [4, 6, 8] and v3 == Vector([4, 6, 8]))
        
        assert act
        
    def testAdditionVertical(self):
        v1 = Vector([[1], [2], [3]])
        v2 = Vector([[3], [4], [5]])
        v3 = v1+v2
        
        act = (v3.values == [[4], [6], [8]] and v3 == Vector([[4], [6], [8]]))
        
        assert act
        
    def testAdditionExceptionWrongSize(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([1, 2, 3, 4])
        
        with pytest.raises(MathException):
            act = v1 + v2
            
    def testAdditionExceptionWrongSize(self):
        v1 = Vector([1, 2, 3])
        
        with pytest.raises(MathException):
            act = v1 + 2
            
    def testScalarProduct(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([1, 2, 4])
        
        vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
        p1 = Point([0, 0, 0])
        cs = CoordinateSystem(p1, vs)
        globals.cs = cs
        
        act = (v1&v2 == 17)
        
        assert act
        
    def testVectorProduct(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([1, 2, 4])
        vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
        p1 = Point([0, 0, 0])
        cs = CoordinateSystem(p1, vs)
        globals.cs = cs
        
        act = (v1**v2 == Vector([2, -1, 0]))
        
        assert act
        
    def testVectorProductException(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([1, 2, 4, 5])
            
        with pytest.raises(MathException):
            act = v1*v2
            
    def testMultiplyWithScalar(self):
        v1 = Vector([1, 2, 3])
        
        act = v1 * 2 == Vector([2, 4, 6])
        
        assert act
        
    def testMultiplyWithVector(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([[1], [2], [4]])
        
        act = v1*v2 == Vector([17])
        
        assert act
            
    def testSubtractionHorizontal(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([1, 2, 4])
        
        act = v2 - v1 == Vector([0, 0, 1])
        
        assert act
        
    def testSubtractionVertical(self):
        v1 = Vector([[1], [2], [3]])
        v2 = Vector([[1], [2], [4]])
        
        act = (v2 - v1 == Vector([[0], [0], [1]]))
        
        assert act
        
    def testLen(self):
        v1 = Vector([1, 2, 3])
        vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
        p1 = Point([0, 0, 0])
        cs = CoordinateSystem(p1, vs)
        globals.cs = cs
        
        act = (v1.len() == 14**0.5)
        
        assert act
        
    def testNorm(self):
        v1 = Vector([1, 2, 3])
        vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
        p1 = Point([0, 0, 0])
        cs = CoordinateSystem(p1, vs)
        globals.cs = cs
        
        act = (v1.norm().len() == 1)
        
        assert act
        
    def testRotate(self):
        v = Vector([1, 2, 3])
        
        act = (v.rotate([0, 1], 90) == Vector([-2, 1, 3]))
        
        assert act
        
    def testDivByConst(self):
        v = Vector([1, 2, 3])
        
        act = (v/2 == Vector([0.5, 1, 1.5]))
        
        assert act
    

class TestPoint:
    def testAddition(self):
        p = Point([1, 1, 1])
        v = Vector([1, 2, 3])
        
        act = (v+p == Point([2, 3, 4]) and p+v == Point([2, 3, 4]))
        
        assert act
        
    def testAdditionCommutatiove(self):
        p = Point([1, 1, 1])
        v = Vector([1, 2, 3])
        
        act = (p+v == Point([2, 3, 4]))
        
        assert act
        
    def testAdditionException(self):
        p = Point([1, 1, 1])   
         
        with pytest.raises(MathException):
            act = p+1
            
    def testSubtraction(self):
        p = Point([1, 1, 1]) 
        v = Vector([1, 2, 3])
        
        act = (p-v == Point([0, -1, -2]))
        
        assert act
    

class TestVectorSpace:
    def testAsVector(self):
        vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
        p = Point([1, 2, 3])
        
        act = (vs.as_vector(p) == Vector([1, 2, 3]))
        
        assert act