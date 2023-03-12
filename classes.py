import sys

class Point:
    def __init__(self, c1: float, c2: float, c3: float):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        
    def as_list(self):
        return [self.c1, self.c2, self.c3]
    
    def distance(point1: __init__, point2: __init__):
        return ((point1.c1 - point2.c1)**2 + (point1.c2 - point2.c2)**2 
                + (point1.c3 - point2.c3)**2)**0.5
        
    # def distance(self, point2: __init__):
    #     return ((self.c1 - point2.c1)**2 + (self.c2 - point2.c2)**2 
    #             + (self.c3 - point2.c3)**2)**0.5
            
    def __add__(self, another_point: __init__):
        return Point(
            c1 = self.c1 + another_point.c1,
            c2 = self.c2 + another_point.c2,
            c3 = self.c3 + another_point.c3
        )
        
    def __mul__(self, scalar: float):
        return Point(
            c1 = self.c1 * scalar,
            c2 = self.c2 * scalar,
            c3 = self.c3 * scalar
        )
        
    def __sub__(self, another_point: __init__):
        return self+(another_point*(-1))
    
    def __truediv__(self, scalar: float):
        if scalar == 0:
            print({"msg": "division by zero"})
            sys.exit()
        return Point(
            c1 = self.c1 / scalar,
            c2 = self.c2 / scalar,
            c3 = self.c3 / scalar
        )
        
class VectorSpace:
    def __init__(self, point: Point):
        self.initial_point = point
            
class Vector():
    def __init__(self, c1: float = None,
                 c2: float = None, c3: float = None):
        if type(c1) == int or type(c1) == float:
            self.c1 = c1
            self.c2 = c2
            self.c3 = c3
        
        else:    
            self.c1 = c1.c1
            self.c2 = c1.c2
            self.c3 = c1.c3
    
    def as_list(self):
        return [self.c1, self.c2, self.c3]
    
    def as_point(self):
        return Point(c1 = self.c1, c2 = self.c2, c3 = self.c3)
    
    def len(self):
        return Point.distance(VectorSpace.initial_point, self)
    
    def __add__(self, another_point: __init__):
        return Point(
            c1 = self.c1 + another_point.c1,
            c2 = self.c2 + another_point.c2,
            c3 = self.c3 + another_point.c3
        )
    
    def __mul__(self, scalar_or_vector: __init__):
        
        if type(scalar_or_vector) == int or type(scalar_or_vector) == float:
            return Vector(
                c1 = self.c1 * scalar_or_vector,
                c2 = self.c2 * scalar_or_vector,
                c3 = self.c3 * scalar_or_vector
            )
            
        scalar_or_vector = scalar_or_vector.as_list()
        another_vector = Vector(c1 = scalar_or_vector[0],
                                c2 = scalar_or_vector[1],
                                c3 = scalar_or_vector[2])
        return (self.c1 * another_vector.c1 + self.c2 * another_vector.c2 + 
            self.c3 * another_vector.c3)
        
    def __pow__(self, another_vector: __init__):
        return Vector(
            self.c2 * another_vector.c3 - self.c3 * another_vector.c2,
            self.c3 * another_vector.c1 - self.c1 * another_vector.c3,
            self.c1 * another_vector.c2 - self.c2 * another_vector.c1
        )
        
    def mixed_mul(vec1: __init__, vec2: __init__, vec3: __init__):
        return vec1 * (vec2 ** vec3)
        
    # смешанное произведение
    
    
    


    
    
point= Point(c1 = 0, c2 = 0, c3 = 0)

VectorSpace.initial_point = point

point1 = Point(
    c1 = 1, c2 = 1, c3 = 1
)

vec1 = Vector(
    point1
)

vec2 = Vector(
    c1=3, c2=2, c3=2
)

vec3 = Vector(
    c1=32, c2=33, c3=21
)

print(Vector.mixed_mul(vec1, vec2, vec3))