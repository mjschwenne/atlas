import unittest
from src.Backend.Voronoi import Voronoi
from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    def test_voronoi_graph_creation(self):
        """
        Display the voronoi diagram with the built-in visualization presets and the graph we will use later
        """
        bounding_box = Polygon([Point(-200, 200), Point(200, 200), Point(200, -200), Point(-200, -200)])
        vor = Voronoi(50, bounding_box)

        voronoi_plot_2d(vor.voronoi, show_vertices=False, show_points=False)
        plt.xlim([-250, 250])
        plt.ylim([-250, 250])
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
        plt.xlim([-250, 250])
        plt.ylim([-250, 250])
        plt.show()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
