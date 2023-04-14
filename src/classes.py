from math import cos, pi, sin
from typing import Union

from src.exceptions import EngineException, MatrixException
import src.globals as globals

@property
def restricted(self):
    raise AttributeError(f'{self.__class__} does not have this attribite')


class Matrix:
    def __init__(self, data: Union[list[list[float]], 'Vector']):
        if isinstance(data, Vector):
            if data.is_transposed == True:
                self.data = data.values
                self.rows = data.size
                self.columns = 1
            else:
                self.data = [data.values]
                self.rows = 1
                self.columns = data.size
        else:
            self.data = data
            self.rows = len(data)
            self.columns = len(data[0])
            for i in range(self.rows-1):
                if len(self.data[i]) != len(self.data[i+1]):
                    raise EngineException(EngineException.RECTANGULAR_MATRIX)

    def zero_matrix(rows: int, columns: int):
        data = [[0 for j in range(columns)] for i in range(rows)]
        return Matrix(data)

    def identity_matrix(size: int):
        result = Matrix.zero_matrix(size, size)
        for i in range(size):
            result.data[i][i] = 1
        return result
    
    def copy(self):
        result = Matrix.zero_matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                result[i][j] = self[i][j]
        return result

    def __eq__(self, obj: 'Matrix'):
        if not (self.rows == obj.rows and self.columns == obj.columns):
            return False
        
        eps = 10**(-7)
        return all(abs(self[i][j] - obj[i][j]) < eps
                    for i in range(self.rows)
                    for j in range(self.columns))
    

    def __add__(self, obj: 'Matrix'):
        if not isinstance(obj, Matrix):
            raise EngineException(EngineException.WRONG_USAGE)

        if not (self.rows == obj.rows and self.columns == obj.columns):
            raise EngineException(EngineException.WRONG_SIZE)

        result = Matrix.zero_matrix(self.rows, self.columns)
        result.data = [[self.data[row][column] + obj.data[row][column]
                        for column in range(self.columns)]
                       for row in range(self.rows)]
        return result

    def __product(obj1: Union['Matrix', float, int],
                  obj2: Union['Matrix', float, int]):
        if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
            if not (obj1.columns == obj2.rows):
                raise EngineException(EngineException.WRONG_SIZE)

            result = [[sum(a * b for a, b in zip(A_row, B_col))
                       for B_col in zip(*obj2.data)]
                      for A_row in obj1.data]
            return Matrix(result)

        elif isinstance(obj1, (float, int)) and isinstance(obj2, Matrix):
            result = obj2.copy()
            for i in range(obj2.rows):
                for j in range(obj2.columns):
                    result.data[i][j] *= obj1
            return result

        elif isinstance(obj1, Matrix) and isinstance(obj2, (float, int)):
            return Matrix.__product(obj2, obj1)

        else:
            raise EngineException(EngineException.WRONG_USAGE)

    def __minor(self, i: int, j: int):
        return [row[:j] + row[j+1:] for row in (self[:i]+self[i+1:])]

    def determinant(self):
        if isinstance(self, Matrix):
            matrix = self.data
        else:
            matrix = self

        if not (len(matrix) == len(matrix[0])):
            raise MatrixException(MatrixException.QUADRATIC_MATRIX)

        if len(matrix) == 1:
            return matrix[0][0]

        determinant = 0
        for c in range(len(matrix)):
            determinant += ((-1)**c)*matrix[0][c] *\
                Matrix.determinant(Matrix.__minor(matrix, 0, c))
                
        return determinant

    def inverse(self):
        determinant = Matrix.determinant(self)

        if determinant == 0:
            raise MatrixException(MatrixException.SINGULAR_MATRIX)

        if self.rows == 2:
            self.data = [[self[1][1]/determinant, -1*self[0][1]/determinant],
                         [-1*self[1][0]/determinant, self[0][0]/determinant]]
            return self

        cofactors = []
        for r in range(self.rows):
            cofactorRow = []
            for c in range(self.rows):
                __minor = Matrix.__minor(self, r, c)
                cofactorRow.append(((-1)**(r+c)) *
                                   Matrix.determinant(__minor))
            cofactors.append(cofactorRow)
        cofactors = Matrix.transpose(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c]/determinant
        self.data = cofactors
        return self

    def gram(self):
        if self.rows != self.columns:
            raise MatrixException(MatrixException.QUADRATIC_MATRIX)

        result = Matrix.zero_matrix(self.rows, self.rows)
        identity = Matrix.identity_matrix(self.rows)
        for i in range(self.rows):
            for j in range(self.columns):
                result[i][j] = BilinearForm(
                    identity, Vector(self[i]), Vector(self[j]))
        return result

    def transpose(self):
        if not isinstance(self, Matrix):
            raise EngineException(EngineException.WRONG_USAGE)

        self.data = [[self[j][i] for j in range(self.rows)]
                     for i in range(self.columns)]
        self.rows, self.columns = self.columns, self.rows
        return self
    
    def rotate(self, axes_indecies: list[int], angle: float):
        angle = angle*pi/180

        rotation_matrix = Matrix.identity_matrix(self.columns)

        n = (-1)**(axes_indecies[0] + axes_indecies[1])

        rotation_matrix[axes_indecies[0]][axes_indecies[0]] = cos(angle)
        rotation_matrix[axes_indecies[1]][axes_indecies[1]] = cos(angle)

        rotation_matrix[axes_indecies[1]][axes_indecies[0]] = n * sin(angle)
        rotation_matrix[axes_indecies[0]][axes_indecies[1]] = (-n) * sin(angle)

        self.data = (self * rotation_matrix).data
        return self

    def rank(self):
        if self.rows != self.columns:
            raise EngineException(EngineException.WRONG_SIZE)
        
        rank = self.columns
        for row in range(0, rank):
            if self[row][row] != 0:
                for col in range(0, self.rows, 1):
                    if col != row:
                        multiplier = (self[col][row] /
                                        self[row][row])
                        for i in range(rank):
                            self[col][i] -= (multiplier *
                                                self[row][i])
            else:
                reduce = True
                for i in range(row + 1, self.rows, 1):
                    if self[i][row] != 0:
                        self.swap(self, row, i, rank)
                        reduce = False
                        break
                if reduce:
                    rank -= 1
                    for i in range(0, self.rows, 1):
                        self[i][row] = self[i][rank]
                row -= 1
        return rank

    def __mul__(self, obj: 'Matrix'):
        return Matrix.__product(self, obj)

    __rmul__ = __mul__

    def __sub__(self, obj: 'Matrix'):
        return self + (obj*(-1))

    def __getitem__(self, key: int):
        return self.data[key]

    def __setitem__(self, key: int, item):
        self.data[key] = item
        return self

    def __repr__(self):
        return f'{self.data}'

    def __truediv__(self, obj: Union['Matrix', int, float]):
        if not (isinstance(self, Matrix) or \
          isinstance(obj, (int, float)) or isinstance(obj, Matrix)):
            raise EngineException(EngineException.WRONG_USAGE)

        if isinstance(obj, (int, float)):
            return self * (1/obj)
        elif isinstance(obj, Matrix):
            return self * obj.inverse()

    def __rtruediv__(self, obj):
        raise EngineException(EngineException.WRONG_USAGE)

