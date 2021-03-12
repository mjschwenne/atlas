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

        voronoi_plot_2d(vor.voronoi, show_vertices=True, show_points=True)
        plt.xlim([-60, 60])
        plt.ylim([-60, 60])
        plt.show()
        for v in vor.graph:
            for adj in vor.graph[v]:
                x_list = [v.get_x(), adj.get_x()]
                y_list = [v.get_y(), adj.get_y()]
                plt.plot(x_list, y_list, 'k-')
        plt.xlim([-60, 60])
        plt.ylim([-60, 60])
        plt.show()
        self.assertEqual(True, True)

    def test_voronoi_generate_polygons(self):
        """
        Test the creation of polygons from the Voronoi graph, then visualize them

        New method to generate polygons. Take self.voronoi.regions and if there are no -1's in the region, take pick the
        first vertex and move in a clockwise direction to another vertex listed in the region. repeat.

        If there is a -1, do mostly the same process as before except that we will generate the polyline 'in' the
        voronoi diagram. For the end vertices of the polyline, find the adjacent vertex to that point which is on the
        bounding polygon, then find the path between them only on the bounding polygon?? There are a few edge cases here

        Check work be ensuring that the voronoi point is inside the polygon which has been constructed!
        """

        bounding_box = Polygon([Point(-200, 200), Point(200, 200), Point(200, -200), Point(-200, -200)])
        vor = Voronoi(50, bounding_box)
        vor.generate_polygons()
        # for v in vor.graph:
        #     for adj in vor.graph[v]:
        #         x_list = [v.get_x(), adj.get_x()]
        #         y_list = [v.get_y(), adj.get_y()]
        #         fig.plot(x_list, y_list, 'k-')

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
            plt.fill(x_list, y_list)
            plt.xlim([-225, 225])
            plt.ylim([-225, 225])
        plt.show()


if __name__ == '__main__':
    unittest.main()
