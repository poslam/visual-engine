class EngineException(Exception):
    WRONG_SIZE = "different size, so operation isn't allowed"
    WRONG_USAGE = "this operation is not allowed with this data"
    DIMENSION_ERROR = lambda x: f"this operation doesn't support that dimension ({x} dimensions required)"
    RECTANGULAR_MATRIX = "not a rectangular matrix (not enough elements)" 
    BASIS_ERROR = "given matrix or list of vector is not a basis"
    
class MatrixException(EngineException):   
    QUADRATIC_MATRIX = "this operation suports only quadratic matrices"
    SINGULAR_MATRIX = "this operation supports only matrices with determinant not equal to zero"
    
class GameException(Exception):
    NOT_FOUND_ERROR = lambda x: f"{x} doesn't exist"
    COLLISION_ERROR = "engine has a collision with entities id's"