class Vector(Matrix):
    def __init__(self, values: Union[list[float], list[list[float]], Matrix]):
        if not isinstance(values, list) and not isinstance(values, Matrix):
            raise EngineException(EngineException.WRONG_USAGE)

        if isinstance(values, Matrix):
            if 1 not in (values.rows, values.columns):
                raise EngineException(EngineException.WRONG_SIZE)

            self.size = [x for x in (values.rows, values.columns) if x != 1]
            values = values.data
          
        if isinstance(values, list) and isinstance(values[0], list):
            for i in range(len(values)-1):
                if len(values[i]) != len(values[i+1]):
                    raise EngineException(EngineException.RECTANGULAR_MATRIX)

        if isinstance(values[0], list):
            self.is_transposed = len(values[0]) == 1
            if len(values[0]) == 1:     # [[1], [2], [3]]
                self.values = values
                self.size = len(values)
            else:                       # [[1, 2, 3]]
                self.values = values[0]
                self.size = len(values[0])

        elif isinstance(values[0], (int, float)):  # [1, 2, 3]
            self.values = values
            self.is_transposed = False
            self.size = len(values)

    def as_matrix(self):
        return Matrix(self)

    def transpose(self):
        temp = Vector(self.as_matrix().transpose())
        self.values = temp.values
        self.is_transposed = not (self.is_transposed)
        return self
    
    def len(self):
        return (self & self)**0.5

    def rotate(self, axes_indecies: list[int], angle: float):
        if self.is_transposed == False:
            self.values = self.as_matrix().rotate(axes_indecies, angle).data[0]
            return self
        self.values = self.transpose().as_matrix().rotate(
            axes_indecies, angle).transpose().data
        return self

    def __scalar_product(self, obj: 'Vector'):
        if self.size != obj.size:
            raise EngineException(EngineException.WRONG_SIZE)
        
        identity = Matrix.identity_matrix(self.size)
        return BilinearForm(identity, self, obj)

    def __vector_product(self, obj: 'Vector'):
        if self.size != 3:
            raise EngineException(EngineException.DIMENSION_ERROR)
        
        basis = globals.coord_system.vs.basis
        
        bas1 = vector_product(basis[1], basis[2])
        bas2 = vector_product(basis[2], basis[0])
        bas3 = vector_product(basis[0], basis[1])
        
        res_vec1 = bas1 * (self[1]*obj[2] - self[2]*obj[1])
        res_vec2 = bas2 * (self[2]*obj[0] - self[0]*obj[2])
        res_vec3 = bas3 * (self[0]*obj[1] - self[1]*obj[0])
        
        return res_vec1+res_vec2+res_vec3

    def __add__(self, obj: 'Vector'):
        if not (isinstance(self, Vector) and isinstance(obj, Vector)):
            raise EngineException(EngineException.WRONG_USAGE)
        if self.size != obj.size:
            raise EngineException(EngineException.WRONG_SIZE)
        
        if self.is_transposed == True and obj.is_transposed == True:
            return Vector((self.as_matrix()+obj.as_matrix()))
        
        if self.is_transposed == True:
            self.transpose()
            
        if obj.is_transposed == True:
            obj.transpose()
        
        return Vector((self.as_matrix()+obj.as_matrix()))
        

    def __and__(self, obj: 'Vector'):
        return Vector.__scalar_product(self, obj)

    def __mul__(self, obj: Union[int, float, 'Vector']):
        if isinstance(obj, Vector):
            result = self.as_matrix() * obj.as_matrix()
            return Vector(result)
        elif isinstance(obj, (int, float)):
            result = self.as_matrix() * obj
            return Vector(result)
        raise EngineException(EngineException.WRONG_USAGE)

    __rmul__ = __mul__

    def __pow__(self, obj: 'Vector'):
        return Vector.__vector_product(self, obj)

    def __sub__(self, obj: 'Vector'):
        return self + (obj*(-1))

    def __repr__(self):
        return f'{self.values}'

    def __eq__(self, obj: 'Vector'):
        return self.as_matrix() == obj.as_matrix()
    
    def __getitem__(self, key: int):
        if self.is_transposed == False:
            return self.values[key]
        return self.values[key][0]

    zero_matrix = restricted
    identity_matrix = restricted
    copy = restricted
    __setitem__ = restricted
    determinant = restricted
    inverse = restricted
    gram = restricted
    rank = restricted
    
