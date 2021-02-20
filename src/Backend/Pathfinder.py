import networkx as nx


class Pathfinder:
    def __init__(self, points):
        g = nx.Graph()
        for p in points:
            g.add_node(p)

    def find_path(self, origin, point):
        pass
