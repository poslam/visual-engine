from typing import Union
class Matrix:
    def __init__(self, data: list[list[float]]):
        self.data = data
        self.rows = len(data)
        self.columns = len(data[0])
        
    def zero_matrix(rows: int, columns: int):
        data = [[0 for j in range(columns)] for i in range(rows)]
        return Matrix(data)
    
    def identity_matrix(size: int):
        result = Matrix.zero_matrix(size, size)
        for i in range(size):
            for j in range(size):
                if i == j: result.data[i][j] = 1
        return result
                   
    def __add__(self, obj: 'Matrix'):
        if isinstance(self, Vector) and isinstance(obj, Vector):
            self, obj = self.as_matrix, obj.as_matrix
            result = Matrix.zero_matrix(self.rows, self.columns)
            if self.rows == obj.rows and self.columns == obj.columns:
                result.data = [[self.data[row][column] + obj.data[row][column] 
                             for column in range(self.columns)] 
                             for row in range(self.rows)]
                if len(result.data[0]) == 1:
                    return Vector(result)
                return Vector(result[0])
            raise Exception("different sizes")
        if isinstance(obj, Matrix):
            result = Matrix.zero_matrix(self.rows, self.columns)
            if self.rows == obj.rows and self.columns == obj.columns:
                result.data = [[self.data[row][column] + obj.data[row][column] 
                             for column in range(self.columns)] 
                             for row in range(self.rows)]
                return result
            raise Exception("different sizes")
        raise TypeError("wrong usage of addition")
    
    def __iadd__(self, obj: 'Matrix'):
        if isinstance(obj, Matrix):
            if self.rows == obj.rows and self.columns == obj.columns:
                self.data = [[self.data[row][column] + obj.data[row][column] 
                             for column in range(self.columns)] 
                             for row in range(self.rows)]
                return self
            raise Exception("different sizes")
        raise TypeError("not a matrix")
    
    def __product(self, obj1: Union['Matrix', float, int], 
                obj2: Union['Matrix', float, int]):
        if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
            if obj1.columns == obj2.rows:
                result = [[sum(a * b for a, b in zip(A_row, B_col))
                            for B_col in zip(*obj2.data)]
                                      for A_row in obj1.data]
                return Matrix(result)
            raise Exception("wrong sizes")
            
        elif isinstance(obj1, (float, int)) and isinstance(obj2, Matrix):
            result = Matrix.zero_matrix(obj2.rows, obj2.columns)
            for i in range(obj2.rows):
                for j in range(obj2.columns):
                    result.data[i][j] *= obj1
            return result
                
        elif isinstance(obj1, Matrix) and isinstance(obj2, (float, int)):
            result = Matrix.zero_matrix(obj1.rows, obj1.columns)
            for i in range(obj1.rows):
                for j in range(obj1.columns):
                    result.data[i][j] = obj1.data[i][j] * obj2
            return result
            
        raise Exception("not a matrix or a scalar")
    
    def __iproduct(self, obj1: Union['Matrix', float, int], 
                 obj2: Union['Matrix', float, int]):
        if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
            if obj1.columns == obj2.rows:
                result = Matrix.zero_matrix(obj2.rows, obj2.columns)
                for i in range(obj1.rows):  
                    for j in range(obj2.columns):  
                        for k in range(obj2.rows):
                            result[i][j] += obj1[i][k] * obj2[k][j]  
                obj1.data = result.data
                return obj1
            raise Exception("wrong sizes")
            
        elif isinstance(obj1, Matrix) and isinstance(obj2, (float, int)):
            for i in range(obj1.columns):
                for j in range(obj1.rows):
                    obj1[i][j] *= obj2
            return obj1
        
        raise Exception("not a matrix or a scalar")
    
    def copy(self):
        if isinstance(self, Vector):
            raise Exception('this operation is forbidden for vectors')
        result = Matrix.zero_matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                result[i][j] = self[i][j]
        return result
    
    def __mul__(self, obj: 'Matrix'):
        if isinstance(self, Matrix) and isinstance(obj, Matrix):
            return self.__product(self, obj)
        if isinstance(self, Matrix) and isinstance(obj, Vector):
            return self.__product(self, obj.as_matrix)
        if isinstance(self, Vector) and isinstance(obj, Matrix):
            return self.__product(self.as_matrix, obj)
        if isinstance(self, Vector) and isinstance(obj, Vector):
            return self.__product(self.as_matrix, obj.as_matrix)
    
    def __rmul__(self, obj: 'Matrix'):
        if isinstance(self, Matrix) and isinstance(obj, Matrix):
            return self.__product(self, obj)
        if isinstance(self, Matrix) and isinstance(obj, Vector):
            return self.__product(self, obj.as_matrix)
        if isinstance(self, Vector) and isinstance(obj, Matrix):
            return self.__product(self.as_matrix, obj)
        if isinstance(self, Vector) and isinstance(obj, Vector):
            return self.__product(self.as_matrix, obj.as_matrix)
    
    def __sub__(self, obj: 'Matrix'):
        if isinstance(obj, Vector):
            return self + (obj*(-1))
        if isinstance(obj, Matrix):
            return self + (obj*(-1))
        raise TypeError("wrong usage of subtraction")
    
    def __imul__(self, obj: 'Matrix'):
        return self.__iproduct(self, obj)
    
    def __getitem__(self, key: int):
        return self.data[key]
    
    def __setitem__(self, key: int, item):
        self.data[key] = item
        return self
    
    def __repr__(self):
        return f'{self.data}'
    
    def transpose(self):
        if isinstance(self, Vector):
            self = self.as_matrix
            data = [[self[j][i] for j in range(self.rows)] 
                    for i in range(self.columns)]
            self = Vector(data[0])
            return self
        if isinstance(self, Matrix):
            data = [[self[j][i] for j in range(self.rows)] 
                    for i in range(self.columns)]
            self = Matrix(data)
            return self
        if isinstance(self, list):
            return [[self[j][i] for j in range(len(self))] 
                    for i in range(len(self[0]))]

    def minor(self, i: int, j: int):
        if isinstance(self, Vector):
            raise Exception('this operation is forbidden for vectors')
        return [row[:j] + row[j+1:] for row in (self[:i]+self[i+1:])]

    def determinant(self):
        if isinstance(self, Vector):
            raise Exception('this operation is forbidden for vectors')
        if isinstance(self, Matrix): matrix = self.data
        else: matrix = self
        
        if len(matrix) == len(matrix):
            if len(matrix) == 2:
                return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
            
            determinant = 0
            for c in range(len(matrix)):
                determinant += ((-1)**c)*matrix[0][c]*\
                Matrix.determinant(Matrix.minor(matrix, 0, c))
            return determinant
        raise Exception("not quadratic matrix")

    def inverse(self):
        if isinstance(self, Vector):
            raise Exception('this operation is forbidden for vectors')
        determinant = Matrix.determinant(self)
        if determinant != 0:
            if self.rows == 2:
                return Matrix([[self[1][1]/determinant, -1*self[0][1]/determinant],
                        [-1*self[1][0]/determinant, self[0][0]/determinant]])

            cofactors = []
            for r in range(self.rows):
                cofactorRow = []
                for c in range(self.rows):
                    minor = Matrix.minor(self,r,c)
                    cofactorRow.append(((-1)**(r+c)) *
                                        Matrix.determinant(minor))
                cofactors.append(cofactorRow)
            cofactors = Matrix.transpose(cofactors)
            for r in range(len(cofactors)):
                for c in range(len(cofactors)):
                    cofactors[r][c] = cofactors[r][c]/determinant
            result = Matrix(cofactors)
            return result
        raise Exception("degenerate matrix")
    
    def gram(self):
        if isinstance(self, Vector):
            raise Exception('this operation is forbidden for vectors')
        if self.rows == self.columns:
            result = Matrix.zero_matrix(self.rows, self.rows)
            for i in range(self.rows):
                for j in range(self.rows):
                    sum = 0
                    for k in range(self.columns):
                        sum += self[i][k]*self[j][k]
                    result[i][j] = sum
            return result
        raise Exception("not a quadratic matrix")
    
    def __truediv__(self, obj: Union[int, float]):
        if isinstance(obj, (int, float)):
            return self * (1/obj)
        raise Exception("not a scalar")
    
    def __rtruediv__(self, obj):
        raise Exception("not commutative")
        
    
