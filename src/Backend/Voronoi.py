import random
import time
import math

from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
import networkx as nx
import numpy as np
from scipy.spatial import Voronoi as Vor


class Voronoi:
    """
    Generates and stores a Voronoi diagram.
    """

    def __init__(self, num_district, bounds):
        self.seeds = []
        self.polygons = []
        self.graph = nx.Graph()
        self.voronoi = None
        self.num_district = num_district
        self.bounds = bounds

        self.generate_seeds()
        self.generate()

    def generate_seeds(self):
        """
        Generate random Points which are used as seeds in the construction of a voronoi diagram.
        """
        random.seed(time.gmtime(0).tm_sec)
        delta_angle = random.random() * 2 * math.pi

        for p in range(self.num_district):
            a = delta_angle + math.sqrt(p) * 5
            r = 0 if p == 0 else 10 + p * (2 + random.random())
            self.seeds.append(Point(math.cos(a) * r, math.sin(a) * r))

    def generate(self):
        """
        Uses scipy and QHull to generate a voronoi diagram based off the the seeds from generate_seeds
        """
        self.voronoi = Vor(Point.to_list(self.seeds))
        print(self.voronoi.points)
        print(self.voronoi.vertices)
        print(self.voronoi.ridge_dict)
        for v in range(len(self.voronoi.vertices)):
            self.graph.add_node(Point.to_point(self.voronoi.vertices[v].tolist()))

        for e in self.voronoi.ridge_dict:
            # Find the endpoints of this edge, if they exist, by finding the Points at the endpoints or setting a
            # point to infinity equal to None
            vertex_pair = (self.voronoi.ridge_dict[e][0], self.voronoi.ridge_dict[e][1])
            v1 = Point.to_point(self.voronoi.vertices[vertex_pair[0]].tolist()) if vertex_pair[0] != -1 else None
            v2 = Point.to_point(self.voronoi.vertices[vertex_pair[1]].tolist()) if vertex_pair[1] != -1 else None
            if v1 is not None and v2 is not None:
                self.graph.add_edge(v1, v2, weight=v1.simple_distance(v2))
            else:
                # Find which endpoint goes to infinity
                known_end = None
                if v1 is None:
                    known_end = v2
                else:
                    known_end = v1
                # Find the midpoint between the seed points
                mid_x = (self.voronoi.points[e[0]][0] + self.voronoi.points[e[1]][0]) / 2
                mid_y = (self.voronoi.points[e[1]][1] + self.voronoi.points[e[1]][1]) / 2
                midpoint = Point(mid_x, mid_y)
                del mid_x, mid_y
                # Find the tangent vector between the seed points. Use a Point to represent the end of the vector
                tan_x = self.voronoi.points[e[1]][0] - self.voronoi.points[e[0]][0]
                tan_y = self.voronoi.points[e[1]][1] - self.voronoi.points[e[0]][1]
                tangent = Point(tan_x, tan_y)
                del tan_x, tan_y
                # Normalize the tangent vector, first finding the norm (magnitude)
                norm = tangent.simple_distance(Point(0, 0))
                tangent.set(tangent.get_x() / norm, tangent.get_y() / norm)
                # Find the normal vector
                normal = Point(-tangent.get_y(), tangent.get_x())
                # The direction of the Voronoi ray is ALWAYS away from the origin, so we need to know if the normal
                # vector is pointing inwards to the origin or outward to infinity. The midpoint vector will always point
                # away from the origin. The dot product a . b = ||a||*||b||*cos(θ), and while we do not care about
                # the magnitude of the dot product, if abs(θ) is more than 90 degrees between the normal vector and
                # the midpoint, than the dot product is negative and the normal vector is pointing in the wrong
                # direction. Thus, we need to multiply the normal vector by the sign of the dot product between itself
                # and the midpoint vector.
                dot_product = midpoint.get_x() * normal.get_x() + midpoint.get_y() * normal.get_y()
                # How the hell does Python not have a sign function? I will use numpy then
                voronoi_direction = Point(np.sign(dot_product) * normal.get_x(), np.sign(dot_product) * normal.get_y())
                # Now we can find the endpoint and add it to the graph.
                other_end = Point(known_end.get_x() + self.bounds * voronoi_direction.get_x(),
                                  known_end.get_y() + self.bounds * voronoi_direction.get_y())
                self.graph.add_node(other_end)
                self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))

    def relax_polygons(self):
        pass
