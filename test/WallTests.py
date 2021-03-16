import unittest
import random
from src.Backend.Wall import Wall
from src.Backend.Point import Point
from src.Backend.Polygon import Polygon
from src.Backend.Voronoi import Voronoi
import matplotlib.pyplot as plt


class TestWall(unittest.TestCase):
    """
    Tests for Wall.py
    """
    def test_create_wall_voronoi_1(self):
        bounding_box = Polygon([Point(-500, 500), Point(500, 500), Point(500, -500), Point(-500, -500)])
        vor = Voronoi(50, bounding_box)
        for i in range(3):
            vor.relax()

        wall = Wall(vor.polygons, vor.graph, bounding_box)

        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'b-')

        x_list = []
        y_list = []
        for p in wall.vertices:
            x_list.append(p.get_x())
            y_list.append(p.get_y())
        x_list.append(wall.vertices[0].get_x())
        y_list.append(wall.vertices[0].get_y())
        plt.plot(x_list, y_list, 'k-')

        x_list = []
        y_list = []
        for r in wall.roads:
            for p in r:
                x_list.append(p.get_x())
                y_list.append(p.get_y())
            plt.plot(x_list, y_list, 'r-')
            x_list = []
            y_list = []

        for p in wall.vertices:
            plt.plot([p.get_x()], [p.get_y()], 'yo')
        for p in wall.gates:
            plt.plot([p.get_x()], [p.get_y()], 'ro')
        plt.show()

        self.assertEqual(True, wall.is_convex())

    def test_create_wall_voronoi_2(self):
        bounding_box = Polygon([Point(-100, 100), Point(100, 100), Point(100, -100), Point(-100, -100)])
        vor = Voronoi(25, bounding_box)
        for i in range(3):
            vor.relax()

        wall = Wall(vor.polygons, vor.graph, bounding_box)

        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'b-')

        x_list = []
        y_list = []
        for p in wall.vertices:
            x_list.append(p.get_x())
            y_list.append(p.get_y())
        x_list.append(wall.vertices[0].get_x())
        y_list.append(wall.vertices[0].get_y())
        plt.plot(x_list, y_list, 'k-')

        x_list = []
        y_list = []
        for r in wall.roads:
            for p in r:
                x_list.append(p.get_x())
                y_list.append(p.get_y())
            plt.plot(x_list, y_list, 'r-')
            x_list = []
            y_list = []

        for p in wall.vertices:
            plt.plot([p.get_x()], [p.get_y()], 'yo')
        for p in wall.gates:
            plt.plot([p.get_x()], [p.get_y()], 'ro')
        plt.show()

        self.assertEqual(True, wall.is_convex())


if __name__ == '__main__':
    unittest.main()
