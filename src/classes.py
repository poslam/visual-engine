from math import cos, pi, sin
from typing import Union

import src.globals
from src.exceptions import EngineException, MatrixException


@property
def restricted(self):
    raise AttributeError(f'{self.__class__} does not have this attribite')


class Matrix:
    def __init__(self, data: Union[list[list[float]], 'Vector']):
        if isinstance(data, Vector):
            data = [data.values]
        self.data = data
        self.rows = len(data)
        self.columns = len(data[0])
        for i in range(self.rows-1):
            if len(self.data[i]) != len(self.data[i+1]):
                raise MatrixException(MatrixException.RECTANGULAR_MATRIX)

    def zero_matrix(rows: int, columns: int):
        data = [[0 for j in range(columns)] for i in range(rows)]
        return Matrix(data)

    def identity_matrix(size: int):
        result = Matrix.zero_matrix(size, size)
        for i in range(size):
            result.data[i][i] = 1
        return result

    def __eq__(self, obj: 'Matrix'):
        if self.rows == obj.rows and self.columns == obj.columns:
            eps = 10**(-7)
            if all(abs(self[i][j] - obj[i][j]) < eps for i in range(self.rows) for j in range(self.columns)):
                return True
        return False

    def __add__(self, obj: 'Matrix'):
        if isinstance(obj, Matrix):
            result = Matrix.zero_matrix(self.rows, self.columns)
            if self.rows == obj.rows and self.columns == obj.columns:
                result.data = [[self.data[row][column] + obj.data[row][column]
                                for column in range(self.columns)]
                               for row in range(self.rows)]
                return result
            raise EngineException(EngineException.WRONG_SIZE)
        raise EngineException(EngineException.WRONG_USAGE)

    def __product(obj1: Union['Matrix', float, int],
                  obj2: Union['Matrix', float, int]):
        if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
            if obj1.columns == obj2.rows:
                result = [[sum(a * b for a, b in zip(A_row, B_col))
                           for B_col in zip(*obj2.data)]
                          for A_row in obj1.data]
                return Matrix(result)
            raise EngineException(EngineException.WRONG_USAGE)

        elif isinstance(obj1, (float, int)) and isinstance(obj2, Matrix):
            result = obj2.copy()
            for i in range(obj2.rows):
                for j in range(obj2.columns):
                    result.data[i][j] *= obj1
            return result

        elif isinstance(obj1, Matrix) and isinstance(obj2, (float, int)):
            return Matrix.__product(obj2, obj1)

    def copy(self):
        result = Matrix.zero_matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                result[i][j] = self[i][j]
        return result

    def __mul__(self, obj: 'Matrix'):
        if (isinstance(self, (Matrix, int, float))
                and isinstance(obj, (Matrix, int, float))):
            return Matrix.__product(self, obj)
        raise EngineException(EngineException.WRONG_USAGE)

    __rmul__ = __mul__

    def __sub__(self, obj: 'Matrix'):
        if isinstance(obj, Matrix):
            return self + (obj*(-1))
        raise EngineException(EngineException.WRONG_USAGE)

    def __getitem__(self, key: int):
        return self.data[key]

    def __setitem__(self, key: int, item):
        self.data[key] = item
        return self

    def __repr__(self):
        return f'{self.data}'

    def transpose(self):
        if isinstance(self, Matrix):
            self.data = [[self[j][i] for j in range(self.rows)]
                         for i in range(self.columns)]
            self.rows, self.columns = self.columns, self.rows
            return self
        if isinstance(self, list):
            return [[self[j][i] for j in range(len(self))]
                    for i in range(len(self[0]))]
        raise EngineException(EngineException.WRONG_USAGE)

    def __minor(self, i: int, j: int):
        return [row[:j] + row[j+1:] for row in (self[:i]+self[i+1:])]

    def determinant(self):
        if isinstance(self, Matrix):
            matrix = self.data
        else:
            matrix = self

        if len(matrix) == len(matrix[0]):
            if len(matrix) == 2:
                return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

            determinant = 0
            for c in range(len(matrix)):
                determinant += ((-1)**c)*matrix[0][c] *\
                    Matrix.determinant(Matrix.__minor(matrix, 0, c))
            return determinant
        raise MatrixException(MatrixException.QUADRATIC_MATRIX)

    def inverse(self):
        determinant = Matrix.determinant(self)
        if determinant != 0:
            if self.rows == 2:
                return Matrix([[self[1][1]/determinant, -1*self[0][1]/determinant],
                               [-1*self[1][0]/determinant, self[0][0]/determinant]])

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
            result = Matrix(cofactors)
            return result
        raise MatrixException(MatrixException.SINGULAR_MATRIX)

    def gram(self):
        if self.rows == self.columns:
            result = Matrix.zero_matrix(self.rows, self.rows)
            identity = Matrix.identity_matrix(self.rows)
            for i in range(self.rows):
                for j in range(self.columns):
                    result[i][j] = BilinearForm(
                        identity, Vector(self[i]), Vector(self[j]))
            return result
        raise MatrixException(MatrixException.QUADRATIC_MATRIX)

    def __truediv__(self, obj: Union['Matrix', int, float]):
        if isinstance(self, Matrix) and isinstance(obj, (int, float)):
            return self * (1/obj)
        if isinstance(self, Matrix) and isinstance(obj, Matrix):
            return self * obj.inverse()
        raise EngineException(EngineException.WRONG_USAGE)

    def __rtruediv__(self, obj):
        raise EngineException(EngineException.WRONG_USAGE)

    def rotate(self, angles: list[float]):
        '''
        angles in degrees
        '''
        if self.columns == 2:
            angle = angles[0]*pi/180
            rotation_matrix = Matrix([[cos(angle), -sin(angle)],
                                      [sin(angle), cos(angle)]])
            self.data = (self * rotation_matrix).data
            return self
        
        if self.columns == 3:
            angle_x, angle_y, angle_z = angles[0]*pi/180, angles[1]*pi/180, angles[2]*pi/180
            rotation_matrix_x = Matrix([[1, 0, 0],
                                        [0, cos(angle_x), -sin(angle_x)],
                                        [0, sin(angle_x), cos(angle_x)]])
            if globals.vs_space.triplet_left == False:
                rotation_matrix_y = Matrix([[cos(angle_y), 0, -sin(angle_y)],
                                            [0, 1, 0],
                                            [sin(angle_y), 0, cos(angle_y)]])
            else:
                rotation_matrix_y = Matrix([[cos(angle_y), 0, sin(angle_y)],
                                            [0, 1, 0],
                                            [-sin(angle_y), 0, cos(angle_y)]])
            rotation_matrix_z = Matrix([[cos(angle_z), -sin(angle_z), 0],
                                        [sin(angle_z), cos(angle_z), 0],
                                        [0, 0, 1]])
            self.data = (self * rotation_matrix_x *
                         rotation_matrix_y * rotation_matrix_z).data
            return self
        
        else:
            pass
        


