import networkx as nx
from src.Backend.Point import Point


class Pathfinder:
    def __init__(self, graph, invalid_points):
        """
        Makes a pathfinder from a graph

        Parameters
        ----------
        graph : graph
            The graph to find a path in
        """
        self.g = graph
        self.invalid_points = invalid_points

    @staticmethod
    def dist(a, b):
        """
        Heuristic method for the astar_path method in find_path method

        Parameters
        ----------
        a : Point
            First node
        b : Point
            Second node

        Returns
        -------
        float
            simple distance between a and b
        """
        return a.simple_distance(b)

    def find_path(self, origin, target):
        path = nx.astar_path(self.g, origin, target, heuristic=self.dist, weight="weight")
        for p in path:
            if p in self.invalid_points:
                return None
        return path
