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

class TestIntersection:
    def test_intersection(self):
        g = Game(cs, EntityList(Entity))

        camera = g.camera(Point([0, 0, 0]), draw_distance=100, fov=100,
                                                direction=Vector([200, 20, 1]))

        a = camera.get_rays_matrix(10, 10)

        myg = MyGame(cs)

        obj = myg.get_hyperellipsoid()(position=Point([1000, 200, 200]), 
                                    direction=Vector([2, 1, 89]), 
                                    semiaxes=[100, 200, 50])

        act = True
        for i in a:
            for j in i:
                if obj.intersection_distance(j) > 0:        
                    assert False
                    
        assert act
