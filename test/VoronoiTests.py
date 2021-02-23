import unittest
from src.Backend.Voronoi import Voronoi
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    def test_voronoi_graph_creation(self):
        """
        Display the voronoi diagram with the built-in visualization presets and the graph we will use later
        """
        vor = Voronoi(50, 150)
        voronoi_plot_2d(vor.voronoi)
        plt.xlim([-200, 200])
        plt.ylim([-200, 200])
        plt.show()
        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'k-')
        plt.xlim([-200, 200])
        plt.ylim([-200, 200])
        plt.show()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