class Vector(Matrix):
    def __init__(self, values: Union[list[list[float]], Matrix]):
        if isinstance(values, Matrix):
            values = values.data
            if len(values[0]) == 1:
                self.as_matrix = Matrix(values)
                self.type = 'vertical'
            elif len(values) == 1:
                self.as_matrix = Matrix([values])
                self.type = 'horizontal'
            else:
                raise Exception('wrong size for a vector')
        elif isinstance(values[0], list):
            if len(values[0]) == 1:
                self.as_matrix = Matrix(values)
                self.type = 'vertical'
            elif len(values) == 1:
                self.as_matrix = Matrix([values])
                self.type = 'horizontal'
            else:
                raise Exception('wrong size for a vector')
        elif isinstance(values[0], (int, float)):
            self.as_matrix = Matrix([values])
            self.type = 'horizontal'
        self.values = values
        self.size = len(values)
        
        
    def __scalar_product(self, obj: 'Vector'):
        if isinstance(obj, Vector):
            result = self.as_matrix * obj.as_matrix.transpose()
            return result[0][0]
        raise Exception("not a vector")
    
    def __vector_product(self, obj: 'Vector'): # only 3d
        pass
    
    
    def __and__(self, obj: 'Vector'):
        return Vector.__scalar_product(self, obj)
    
    # def __mul__(self, obj: Union[int, float, 'Vector']):
    #     if isinstance(obj, Vector):
    #         result = self.as_matrix * obj.as_matrix
    #         return result
    #     elif isinstance(obj, (int, float)):
    #         result = self.as_matrix * obj
    #         return Vector(result.data[0])
        
    # def __rmul__(self, obj: Union[int, float, 'Vector']):
    #     if isinstance(obj, Vector):
    #         result = self.as_matrix * obj.as_matrix
    #         return result
    #     elif isinstance(obj, (int, float)):
    #         result = self.as_matrix * obj
    #         return result
        
    # def vector_product(self, vector: 'Vector'):
    # return Vector(
    #     self.c2 * vector.c3 - self.c3 * vector.c2,
    #     self.c3 * vector.c1 - self.c1 * vector.c3,
    #     self.c1 * vector.c2 - self.c2 * vector.c1
    # )
        
    def __repr__(self):
        return f'{self.values}'
    
    
def BilinearForm():
    pass

class VectorSpace:
    pass

class Point(Vector):
    pass

class CoorinateSystem:
    pass
        
    
# matrix1 = Matrix([[1, 2], 
#                   [3, 4]])
# matrix2 = Matrix([[1, 2], 
#                   [3, 3]])

# vec1 = Vector([1, 2, 3])
# vec2 = Vector([2, 3, 5])
# vec3 = Vector([[1], [2], [3]])

# x = Matrix.zero_matrix(2, 4)

# print(matrix1)


# matrix3 = matrix1.gram()
# print(matrix3)

# i = Matrix.identity_matrix(2)

# x = matrix1.inverse()
# # print(x.rows)

# # matrix2 -= matrix1

# print(matrix1*x)

