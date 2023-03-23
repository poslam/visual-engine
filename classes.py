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
    
    def product(self, obj1: 'Matrix', obj2: 'Matrix'):
        if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
            result = [[sum(a * b for a, b in zip(A_row, B_col))
                        for B_col in zip(*obj2.data)]
                                for A_row in obj1.data]
            return Matrix(result, obj1.rows, obj2.columns)
        
        elif isinstance(obj1, (float, int)) and isinstance(obj2, Matrix):
            result = Matrix.zero_matrix(obj2.rows, obj2.columns)
            for i in range(obj2.rows):
                for j in range(obj2.columns):
                    result.data[i][j] *= obj1
            return result
            
        elif isinstance(obj1, Matrix) and isinstance(obj2, (float, int)):
            result = Matrix.zero_matrix(obj1.rows, obj1.columns)
            for i in range(obj1.columns):
                for j in range(obj1.rows):
                    result.data[i][j] = obj1.data[i][j] * obj2
            return result
        
        raise Exception("not a matrix or a scalar")
    
    def iproduct(self, obj1: 'Matrix', obj2: 'Matrix'):
        if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
            result = Matrix.zero_matrix(obj2.rows, obj2.columns)
            for i in range(obj1.rows):  
                for j in range(obj2.columns):  
                    for k in range(obj2.rows):
                        result[i][j] += obj1[i][k] * obj2[k][j]  
            obj1.data = result.data
            return obj1
            
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
        data = [[self[j][i] for j in range(self.rows)] 
                for i in range(self.columns)]
        self = Matrix(data, self.columns, self.rows)
        return self

    def getMatrixMinor(self, i: int, j: int):
        return [row[:j] + row[j+1:] for row in (self[:i]+self[i+1:])]

    def getMatrixDeternminant(self):
        if isinstance(self, Matrix): matrix = self.data
        else: matrix = self
        
        if len(matrix) == len(matrix):
            if len(matrix) == 2:
                return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
            
            determinant = 0
            for c in range(len(matrix)):
                determinant += ((-1)**c)*matrix[0][c]*\
                Matrix.getMatrixDeternminant(Matrix.getMatrixMinor(matrix, 0, c))
            return determinant
        raise Exception("not quadratic matrix")

    # def getMatrixInverse(m):
    #     determinant = Matrix.getMatrixDeternminant(m)
    #     #special case for 2x2 matrix:
    #     if len(m) == 2:
    #         return [[m[1][1]/determinant, -1*m[0][1]/determinant],
    #                 [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #     #find matrix of cofactors
    #     cofactors = []
    #     for r in range(len(m)):
    #         cofactorRow = []
    #         for c in range(len(m)):
    #             minor = Matrix.getMatrixMinor(m,r,c)
    #             cofactorRow.append(((-1)**(r+c)) * Matrix.getMatrixDeternminant(minor))
    #         cofactors.append(cofactorRow)
    #     cofactors = cofactors.transposeMatrix()
    #     for r in range(len(cofactors)):
    #         for c in range(len(cofactors)):
    #             cofactors[r][c] = cofactors[r][c]/determinant
    #     return cofactors
        

matrix1 = Matrix([[1, 2], [3, 4]], 2, 2)
matrix2 = Matrix([[2, 3, 3], [1, 0, 4], [2, 2, 56]], 3, 3)

i = Matrix.identity_matrix(5)
print(i)

x = matrix2.getMatrixDeternminant()

print(x)


# осталось сделать inverse и gram