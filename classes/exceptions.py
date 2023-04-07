class EngineException(Exception):
    
    RECTANGULAR_MATRIX = "not a rectangular matrix (not enough elements)"
    WRONG_SIZES = "different sizes, so operation isn't allowed"
    WRONG_USAGE = "this operation is not allowed with this data"
    QUADRATIC_MATRIX = "this operation suports only quadratic matrices"
    SINGULAR_MATRIX = "this operation supports only matrices with determinant not equal to zero"
    DIMENSION_ERROR = lambda x: f"this operation doesn't support that dimension ({x} dimensions required)"
    


# import random
# if random() > 0.5:
#     raise EngineException(EngineException.RECTANGULAR_MATRIX)
# else:
#     raise EngineException(EngineException.WRONG_SIZES(1, 4))