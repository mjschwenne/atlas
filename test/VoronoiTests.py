import unittest
from src.Backend.Voronoi import Voronoi
from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt


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

        bounding_box = Polygon([Point(-50, 50), Point(50, 50), Point(50, -50), Point(-50, -50)])
        vor = Voronoi(10, bounding_box)
        vor.generate_polygons()

        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'k-')
        # for p in vor.polygons:
        print("Edges =", len(vor.graph.edges))
        print("Polygons =", len(vor.polygons))
        print(vor.voronoi.vertices)
        print(vor.voronoi.regions)
        # vert_list = p.get_vertices()
        # x_list = []
        # y_list = []
        # for v in vert_list:
        #     x_list.append(v.get_x())
        #     y_list.append(v.get_y())
        # plt.fill(x_list, y_list)
        # plt.xlim([-60, 60])
        # plt.ylim([-60, 60])
        plt.show()


if __name__ == '__main__':
    unittest.main()
