from lib.math.point import Point
from lib.math.vs import VectorSpace


class CoordinateSystem:
    def __init__(self, initial_point: Point, vs: VectorSpace):
        self.initial_point = initial_point
        self.vs = vs