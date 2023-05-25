from lib.exceptions.math_exc import MathException
from lib.math.funcs import restricted
from lib.math.matrix_vector import Vector


class Point(Vector):
    def addition(self, vector: Vector):
        if not isinstance(vector, Vector):
            raise MathException(MathException.WRONG_USAGE)
        if self.size != vector.size:
            raise MathException(MathException.WRONG_SIZE)

        return Point([self.values[i]+vector.values[i]
                      for i in range(self.size)])
    
    def subtraction(self, vector: Vector):
        if not isinstance(vector, Vector):
            raise MathException(MathException.WRONG_USAGE)
        if self.size != vector.size:
            raise MathException(MathException.WRONG_SIZE)

        return Point([self.values[i]-vector.values[i]
                      for i in range(self.size)])
    
    def __add__(self, vector: Vector):
        return self.addition(vector)

    __radd__ = __add__

    def __sub__(self, vector: Vector):
        return self.subtraction(vector)

    __mul__ = restricted
    __rmul__ = restricted
    __and__ = restricted
    __pow__ = restricted
    transpose = restricted
    len = restricted
