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
        vor = Voronoi(50)
        voronoi_plot_2d(vor.voronoi)
        plt.show()
        nx.draw(vor.graph, vor.voronoi.vertices)
        plt.show()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
