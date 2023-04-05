class RectangularcMatrix(Exception):
    def __init__(self):
        super().__init__("not a rectangular matrix (not enough elements)")


class WrongSizes(Exception):
    def __init__(self) -> None:
        super().__init__("different sizes, so operation isn't allowed")


class WrongUsage(Exception):
    def __init__(self) -> None:
        super().__init__("this operation is not allowed with this data")


class QuadraticMatrix(Exception):
    def __init__(self):
        super().__init__("this operation suports only quadratic matrices")


class SingularMatrix(Exception):
    def __init__(self) -> None:
        super().__init__("this operation supports only matrices with determinant\
                         not equal to zero")


class DimensionError(Exception):
    def __init__(self) -> None:
        super().__init__("this operation doesn't support that dimension")


