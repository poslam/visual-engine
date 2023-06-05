from src.game import MyGame
from lib.engine.engine import Entity, EntityList
from lib.engine.game import Game
from lib.math.cs import CoordinateSystem
from lib.math.matrix_vector import Vector
from lib.math.point import Point
from lib.math.vs import VectorSpace
import src.globals as globals

vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
p1 = Point([0, 0, 0])
cs = CoordinateSystem(p1, vs)

globals.cs = cs

g = Game(cs, EntityList(Entity))

class TestIntersection:
    def test_intersection(self):

        camera = g.camera(Point([0, 0, 0]), draw_distance=100, fov=100,
                                                direction=Vector([1, 1, 1]))

        a = camera.get_rays_matrix(10, 10)

        myg = MyGame(cs, EntityList(Entity))

        obj = myg.get_hyperellipsoid()(position=Point([-10, 10, 10]), 
                                    direction=Vector([2, 1, 89]), 
                                    semiaxes=[0.1, 0.2, 0.5])

        act = True
        for i in a:
            for j in i:
                if obj.intersection_distance(j) > 0:        
                    assert False
                    
        assert act
