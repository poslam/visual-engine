from classes import *
import globals
globals.Iitialize()
globals.VSpace = VectorSpace

def main():

    base = VectorSpace(
        initial_point=Point(0, 0, 0),
        e1=Vector(2, 3, 5),
        e2=Vector(0, 1, 0),
        e3=Vector(0, 0, 1)
    )

    globals.VSpace = base
        
    point1 = Point(1, 1, 1)
    point2 = Point(2, 2, 2)
    point3 = Point(23, 2, 2)

    vec1 = Vector(point1)
    vec2 = Vector(c1=3, c2=2, c3=2)
    vec3 = Vector(31, 32, 33)


    # distance
    print("distance:", Point.distance(point1, point3))

    # distance
    print("distance:", point1.distance(point3))

    # point + point
    point = point1+point2
    print("add of points:", point.as_list())

    # point * scalar
    point = point1*33
    print("point * scalar:", point.as_list())

    # point - point
    point = point1 - point2
    print("point - point: ", point.as_list())

    # point / scalar
    point = point1 / 3
    print("point / scalar: ", point.as_list())

    # length of vec
    vec = vec1.len()
    print("length of vec: ", vec)

    # vec + vec
    vec = vec1 + vec2
    print("vec + vec: ", vec.as_list())

    # vec * scalar
    vec = vec1 * 2
    print("vec * scalar: ", vec.as_list())

    # scalar * vec
    vec = 2 * vec1
    print("scalar * vec: ", vec.as_list())

    # vec * vec, скалярное произведение
    vec = vec1 * vec2
    print("vec * vec, скалярное произведение: ", vec)

    # vec ** vec, векторное произведение
    vec = vec1 ** vec2
    print("vec ** vec, векторное произведение: ", vec.as_list())


    vec3 = vec3.norm()
    print("нормирование вектора: ", vec3.as_list(), vec3.len())

    ptn = Point(1, 2, 3)
    print(ptn*2)

    
    print(vec1/2)
    
if __name__ == "__main__":
    main()