import networkx as nx


class Pathfinder:
    def __init__(self, graph):
        """
        Makes a pathfinder from a graph

        Parameters
        ----------
        graph : graph
            The graph to find a path in
        """
        self.g = graph

    def find_path(self, origin, target):
        if nx.has_path(self.g, origin, target):
            return None

        path = nx.astar_path(self.g, origin, target)
        print(path)
