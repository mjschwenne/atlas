import math
from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
import heapq


class Voronoi:
    """
    Generates and stores a Voronoi diagram.
    """
    def __init__(self):
        self.seeds = []
        self.polygons = []

    def generate_seeds(self):
        """
        Generate random Points which are used as seeds in the construction of a voronoi diagram.

        Returns
        -------
        List of Point
            A list of Points
        """
        pass

    def generate(self):
        """
        Uses Fortune's algorithm to construct a voronoi diagrams using the seeds from generate_seeds

        Returns
        -------
        List of Polygon
            A list of Polygons in the diagram
        """
        pass

    def relax_polygons(self):
        pass
