from lib.exceptions.math_exc import MathException
from lib.math.matrix_vector import Matrix
from lib.math.point import Point
from lib.math.matrix_vector import Vector


class VectorSpace:
    def __init__(self, basis: list[Vector]):
        matrix = Matrix([vec.values for vec in basis])

        if matrix.rank() != matrix.rows or matrix.determinant == 0:
            raise MathException(MathException.BASIS_ERROR)

        self.basis = matrix
        self.size = len(basis)

    def as_vector(self, point: Point):
        if point.size != self.size:
            raise MathException(MathException.WRONG_SIZE)

        result = Matrix.zero_matrix(1, point.size)
        det = self.basis.determinant()
        for column in range(point.size):
            temp_matrix = self.basis.copy().transpose()
            for row in range(point.size):
                temp_matrix[row][column] = point[row]
            result[0][column] = temp_matrix.determinant() / det
        return Vector(result)
