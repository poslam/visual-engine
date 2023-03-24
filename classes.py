from typing import Union
class Matrix:
    def __init__(self, data: list[list[float]], rows: int, columns: int):
        self.data = data
        self.rows = rows
        self.columns = columns
        
        if self.rows != len(data):
            raise Exception("not enough rows")
        
        if any(self.columns != len(x) for x in data):
            raise Exception("not enough columns")
        
    def zero_matrix(rows: int, columns: int):
        data = [[0 for j in range(columns)] for i in range(rows)]
        return Matrix(data, rows, columns)
    
    def identity_matrix(size: int):
        result = Matrix.zero_matrix(size, size)
        for i in range(size):
            for j in range(size):
                if i == j: result.data[i][j] = 1
        return result
                   
    def __add__(self, obj: 'Matrix'):
        if isinstance(obj, Matrix):
            result = Matrix.zero_matrix(self.rows, self.columns)
            if self.rows == obj.rows and self.columns == obj.columns:
                result.data = [[self.data[row][column] + obj.data[row][column] 
                             for column in range(self.columns)] 
                             for row in range(self.rows)]
                return result
            raise Exception("different sizes")
        
        raise Exception("not a matrix")
    
    def __iadd__(self, obj: 'Matrix'):
        if isinstance(obj, Matrix):
            if self.rows == obj.rows and self.columns == obj.columns:
                self.data = [[self.data[row][column] + obj.data[row][column] 
                             for column in range(self.columns)] 
                             for row in range(self.rows)]
                return self
            raise Exception("different sizes")
        
        raise Exception("not a matrix")
    
    def product(self, obj1: Union['Matrix', float, int], 
                obj2: Union['Matrix', float, int]):
        if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
            if obj1.columns == obj2.rows:
                result = [[sum(a * b for a, b in zip(A_row, B_col))
                            for B_col in zip(*obj2.data)]
                                      for A_row in obj1.data]
                return Matrix(result, obj1.rows, obj2.columns)
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
    
    def iproduct(self, obj1: Union['Matrix', float, int], 
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
        result = Matrix.zero_matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                result[i][j] = self[i][j]
        return result
    
    def __mul__(self, obj: 'Matrix'):
        return self.product(self, obj)
    
    def __rmul__(self, obj: 'Matrix'):
        return self.product(self, obj)
    
    def __sub__(self, obj: 'Matrix'):
        if isinstance(obj, Matrix):
            return self + (obj*(-1))
        raise Exception("not a matrix")
    
    def __imul__(self, obj: 'Matrix'):
        return self.iproduct(self, obj)
    
    def __getitem__(self, key: int):
        return self.data[key]
    
    def __setitem__(self, key: int, item):
        self.data[key] = item
        return self
    
    def __repr__(self):
        return f'{self.data}'
    
    def transposeMatrix(self):
        if isinstance(self, Matrix):
            data = [[self[j][i] for j in range(self.rows)] 
                    for i in range(self.columns)]
            self = Matrix(data, self.columns, self.rows)
            return self
        if isinstance(self, list):
            return [[self[j][i] for j in range(len(self))] 
                    for i in range(len(self[0]))]

    def Minor(self, i: int, j: int):
        return [row[:j] + row[j+1:] for row in (self[:i]+self[i+1:])]

    def Determinant(self):
        if isinstance(self, Matrix): matrix = self.data
        else: matrix = self
        
        if len(matrix) == len(matrix):
            if len(matrix) == 2:
                return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
            
            determinant = 0
            for c in range(len(matrix)):
                determinant += ((-1)**c)*matrix[0][c]*\
                Matrix.Determinant(Matrix.Minor(matrix, 0, c))
            return determinant
        raise Exception("not quadratic matrix")

    def Inverese(matrix):
        if isinstance(matrix, Matrix):
            determinant = Matrix.Determinant(matrix)
            if determinant != 0:
                if matrix.rows == 2:
                    return Matrix([[matrix[1][1]/determinant, -1*matrix[0][1]/determinant],
                            [-1*matrix[1][0]/determinant, matrix[0][0]/determinant]], 2, 2)

                cofactors = []
                for r in range(matrix.rows):
                    cofactorRow = []
                    for c in range(matrix.rows):
                        minor = Matrix.Minor(matrix,r,c)
                        cofactorRow.append(((-1)**(r+c)) *
                                           Matrix.Determinant(minor))
                    cofactors.append(cofactorRow)
                cofactors = Matrix.transposeMatrix(cofactors)
                for r in range(len(cofactors)):
                    for c in range(len(cofactors)):
                        cofactors[r][c] = cofactors[r][c]/determinant
                result = Matrix(cofactors, len(cofactors), len(cofactors[0]))
                return result
            raise Exception("degenerate matrix")
        raise Exception("not a matrix")
    
    def gram(self):
        result = Matrix.zero_matrix(self.rows, self.rows)
        for i in range(self.rows):
            for j in range(self.rows):
                sum = 0
                for k in range(self.columns):
                    sum += self[i][k]*self[j][k]
                result[i][j] = sum
        return result
    
    
class Vector(Matrix):
    def __init__(self, values: list[list[float]]):
        if isinstance(values[0], list):
            self.as_matrix = Matrix(values, len(values), len(values[0]))
        else:
            self.as_matrix = Matrix([values], 1, len(values))
        self.values = values
        self.size = len(values)
        
    def scalar_product(self, obj: 'Matrix'):
        if isinstance(obj, Vector):
            result = self.as_matrix * obj.as_matrix.transposeMatrix()
            return result[0][0]
        raise Exception("not a vector")
    
    
    def __and__(self, obj: 'Vector'):
        return Vector.scalar_product(self, obj)
    
    def __mul__(self, obj: Union[int, float, 'Vector']):
        if isinstance(obj, Vector):
            result = self.as_matrix * obj.as_matrix
            return result
        elif isinstance(obj, (int, float)):
            result = self.as_matrix * obj
            return result
        
    def __rmul__(self, obj: Union[int, float, 'Vector']):
        if isinstance(obj, Vector):
            result = self.as_matrix * obj.as_matrix
            return result
        elif isinstance(obj, (int, float)):
            result = self.as_matrix * obj
            return result
        
        # def vector_product(self, vector: 'Vector'):
        # return Vector(
        #     self.c2 * vector.c3 - self.c3 * vector.c2,
        #     self.c3 * vector.c1 - self.c1 * vector.c3,
        #     self.c1 * vector.c2 - self.c2 * vector.c1
        # )
        
    def __repr__(self):
        return f'{self.values}'
        
    
        

matrix1 = Matrix([[1, 2], 
                  [3, 4]], 2, 2)
matrix2 = Matrix([[1, 2], 
                  [3, 3]], 2, 2)

matrix3 = Matrix([[1, 2, 3]], 1, 3)
matrix4 = Matrix([[2, 3, 5]], 1, 3)

vec1 = Vector([1, 2, 3])
vec2 = Vector([2, 3, 5])
vec3 = Vector([[2, 3], [3, 4], [5, 1]])

print(vec1*vec3)


# matrix3 = matrix1.gram()
# print(matrix3)

# i = Matrix.identity_matrix(2)

# x = matrix1.Inverese()
# # print(x.rows)

# # matrix2 -= matrix1

# print(matrix1*x)

