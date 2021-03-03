import unittest
from src.Backend.Voronoi import Voronoi
from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as mplPoly
from matplotlib.collections import PatchCollection
import numpy as np


class TestVoronoi(unittest.TestCase):
    def test_voronoi_graph_creation(self):
        """
        Display the voronoi diagram with the built-in visualization presets and the graph we will use later
        """
        bounding_box = Polygon([Point(-50, 50), Point(50, 50), Point(50, -50), Point(-50, -50)])
        vor = Voronoi(10, bounding_box)

        voronoi_plot_2d(vor.voronoi, show_vertices=False, show_points=False)
        plt.xlim([-60, 60])
        plt.ylim([-60, 60])
        plt.show()
        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'k-')
        # plt.plot([-250, 250], [-200, -200], 'r--')
        # plt.plot([-250, 250], [200, 200], 'r--')
        # plt.plot([-200, -200], [-250, 250], 'r--')
        # plt.plot([200, 200], [-250, 250], 'r--')
        plt.xlim([-60, 60])
        plt.ylim([-60, 60])
        plt.show()
        self.assertEqual(True, True)

    def test_voronoi_generate_polygons(self):
        """
        Test the creation of polygons from the Voronoi graph, then visualize them
        """

        bounding_box = Polygon([Point(-200, 200), Point(200, 200), Point(200, -200), Point(-200, -200)])
        vor = Voronoi(50, bounding_box)
        vor.generate_polygons()
        polys = []
        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'k-')
        for p in vor.polygons:
            vert_list = p.get_vertices()
            x_list = []
            y_list = []
            for v in vert_list:
                x_list.append(v.get_x())
                y_list.append(v.get_y())
            plt.fill(x_list, y_list, "c")
            plt.xlim([-225, 225])
            plt.ylim([-225, 225])
        plt.show()


if __name__ == '__main__':
    unittest.main()
