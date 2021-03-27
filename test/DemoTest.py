import unittest
from src.Backend.Point import Point
from src.Backend.Polygon import Polygon
from src.Backend.Voronoi import Voronoi
from src.Backend.Infrastructure import Infrastructure
from src.Backend.Constructor import Constructor
import matplotlib.pyplot as plt


class DemoTest(unittest.TestCase):
    def test_demo_small_city(self):
        bounding_polygon = Polygon([Point(250, 250), Point(250, -250), Point(-250, -250), Point(-250, 250)])
        num_district = 50
        vor = Voronoi(num_district, bounding_polygon)
        vor.relax()
        vor.relax()

        wall = Infrastructure(vor.polygons, vor.graph, bounding_polygon)

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
