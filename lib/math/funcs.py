from lib.exceptions.math_exc import MathException


@property
def restricted(self):
    raise AttributeError(f'{self.__class__} does not have this attribite')


def BilinearForm(matrix, vec1, vec2):
    if not (matrix.rows == matrix.columns and matrix.rows == vec1.size and
            matrix.rows == vec2.size):
        raise MathException(MathException.WRONG_SIZE)

    sum = 0
    for i in range(matrix.rows):
        for j in range(matrix.rows):
            sum += matrix[i][j]*vec1[i]*vec2[j]
    return sum