class Vector(Matrix):
    def __init__(self, values: Union[list[list[float]], Matrix]):
        if isinstance(values, Matrix):
            values = values.data
        if isinstance(values[0], list):
            if len(values[0]) == 1:
                self.as_matrix = Matrix(values)
                self.values = values
                self.is_transposed = True
                self.size = len(values)
            elif len(values) == 1:
                self.as_matrix = Matrix(values)
                self.values = values[0]
                self.is_transposed = False
                self.size = len(values[0])
            else:
                raise Exception("wrong size for a vector")
        elif isinstance(values[0], (int, float)):
            self.as_matrix = Matrix([values])
            self.values = values
            self.is_transposed = False
            self.size = len(values)

    def transpose(self):
        temp = Vector(self.as_matrix.transpose())
        self.values = temp.values
        self.as_matrix = temp.as_matrix
        self.is_transposed = not (self.is_transposed)
        return self

    def __getitem__(self, key: int):
        if self.is_transposed == False:
            return self.values[key]
        return self.values[key][0]

    def __scalar_product(self, obj: 'Vector'):
        if self.size == obj.size:
            identity = Matrix.identity_matrix(self.size)
            return BilinearForm(identity, self, obj)
        raise EngineException(EngineException.WRONG_SIZE)

    def __vector_product(self, obj: 'Vector'):
        if self.size == 3 and obj.size == 3:
            return Vector([self[1]*obj[2] - self[2]*obj[1],
                           self[2]*obj[0] - self[0]*obj[2],
                           self[0]*obj[1] - self[1]*obj[0]])
        raise EngineException(EngineException.DIMENSION_ERROR(3))

    def __add__(self, obj: 'Vector'):
        if isinstance(self, Vector) and isinstance(obj, Vector):
            if self.size == obj.size:
                if self.is_transposed == False and obj.is_transposed == False:
                    return Vector((self.as_matrix+obj.as_matrix).data)
                elif self.is_transposed == True and obj.is_transposed == False:
                    return Vector((self.transpose().as_matrix+obj.as_matrix).data)
                elif self.is_transposed == False and obj.is_transposed == True:
                    return Vector((self.as_matrix+obj.transpose().as_matrix).data)
                return Vector((self.as_matrix+obj.as_matrix).data).transpose()
            raise EngineException(EngineException.WRONG_SIZE)
        raise EngineException(EngineException.WRONG_USAGE)

    def __and__(self, obj: 'Vector'):
        return Vector.__scalar_product(self, obj)

    def __mul__(self, obj: Union[int, float, 'Vector']):
        if isinstance(obj, Vector):
            result = self.as_matrix * obj.as_matrix
            return Vector(result)
        elif isinstance(obj, (int, float)):
            result = self.as_matrix * obj
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
        return self.as_matrix == obj.as_matrix

    def len(self):
        return (self & self)**0.5

    def rotate_2D(self, angle: float):
        '''
        angle in degrees
        '''
        if self.is_transposed == True:
            return Vector(self.transpose().as_matrix.rotate_2D(angle)).transpose()
        return Vector(self.as_matrix.rotate_2D(angle))

    def rotate_3D(self, angle_x: float, angle_y: float, angle_z: float):
        '''
        angles in degrees
        '''
        if self.is_transposed == True:
            return Vector(self.transpose().as_matrix.rotate_3D(angle_x, angle_y, angle_z)).transpose()
        return Vector(self.as_matrix.rotate_3D(angle_x, angle_y, angle_z))

    zero_matrix = restricted
    identity_matrix = restricted
    copy = restricted
    __setitem__ = restricted
    determinant = restricted
    inverse = restricted
    gram = restricted


