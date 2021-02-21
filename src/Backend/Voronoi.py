import random
import time
import math

from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
import networkx as nx
from scipy.spatial import Voronoi as Vor


class Voronoi:
    """
    Generates and stores a Voronoi diagram.
    """
    def __init__(self, num_district):
        self.seeds = []
        self.polygons = []
        self.graph = nx.Graph()
        self.voronoi = None
        self.num_district = num_district

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
            self.graph.add_node(v, pos=self.voronoi.vertices[v])

        for e in self.voronoi.ridge_dict:
            pair = (self.voronoi.ridge_dict[e][0], self.voronoi.ridge_dict[e][1])
            if pair[0] != -1 and pair[1] != -1:
                self.graph.add_edge(pair[0], pair[1])

    def relax_polygons(self):
        pass
