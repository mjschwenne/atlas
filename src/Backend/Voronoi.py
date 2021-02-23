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
                # Used to determine which end of the ray is bounded and where the ray intersects the bounding box
                mid_x = (self.voronoi.points[e[0]][0] + self.voronoi.points[e[1]][0]) / 2
                mid_y = (self.voronoi.points[e[1]][1] + self.voronoi.points[e[1]][1]) / 2
                midpoint = Point(mid_x, mid_y)
                # Calculate the slope of the ray. Set to infinity if delta x is 0
                delta_x = known_end.get_x() - midpoint.get_x()
                delta_y = known_end.get_y() - midpoint.get_y()
                ray_slope = delta_y / delta_x if delta_x != 0 else math.inf
                # Compare the x coordinates.
                # If it is equal, the ray is vertical
                # If the known endpoint has the smaller x coordinate, the ray extends right
                # If it has a smaller x coordinate, the ray extends left
                if ray_slope == math.inf:
                    # The ray could intersect the top or the bottom, depending on if the midpoint is above or below the
                    # known endpoint
                    if known_end.get_y() > midpoint.get_y():
                        # Intersects the bottom bound
                        other_end = Point(known_end.get_x(), self.bounds["bottom"])
                        self.graph.add_node(other_end)
                        self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))
                    else:
                        # Intersects the upper bound
                        other_end = Point(known_end.get_x(), self.bounds["top"])
                        self.graph.add_node(other_end)
                        self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))
                # The ray extends to the right
                elif known_end.get_x() < midpoint.get_x():
                    # The ray could intersect the top, bottom or right side of the bounding box
                    # We will start by seeing where it intersects the right side of the box
                    y = ray_slope * (self.bounds["right"] - known_end.get_x()) + known_end.get_y()
                    # We need to change the end point if it intersects above the top or below the bottom
                    if y > self.bounds["top"]:
                        # Set the y coordinate to be the upper bound and compute the new x
                        x = (self.bounds["top"] - known_end.get_y() + ray_slope * known_end.get_x()) / ray_slope
                        # Insert the new endpoint and edge
                        other_end = Point(x, self.bounds["top"])
                        self.graph.add_node(other_end)
                        self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))
                    elif y < self.bounds["bottom"]:
                        # Set the y coordinate to the bottom and compute the new x
                        x = (self.bounds["bottom"] - known_end.get_y() + ray_slope * known_end.get_x()) / ray_slope
                        # Insert the new endpoint and edge
                        other_end = Point(x, self.bounds["bottom"])
                        self.graph.add_node(other_end)
                        self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))
                    else:
                        # The ray intersects on the right edge, so we insert the new endpoint and edge
                        other_end = Point(self.bounds["right"], y)
                        self.graph.add_node(other_end)
                        self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))
                # The ray extends to the left
                elif known_end.get_x() > midpoint.get_x():
                    # The ray could intersect the top, bottom or left side of the bounding box
                    # We will start by seeing where it intersects the left side of the box
                    y = ray_slope * (self.bounds["left"] - known_end.get_x()) + known_end.get_y()
                    # We need to change the end point if it intersects above the top or below the bottom
                    if y > self.bounds["top"]:
                        # Set the y coordinate to be the upper bound and compute the new x
                        x = (self.bounds["top"] - known_end.get_y() + ray_slope * known_end.get_x()) / ray_slope
                        # Insert the new endpoint and edge
                        other_end = Point(x, self.bounds["top"])
                        self.graph.add_node(other_end)
                        self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))
                    elif y < self.bounds["bottom"]:
                        # Set the y coordinate to be bottom and compute the new x
                        x = (self.bounds["bottom"] - known_end.get_y() + ray_slope * known_end.get_x()) / ray_slope
                        # Insert the new endpoint and edge
                        other_end = Point(x, self.bounds["bottom"])
                        self.graph.add_node(other_end)
                        self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))
                    else:
                        # The ray intersects on the left edge, so we insert the new endpoint and edge
                        other_end = Point(self.bounds["left"], y)
                        self.graph.add_node(other_end)
                        self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))

    def relax_polygons(self):
        pass