def BilinearForm(matrix: Matrix, vec1: Vector, vec2: Vector):
    if not (matrix.rows == matrix.columns and matrix.rows == vec1.size and \
            matrix.rows == vec2.size):
        raise EngineException(EngineException.WRONG_SIZE)
    
    sum = 0
    for i in range(matrix.rows):
        for j in range(matrix.rows):
            sum += matrix[i][j]*vec1[i]*vec2[j]
    return sum

def vector_product(vec1: 'Vector', vec2: 'Vector'):
        return Vector([vec1[1]*vec2[2] - vec1[2]*vec2[1],
                       vec1[2]*vec2[0] - vec1[0]*vec2[2],
                       vec1[0]*vec2[1] - vec1[1]*vec2[0]])

class Point(Vector):
    def __add__(self, vector: Vector):
        if not isinstance(vector, Vector):
            raise EngineException(EngineException.WRONG_USAGE)
        if self.size != vector.size:
            raise EngineException(EngineException.WRONG_SIZE)
        
        return Point([self.values[i]+vector.values[i]
                        for i in range(self.size)])

    __radd__ = __add__

    def __sub__(self, vector: Vector):
        if not isinstance(vector, Vector):
            raise EngineException(EngineException.WRONG_USAGE)
        if self.size != vector.size:
            raise EngineException(EngineException.WRONG_SIZE)
        
        return Point([self.values[i]-vector.values[i]
                        for i in range(self.size)])

    __mul__ = restricted
    __rmul__ = restricted
    __and__ = restricted
    __pow__ = restricted
    transpose = restricted
    len = restricted


class VectorSpace:
    def __init__(self, basis: list[Vector]):
        matrix = Matrix([vec.values for vec in basis])
        
        if matrix.rank() != matrix.rows or matrix.determinant == 0:
            raise EngineException(EngineException.BASIS_ERROR)
        
        self.basis = matrix
        self.size = len(basis)

    def scalar_product(self, vec1: Vector, vec2: Vector):
        if vec1.is_transposed:
            vec1 = vec1.transpose()

        if not vec2.is_transposed:
            vec2 = vec2.transpose()

        return (vec1.as_matrix() * Matrix.gram(self.basis) * vec2.as_matrix())[0][0]
    
    # def vector_product(self, vec1: Vector, vec2: Vector):
    #     if self.size != 3:
    #         raise EngineException(EngineException.DIMENSION_ERROR)
        
    #     bas1 = vector_product(self.basis[1], self.basis[2])
    #     bas2 = vector_product(self.basis[2], self.basis[0])
    #     bas3 = vector_product(self.basis[0], self.basis[1])
        
    #     res_vec1 = bas1 * (vec1[1]*vec2[2] - vec1[2]*vec2[1])
    #     res_vec2 = bas2 * (vec1[2]*vec2[0] - vec1[0]*vec2[2])
    #     res_vec3 = bas3 * (vec1[0]*vec2[1] - vec1[1]*vec2[0])
        
    #     return res_vec1+res_vec2+res_vec3

    def as_vector(self, point: Point):
        if point.size != self.size:
            raise EngineException(EngineException.WRONG_SIZE)
        
        result = Matrix.zero_matrix(1, point.size)
        det = self.basis.determinant()
        for column in range(point.size):
            temp_matrix = self.basis.copy().transpose()
            for row in range(point.size):
                temp_matrix[row][column] = point[row]
            result[0][column] = temp_matrix.determinant() / det
        return Vector(result)


class CoordinateSystem:
    def __init__(self, initial_point: Point, vs: VectorSpace):
        self.initial_point = initial_point
        self.vs = vs
