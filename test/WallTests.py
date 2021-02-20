import unittest
import random
import time
from src.Backend.Wall import Wall
from src.Backend.Point import Point
from src.Backend.Polygon import Polygon
import matplotlib.pyplot as plt


class TestRegion(unittest.TestCase):

    def test_create_wall_basic_one_polygon(self):
        p1 = Polygon([Point(1, 0), Point(2, 4), Point(6, 12), Point(10, 5), Point(1, 4), Point(3, 5), Point(8, 9),
                     Point(1, 1), Point(2, 12)])

        list_points = Polygon.to_points([p1])
        wall = Wall([p1])
        x_list = []
        y_list = []
        for p in wall.vertices:
            x_list.append(p.get_x())
            y_list.append(p.get_y())
        for p in list_points:
            plt.plot([p.get_x()], [p.get_y()], 'bo')
        x_list.append(wall.vertices[0].get_x())
        y_list.append(wall.vertices[0].get_y())
        plt.plot(x_list, y_list, 'k-')
        for p in wall.vertices:
            plt.plot([p.get_x()], [p.get_y()], 'yo')
        plt.show()
        self.assertEqual(True, wall.is_convex())

    def test_create_wall_basic_many_polygons(self):
        random.seed(time.gmtime(0).tm_sec)
        poly_list = []
        for i in range(0, int(random.uniform(1, 50))):
            point_list = []
            for j in range(0, int(random.uniform(1, 50))):
                point_list.append(Point(int(random.uniform(random.uniform(-100, 0), random.uniform(0, 100))),
                                        int(random.uniform(random.uniform(-100, 0), random.uniform(0, 100)))))
            poly_list.append(Polygon(point_list))
        list_points = Polygon.to_points(poly_list)
        wall = Wall(poly_list)
        x_list = []
        y_list = []
        for p in wall.vertices:
            x_list.append(p.get_x())
            y_list.append(p.get_y())
        for p in list_points:
            plt.plot([p.get_x()], [p.get_y()], 'bo')
        x_list.append(wall.vertices[0].get_x())
        y_list.append(wall.vertices[0].get_y())
        plt.plot(x_list, y_list, 'k-')
        for p in wall.vertices:
            plt.plot([p.get_x()], [p.get_y()], 'yo')
        plt.show()
        self.assertEqual(True, wall.is_convex())


if __name__ == '__main__':
    unittest.main()
