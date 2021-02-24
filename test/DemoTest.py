import unittest
from src.Backend.Pathfinder import Pathfinder
from src.Backend.Voronoi import Voronoi
from src.Backend.Wall import Wall
import matplotlib.pyplot as plt


class DemoTest(unittest.TestCase):
    def test_demo_small_city(self):
        vor = Voronoi(50, 150)
        self.assertEqual(True, True)
        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'k-')
        plt.xlim([-vor.bounds, vor.bounds])
        plt.ylim([-vor.bounds, vor.bounds])
        plt.show()


if __name__ == '__main__':
    unittest.main()
