from math import cos, pi, sin
from typing import Union
from lib.math.funcs import BilinearForm, restricted
from lib.exceptions.math_exc import MathException

import src.globals as globals


class Matrix:
    def __init__(self, data: Union[list[list[float]], 'Vector']):
        if isinstance(data, Vector):
            if data.is_transposed:
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
                    raise MathException(MathException.RECTANGULAR_MATRIX)

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
    
    def equalize(self, obj: 'Matrix'):
        if not (self.rows == obj.rows and self.columns == obj.columns):
            return False

        eps = 10**(-7)
        return all(abs(self[i][j] - obj[i][j]) < eps
                   for i in range(self.rows)
                   for j in range(self.columns))
        
    def addition(self, obj: 'Matrix'):
        if not isinstance(obj, Matrix):
            raise MathException(MathException.WRONG_USAGE)

        if not (self.rows == obj.rows and self.columns == obj.columns):
            raise MathException(MathException.WRONG_SIZE)

        result = Matrix.zero_matrix(self.rows, self.columns)
        result.data = [[self.data[row][column] + obj.data[row][column]
                        for column in range(self.columns)]
                       for row in range(self.rows)]
        return result

    def product(obj1: Union['Matrix', float, int],
                  obj2: Union['Matrix', float, int]):
        if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
            if not (obj1.columns == obj2.rows):
                raise MathException(MathException.WRONG_SIZE)

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
            return Matrix.product(obj2, obj1)

        else:
            raise MathException(MathException.WRONG_USAGE)

    def minor(self, i: int, j: int):
        minor_data = self.copy().data
        minor_data.pop(i)
        for row in range(len(minor_data)):
            minor_data[row].pop(j)
        return Matrix(minor_data)

    def determinant(self):
        if isinstance(self, Matrix):
            matrix = self.data
        else:
            matrix = self

        if not (len(matrix) == len(matrix[0])):
            raise MathException(MathException.QUADRATIC_MATRIX)

        if self.rows == 1:
            return self.data[0][0]

        elif isinstance(self.data[0][0], (int, float)):
            size = self.columns
            result = 0
            for index in range(size):
                submatrix = self.minor(0, index)
                det = submatrix.determinant()
                result += (-1)**index * det * self.data[0][index]
        else:
            size = self.columns
            result = Vector([0, 0, 0])
            for index in range(size):
                submatrix = self.minor(0, index)
                det = submatrix.determinant()
                result += (-1)**index * det * self.data[0][index]
        return result

    def inverse(self):
        determinant = Matrix.determinant(self)

        if determinant == 0:
            raise MathException(MathException.SINGULAR_MATRIX)

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
            raise MathException(MathException.QUADRATIC_MATRIX)

        result = Matrix.zero_matrix(self.rows, self.rows)
        identity = Matrix.identity_matrix(self.rows)
        for i in range(self.rows):
            for j in range(self.columns):
                result[i][j] = BilinearForm(
                    identity, Vector(self[i]), Vector(self[j]))
        return result

    def transpose(self):
        if not isinstance(self, Matrix):
            raise MathException(MathException.WRONG_USAGE)

        self.data = [[self[j][i] for j in range(self.rows)]
                     for i in range(self.columns)]
        self.rows, self.columns = self.columns, self.rows
        return self

    def rotate(self, axes_indecies: list[int], angle: float):
        angle = angle*pi/180

        rotation_matrix = Matrix.identity_matrix(self.rows)

        n = (-1)**(axes_indecies[0] + axes_indecies[1] + 1)

        rotation_matrix[axes_indecies[0]][axes_indecies[0]] = cos(angle)
        rotation_matrix[axes_indecies[1]][axes_indecies[1]] = cos(angle)

        rotation_matrix[axes_indecies[1]][axes_indecies[0]] = n * sin(angle)
        rotation_matrix[axes_indecies[0]][axes_indecies[1]] = (-n) * sin(angle)

        self.data = (rotation_matrix * self).data
        return self
    
    def rotate_3d(self, angles: list[Union[int, float]]):
        if self.columns == 2 or self.rows == 2:
            angle = angles[0]*pi/180
            rotation_matrix = Matrix([[cos(angle), -sin(angle)],
                                      [sin(angle), cos(angle)]])
            self.data = (rotation_matrix * self).data
            return self
        
        if self.columns == 3 or self.rows == 3:
            angle_x, angle_y, angle_z = angles[0]*pi/180, angles[1]*pi/180, angles[2]*pi/180
            rotation_matrix_x = Matrix([[1, 0, 0],
                                        [0, cos(angle_x), -sin(angle_x)],
                                        [0, sin(angle_x), cos(angle_x)]])
            rotation_matrix_y = Matrix([[cos(angle_y), 0, -sin(angle_y)],
                                        [0, 1, 0],
                                        [sin(angle_y), 0, cos(angle_y)]])
            rotation_matrix_z = Matrix([[cos(angle_z), -sin(angle_z), 0],
                                        [sin(angle_z), cos(angle_z), 0],
                                        [0, 0, 1]])
                        
            self.data = (rotation_matrix_x *
                         rotation_matrix_y * rotation_matrix_z * self).data
            return self
        
        else:
            raise MathException(MathException.DIMENSION_ERROR(3))

    def rank(self):
        if self.rows != self.columns:
            raise MathException(MathException.WRONG_SIZE)

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
    
    def division(self, obj: 'Matrix'):
        if not (isinstance(self, Matrix) or
                isinstance(obj, (int, float)) or isinstance(obj, Matrix)):
            raise MathException(MathException.WRONG_USAGE)

        if isinstance(obj, (int, float)):
            return self * (1/obj)
        elif isinstance(obj, Matrix):
            return self * obj.inverse()
    
    def __eq__(self, obj: 'Matrix'):
        return self.equalize(obj)

    def __add__(self, obj: 'Matrix'):
        return self.addition(obj)

    def __mul__(self, obj: 'Matrix'):
        return Matrix.product(self, obj)

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
        return self.division(obj)

    def __rtruediv__(self, obj):
        raise MathException(MathException.WRONG_USAGE)


