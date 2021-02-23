import unittest
from src.Backend.Voronoi import Voronoi
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt
import networkx as nx


class MyTestCase(unittest.TestCase):
    def test_something(self):
        """
        Display the voronoi diagram with the built-in visualization presets and the graph we will use later
        """
        bounds = {"top": 150, "bottom": -150, "left": -150, "right": 150}
        vor = Voronoi(50, bounds)
        voronoi_plot_2d(vor.voronoi)
        plt.xlim([-200, 200])
        plt.ylim([-200, 200])
        plt.show()
        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list)
        plt.xlim([-200, 200])
        plt.ylim([-200, 200])
        plt.show()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