def BilinearForm(matrix: Matrix, vec1: Vector, vec2: Vector):
    if matrix.rows == matrix.columns and matrix.rows == vec1.size and \
            matrix.rows == vec2.size:
        sum = 0
        for i in range(matrix.rows):
            for j in range(matrix.rows):
                sum += matrix[i][j]*vec1[i]*vec2[j]
        return sum
    raise EngineException(EngineException.WRONG_SIZE)


class Point(Vector):
    def __add__(self, vector: Vector):
        if isinstance(vector, Vector):
            if self.size == vector.size:
                return Point([self.values[i]+vector.values[i]
                              for i in range(self.size)])
            raise EngineException(EngineException.WRONG_SIZE)
        raise EngineException(EngineException.WRONG_USAGE)

    __radd__ = __add__

    def __sub__(self, vector: Vector):
        if isinstance(vector, Vector):
            if self.size == vector.size:
                return Point([self.values[i]-vector.values[i]
                              for i in range(self.size)])
            raise EngineException(EngineException.WRONG_SIZE)
        raise EngineException(EngineException.WRONG_USAGE)

    __mul__ = restricted
    __rmul__ = restricted
    __and__ = restricted
    __pow__ = restricted
    transpose = restricted
    len = restricted


class VectorSpace:
    def __init__(self, basis: list[Vector]):
        self.basis = Matrix([vec.values for vec in basis])
        self.size = len(basis)
        temp = basis[0]**basis[1]
        if temp&basis[2] / (temp.len()*basis[2].len()) == 1:
            self.triplet_left = False
        else:
            self.triplet_left = True
        

    def scalar_product(self, vec1: 'Vector', vec2: 'Vector'):
        if vec1.is_transposed == False and vec2.is_transposed == False:
            return (vec1.as_matrix*Matrix.gram(self.basis)*vec2.transpose().as_matrix)[0][0]
        elif vec1.is_transposed == False and vec2.is_transposed:
            return (vec1.as_matrix*Matrix.gram(self.basis)*vec2.as_matrix)[0][0]
        elif vec1.is_transposed and vec2.is_transposed:
            return (vec1.transpose().as_matrix*Matrix.gram(self.basis)*vec2.as_matrix)[0][0]
        elif vec1.is_transposed and vec2.is_transposed == False:
            return (vec1.transpose().as_matrix*Matrix.gram(self.basis)*vec2.transpose().as_matrix)[0][0]
        raise EngineException(EngineException.WRONG_USAGE)

    def as_vector(self, point: Point):
        if point.size == self.size:
            result = Matrix.zero_matrix(1, point.size)
            det = self.basis.determinant()
            for column in range(point.size):
                temp_matrix = self.basis.copy().transpose()
                for row in range(point.size):
                    temp_matrix[row][column] = point[row]
                result[0][column] = temp_matrix.determinant() / det
            return Vector(result)
        raise EngineException(EngineException.WRONG_SIZE)


class CoorinateSystem:
    def __init__(self, initial_point: Point, vs: VectorSpace):
        self.initial_point = initial_point
        self.vs = vs