class Vector(Matrix):
    def __init__(self, values: Union[list[float], list[list[float]], Matrix]):
        if not isinstance(values, list) and not isinstance(values, Matrix):
            raise MathException(MathException.WRONG_USAGE)
        
        if isinstance(values[0], Vector):   # Vector([Vector])
            self.is_transposed = False
            self.values = [x for x in values]
            
        if isinstance(values, Matrix):
            if 1 not in (values.rows, values.columns):
                raise MathException(MathException.WRONG_SIZE)

            self.size = [x for x in (values.rows, values.columns) if x != 1]
            values = values.data

        if isinstance(values, list) and isinstance(values[0], list):
            for i in range(len(values)-1):
                if len(values[i]) != len(values[i+1]):
                    raise MathException(MathException.RECTANGULAR_MATRIX)

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

    def len(self) -> Union[int, float]:
        return (self & self)**0.5

    def rotate(self, axes_indecies: list[int], angle: float):
        if self.is_transposed == False:
            self.values = self.transpose().as_matrix().rotate(axes_indecies, angle).data
            return self.transpose()
        
        self.values = self.as_matrix().rotate(
            axes_indecies, angle).data
        return self
    
    def rotate_3d(self, angles: list[Union[int, float]]):
        if self.is_transposed:
            self.values = self.as_matrix().rotate_3d(angles).data
            return self
        
        else:
            self.values = self.transpose().as_matrix().rotate_3d(angles).data
            return self.transpose()
        
    def norm(self):
        return self/self.len()

    def copy(self):
        return Vector(self.as_matrix().copy())

    def scalar_product(vec1: 'Vector', vec2: 'Vector'):
        vs = globals.cs.vs

        if vec1.is_transposed:
            vec1 = vec1.copy().transpose()

        if not vec2.is_transposed:
            vec2 = vec2.copy().transpose()

        return (vec1.as_matrix() * Matrix.gram(vs.basis) * vec2.as_matrix())[0][0]

    def __additional_vec_prod(self, obj: 'Vector'):
        if not isinstance(obj, Vector):
            raise MathException(MathException.WRONG_USAGE)

        if not (self.size == 3 and obj.size == 3):
            raise MathException(MathException.WRONG_SIZE)

        v1 = Vector([1, 0, 0])
        v2 = Vector([0, 1, 0])
        v3 = Vector([0, 0, 1])
        m = Matrix([[v1, v2, v3], self.values, obj.values])
        return m.determinant()

    def vector_product(vec1, vec2: 'Vector'):
        if not isinstance(vec2, Vector):
            raise MathException(MathException.WRONG_USAGE)

        else:
            if not (vec1.size == 3 and vec2.size == 3):
                raise MathException(MathException.WRONG_SIZE)

            else:
                vs = globals.cs.vs

                basis_v1 = Vector(vs.basis[0])
                basis_v2 = Vector(vs.basis[1])
                basis_v3 = Vector(vs.basis[2])

                v1 = basis_v2.__additional_vec_prod(basis_v3)
                v2 = basis_v3.__additional_vec_prod(basis_v1)
                v3 = basis_v1.__additional_vec_prod(basis_v2)

                m = Matrix([[v1, v2, v3], vec1.values, vec2.values])
                return m.determinant()

    def addition(self, obj: 'Vector'):
        if not (isinstance(self, Vector) and isinstance(obj, Vector)):
            raise MathException(MathException.WRONG_USAGE)
        if self.size != obj.size:
            raise MathException(MathException.WRONG_SIZE)

        if self.is_transposed == True and obj.is_transposed == True:
            return Vector((self.as_matrix()+obj.as_matrix()))

        if self.is_transposed == True:
            self.transpose()

        if obj.is_transposed == True:
            obj.transpose()

        return Vector((self.as_matrix()+obj.as_matrix()))
    
    def multiply(self, obj: Union[int, float, 'Vector']):
        if isinstance(obj, Vector):
            result = self.as_matrix() * obj.as_matrix()
            return Vector(result)
        elif isinstance(obj, (int, float)):
            result = self.as_matrix() * obj
            return Vector(result)
        raise MathException(MathException.WRONG_USAGE)
    
    def division(self, obj: Union[int, float]):
        if not isinstance(obj, (int, float)):
            return MathException(MathException.WRONG_USAGE)
        
        data = self.values
        
        for i in range(len(data)):
            data[i] = data[i]/obj
            
        self.values = data
        return self

    def __add__(self, obj: 'Vector'):
        return self.addition(obj)

    def __and__(self, obj: 'Vector'):
        return Vector.scalar_product(self, obj)

    def __mul__(self, obj: Union[int, float, 'Vector']):
        return self.multiply(obj)

    __rmul__ = __mul__

    def __pow__(self, obj: 'Vector'):
        return Vector.vector_product(self, obj)

    def __sub__(self, obj: 'Vector'):
        return self + (obj*(-1))

    def __repr__(self):
        return f'{self.values}'

    def __eq__(self, obj: 'Vector'):
        if obj == None:
            return False
        return self.as_matrix() == obj.as_matrix()

    def __getitem__(self, key: int):
        if self.is_transposed == False:
            return self.values[key]
        return self.values[key][0]
    
    def __setitem__(self, key: int, item):
        if self.is_transposed:
            self.values[key][0] = item
        else:
            self.values[key] = item
  
    def __truediv__(self, obj: Union[int, float]):
        return self.division(obj)

    zero_matrix = restricted
    identity_matrix = restricted
    determinant = restricted
    inverse = restricted
    gram = restricted
    rank = restricted