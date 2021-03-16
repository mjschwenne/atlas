import networkx
import networkx as nx
from src.Backend.Point import Point


class Pathfinder:
    """
    This class is used to find path between two points

    Attributes
    ----------
    g : graph (networkx)
        The graph from Voronoi.py
    invalid_points : List of Points
        Points that paths can't go through
    """

    def __init__(self, graph, invalid_points):
        """
        Makes a pathfinder from a graph

        Parameters
        ----------
        graph : graph
            The graph to find a path in
        """
        self.g = graph.copy()
        new_graph = self.g.copy()
        self.invalid_points = invalid_points
        for p in invalid_points:
            if p in self.g:
                new_graph.remove_edges_from(self.g.edges(p))
        self.g = new_graph

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

    @staticmethod
    def path_distance(path):
        dist = 0
        for i in range(0, len(path) - 2):
            p1 = path[i]
            p2 = path[i + 1]
            dist += p1.simple_distance(p2)
        return dist

    def find_path(self, origin, target):
        """
        Given an origin find the shortest path to target

        Parameters
        ----------
        origin : Point
            The first point in the path
        target : Point
            The last point in the path

        Returns
        -------
        List of Points
            The path from origin to target
        """
        not_found = True
        try:
            path = nx.astar_path(self.g, origin, target, heuristic=self.dist, weight="weight")
        except networkx.exception.NetworkXNoPath:
            return None
        while not_found:
            path = nx.astar_path(self.g, origin, target, heuristic=self.dist, weight="weight")
            for p in path:
                if p in self.invalid_points:
                    continue
            not_found = False
        return path
