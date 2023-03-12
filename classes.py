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
            
          
class Vector:
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
    
    def len(self, base):
        return Point.distance(base.initial_point, self)
    
    def __add__(self, another_vec: __init__):
        return Vector(
            c1 = self.c1 + another_vec.c1,
            c2 = self.c2 + another_vec.c2,
            c3 = self.c3 + another_vec.c3
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
        
    def norm(self, base):
        len = self.len(base)
        if len != 0:
            return Vector(
                c1= self.c1/len, c2=self.c2/len, c3=self.c3/len
            )
        print({"msg": "division by zero"})
        sys.exit()
        
        
class VectorSpace:
    def __init__(self, initial_point: Point,
                 e1: Vector, e2: Vector, e3: Vector):
        self.initial_point = initial_point
        self.e1 = self.norm(e1)
        self.e2 = self.norm(e2)
        self.e3 = self.norm(e3)
        # self.e1 = e1
        # self.e2 = e2
        # self.e3 = e3
        
    def len(self, point2: Point):
        return Point.distance(self.initial_point, point2)
    
    def norm(self, vec: Vector):
        len = self.len(vec.as_point())
        if len != 0:
            return Vector(
                c1=vec.c1/len, c2=vec.c2/len, c3=vec.c3/len
            )
        print({"msg": "division by zero"})
        sys.exit()
        

class Camera:
    def __init__(self, position: Point, look_dir: Vector, 
                 look_at: Point, fov: float, k: float,
                 draw_distance: float):
        self.position = position
        self.look_dir = look_dir
        self.look_at = look_at
        self.fov = fov
        self.vfov = 2/3*fov*k
        # k - коэфициент сжатия
        self.draw_distance = draw_distance
        
    def send_rays(self, amount_rays: int):
        pass
    
    
class Object:
    def __init__(self, position: Point, rotation: Vector,
                 obj_points: list):
        self.position = position
        self.rotation = position
        self.obj_points = obj_points
        
    def contains(self, point: Point):
        return point in self.obj_points
    
    
