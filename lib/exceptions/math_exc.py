class MathException(Exception):
    WRONG_SIZE = "different size, so operation isn't allowed"
    WRONG_USAGE = "this operation is not allowed with this data"
    DIMENSION_ERROR = lambda x: f"this operation doesn't support that dimension ({x} dimensions required)"
    RECTANGULAR_MATRIX = "not a rectangular matrix (not enough elements)" 
    BASIS_ERROR = "given matrix or list of vector is not a basis"
    QUADRATIC_MATRIX = "this operation suports only quadratic matrices"
    SINGULAR_MATRIX = "this operation supports only matrices with determinant not equal to zero"
    ZERO_DIVISION = "division by zero is forbidden"