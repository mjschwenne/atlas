import random
import time
import math

from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
from scipy.spatial import ConvexHull


class Wall(Polygon):

    def __init__(self, regions):
        """
        Constructs a wall given a list of Regions

        Parameters
        ----------
        regions : List of Regions
            A list of Regions to make a wall around
        """
        # Finds the total vertices from all the regions
        total_vertices = Polygon.to_points(regions)

        # Creates the wall and finds its vertices
        list_points = Point.to_list(total_vertices)
        hull = ConvexHull(list_points)
        ver = []
        for p in hull.vertices:
            ver.append(hull.points[p])
        vertices = Polygon.to_polygon(ver).get_vertices()

        super().__init__(vertices)

        self.gates = []
        random.seed(time.gmtime(0).tm_sec)

        self.gates.append(vertices[int(random.uniform(0, len(vertices)))])

        tries = 0
        while tries < len(vertices):
            tries += 1
            r = int(random.uniform(0, len(vertices)))
            if vertices[r] in self.gates:
                continue
            min_dis = vertices[r].simple_distance(self.gates[0])
            for g in self.gates:
                cur_dis = vertices[r].simple_distance(g)
                if cur_dis < min_dis:
                    min_dis = cur_dis
            if min_dis < (self.get_perimeter() * 0.15):
                continue
            tries = 0
            self.gates.append(vertices[r])


    def get_gates(self):
        """
        Returns the List of Points that defines the Gates

        Returns
        -------
        List of Points
            The List of Points that defines the Gates of the Wall
        """
        return self.gates

    def set_gates(self, new_gates):
        """
        Sets the List of Points that defines the Gates of a Wall

        Parameters
        ----------
        new_gates : List of Points
            The new List of Points that defines the Gates of the Wall
        """
        self.gates = new_gates
