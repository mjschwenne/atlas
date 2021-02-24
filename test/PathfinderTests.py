import unittest
from src.Backend.Pathfinder import Pathfinder
from src.Backend.Voronoi import Voronoi
import matplotlib.pyplot as plt


class PathfinderTests(unittest.TestCase):
    def test_pathfinder_basic(self):
        vor = Voronoi(50, 150)
        p = Pathfinder(vor.graph, [])
        nodes = list(vor.graph.nodes)
        origin = nodes[0]
        target = nodes[9]
        path = list(p.find_path(origin, target))
        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'k-')
        p_x_list = []
        p_y_list = []
        for p in path:
            p_x_list.append(p.get_x())
            p_y_list.append(p.get_y())
        plt.plot(p_x_list, p_y_list, 'b-')
        plt.xlim([-vor.bounds, vor.bounds])
        plt.ylim([-vor.bounds, vor.bounds])
        plt.show()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
