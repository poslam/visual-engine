import globals 
from typing import Union

class Point:
    def __init__(self, c1: float, c2: float, c3: float):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        
    def as_list(self):
        return [self.c1, self.c2, self.c3]
    
    def distance(self, point: __init__):
        return ((self.c1 - point.c1)**2 + (self.c2 - point.c2)**2 
                + (self.c3 - point.c3)**2)**0.5
            
    def __add__(self, another_point: __init__):
        return Point(
            c1 = self.c1 + another_point.c1,
            c2 = self.c2 + another_point.c2,
            c3 = self.c3 + another_point.c3
        )
        
    def __mul__(self, operand):
        return Point(
            c1 = self.c1 * operand,
            c2 = self.c2 * operand,                
            c3 = self.c3 * operand
        )
    
    def __rmul__(self, operand):
        return self.__mul__(operand)
        
    def __sub__(self, another_point: 'Point'):
        return self+(another_point*(-1))
    
    def __truediv__(self, scalar: float):
        if scalar == 0:
            raise Exception(ZeroDivisionError)
        
        return Point(
            c1 = self.c1 / scalar,
            c2 = self.c2 / scalar,
            c3 = self.c3 / scalar
        )
        
    def __repr__(self):
        return f"Point({self.c1}, {self.c2}, {self.c3})"
            
          
class Vector:
    def __init__(self, c1: Union[float, Point] = None,
                 c2: float = None, c3: float = None):
        if isinstance(c1, (int, float)):
            self.c1 = c1
            self.c2 = c2
            self.c3 = c3

        elif isinstance(c1, Point):   
            self.c1 = c1.c1
            self.c2 = c1.c2
            self.c3 = c1.c3
    
    def as_list(self):
        return [self.c1, self.c2, self.c3]
    
    def as_point(self):
        return Point(c1 = self.c1, c2 = self.c2, c3 = self.c3)
    
    def len(self):
        return Point.distance(globals.VSpace.initial_point, self)
    
    def __add__(self, another_vec: __init__):
        return Vector(
            c1 = self.c1 + another_vec.c1,
            c2 = self.c2 + another_vec.c2,
            c3 = self.c3 + another_vec.c3
        )
        
    def scalar_product(self, vector: 'Vector') -> Union[int, float]:
        return self.c1 * vector.c1 + self.c2 * vector.c2 + self.c3 * vector.c3
    
    def vector_product(self, vector: 'Vector'):
        return Vector(
            self.c2 * vector.c3 - self.c3 * vector.c2,
            self.c3 * vector.c1 - self.c1 * vector.c3,
            self.c1 * vector.c2 - self.c2 * vector.c1
        )
    
    def __mul__(self, object: Union[int, float, 'Vector']):
        
        if isinstance(object, (int, float)):
            return Vector(
                c1 = self.c1 * object,
                c2 = self.c2 * object,
                c3 = self.c3 * object
            )
        
        if isinstance(object, Vector):
            return self.scalar_product(object)
        
    def __rmul__(self, object: Union[int, float, 'Vector']):
        return self.__mul__(object)
    
    def __truediv__(self, scalar: float):
        if scalar == 0:
            raise Exception(ZeroDivisionError)
        
        return self*(1/scalar)

    def __pow__(self, object: 'Vector'):
        if isinstance(object, Vector):
            return self.vector_product(object)
        
    # @staticmethod
    # def mixed_mul(vec1: __init__, vec2: __init__, vec3: __init__):
    #     return vec1 * (vec2 ** vec3)
        
    def norm(self):
        return self*(1/self.len())
        
    def __repr__(self):
        return f"Vector({self.c1}, {self.c2}, {self.c3})"
        
        
class VectorSpace:
    initial_point = Point(0, 0, 0)
    
    def __init__(self, initial_point: Point,
                 e1: Vector, e2: Vector, e3: Vector):
        self.initial_point = initial_point
        self.e1 = e1.norm()
        self.e2 = e2.norm()
        self.e3 = e3.norm()

class Camera:
    def __init__(self, position: Point, look_dir_at: Union[Vector, Point], 
                 fov: float, k: float,
                 draw_distance: float):
        self.position = position
        self.look_dir_at = look_dir_at
        self.fov = fov
        self.vfov = 2/3*fov*k
        # k - коэффициент сжатия
        self.draw_distance = draw_distance
        
    def send_rays(self, amount_rays: int):
        pass
    
    
class Object:
    def __init__(self, position: Point, rotation: Vector):
        self.position = position
        self.rotation = position
        
    def contains(self, point: Point):
        return False
    
# class Ball(Object):
    
    # def contains(self, point: Point):
    #     return self.parameters.center.distance(point) <= self.parameters.radius
    
