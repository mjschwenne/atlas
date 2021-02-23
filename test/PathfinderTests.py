import unittest
from src.Backend.Pathfinder import Pathfinder
from src.Backend.Voronoi import Voronoi
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt
import networkx as nx


class PathfinderTests(unittest.TestCase):
    def test_pathfinder_basic(self):
        vor = Voronoi(50)
        p = Pathfinder(vor.graph)
        print("Graph:", vor.graph)
        # DOESNT WORK #


if __name__ == '__main__':
    unittest.main()
