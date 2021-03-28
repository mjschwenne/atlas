from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
from src.Backend.Pathfinder import Pathfinder
from scipy.spatial import ConvexHull
import networkx as nx
import numpy as np
from collections import deque


def print_list(list_name, points):
    print(f"{list_name} = [", end=" ")
    for i in points:
        print(f"{i},", end=" ")
    print("]")


def bfs_path(G, source, destination):
    """
    Use a breadth first search to find the path from vertex `source` to vertex `destination`.

    Parameters
    ----------
    G : nx.Graph
        The graph to search
    source : Point
        Origin point
    destination : Point
        Destination point

    Returns
    -------
    deque
        A queue with the path from `source` to `destination` already enqueued.
    """
    vertex_dict = dict(nx.bfs_predecessors(G, source))
    queue = deque()
    queue.append(destination)
    # print(f"Finding path from {source} to {destination} using {print_dict('vertex_dict', vertex_dict)}")
    while queue[-1] != source:
        # print(f"Head of queue is {queue[-1]}")
        queue.append(vertex_dict[queue[-1]])
    queue.reverse()
    return queue


def move_vertex(region, vertex, new_vertex, graph):
    """
    Move the vertex in the region, and update that same vertex in the neighbours of the region

    Parameters
    ----------
    region : Region
        The region whose vertex is being updated
    vertex : Point
        Vertex of the region to be changed, which will also be updated in the neighbouring regions
    new_vertex : Point
        The new location of the vertex
    graph : nx.Graph
        Underlying graph of the region boundaries, which needs to be update for the Pathfinder class

    Returns
    -------
    nx.Graph
        The new graph with the moved vertex
    """
    # Skip useless moves
    if vertex == new_vertex:
        return
    # Update the original region
    new_vertex_list = [new_vertex if v == vertex else v for v in region.vertices]
    print(f"Updating {vertex} to {new_vertex}")
    print_list("old vertices", region.vertices)
    region.set_vertices(new_vertex_list)
    print_list("new vertices", region.vertices)
    # Check the neighbours
    for r in region.get_neighbors():
        new_vertex_list = [new_vertex if v == vertex else v for v in r.vertices]
        r.set_vertices(new_vertex_list)
    # Update the point position in the graph
    vert_map = {vertex: new_vertex}
    return nx.relabel_nodes(graph, vert_map)


def project_vector(u, v):
    """
    Project vector `u` onto vector `v`

    Convert the Points into np.array and then use

    .. math:: \text\{proj\}_{\\vec{v}}(\\vec{u}) = \\frac{\\vec{u} \\cdot \\vec{v}}{||\\vec{v}||^2} \\times \\vec{v}

    Parameters
    ----------
    u : Point
        Vector
    v : Point
        Vector

    Returns
    -------
    Point
        The result of projecting u onto v
    """
    u_np = np.array([u.get_x(), u.get_y()])
    v_np = np.array([v.get_x(), v.get_y()])
    proj = (np.dot(u_np, v_np) / np.dot(v_np, v_np)) * v_np
    return Point(proj[0], proj[1])


class Infrastructure(Polygon):
    """
    This class represents the Infrastructure using a Polygon, Pathfinder, and a Graph

    Attributes
    ----------
    gates : List of Points
        The location of the gates along the city wall
    roads : List of Lists of Points
        Each list represents the points along a path which represents the main roads of the city
    """

    def __init__(self, regions, graph, bounding_box):
        """
        Constructs the Infrastructure of the city given a list of Regions, the underlying graph, and a bounding_box.

        Parameters
        ----------
        regions : list of Region
            A list of Regions of the city
        graph : nx.Graph
            Networkx Graph of Region
        bounding_box : Polygon
            The max polygon of the city (the bounding box of the city)
        """
        self.regions = regions
        in_city_list = []

        for p in self.regions:
            furthest_dist_from_center = p.furthest_point(Point(0.0, 0.0)).simple_distance(Point(0.0, 0.0))
            if furthest_dist_from_center < bounding_box.get_perimeter() * 0.1:
                in_city_list.append(p)

        # Finds the total vertices from all the regions
        total_vertices = Polygon.to_points(in_city_list)

        # Creates the wall and finds its vertices
        list_points = Point.to_list(total_vertices)
        hull = ConvexHull(list_points)
        ver = []
        for p in hull.vertices:
            ver.append(hull.points[p])
        vertices = Polygon.to_polygon(ver).get_vertices()

        # Makes this wall a Polygon
        super().__init__(vertices)

        # Clip the graph so that it is only vertices on or inside of the wall.
        clipped_graph = graph.copy()
        outer_graph = graph.copy()
        for v in graph:
            if not self.is_contained(v):
                clipped_graph.remove_node(v)
            else:
                outer_graph.remove_node(v)
        # For each edge, adjust the polygons if needed
        for v in range(len(self.vertices)):
            start = vertices[v]
            end = vertices[(v + 1) % len(self.vertices)]
            clipped_graph = self.__push_polygons(clipped_graph, start, end)
        # Merge the final clipped graph back into the regular graph
        graph = nx.compose(outer_graph, clipped_graph)

        # Finds the Roads and Gates
        center_poly = None
        for p in self.regions:
            if p.is_contained(Point(0.0, 0.0)):
                center_poly = p

        self.gates = []
        self.roads = []
        pathfinder = Pathfinder(graph, [])

        n = len(center_poly.vertices)

        k, m = divmod(len(self.vertices), n)
        sections_vertices = list(self.vertices[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

        for v in center_poly.vertices:
            min_point = sections_vertices[0][0]
            min_path = pathfinder.find_path(v, min_point)
            if min_path is None:
                continue
            min_dist = Pathfinder.path_distance(min_path)
            min_section = sections_vertices[0]
            for s in sections_vertices:
                for p in s:
                    new_path = pathfinder.find_path(v, p)
                    if new_path is None:
                        continue
                    new_dist = Pathfinder.path_distance(new_path)
                    if new_dist < min_dist:
                        min_section = s
                        min_point = p
                        min_path = new_path
                        min_dist = new_dist
            sections_vertices.remove(min_section)
            self.gates.append(min_point)
            self.roads.append(min_path)

        border_polys = []
        for p in regions:
            if bounding_box.is_bordering(p):
                border_polys.append(p)

        border_polys_points = Polygon.to_points(border_polys)
        border_points = []
        for i in range(0, len(bounding_box.vertices)):
            v1 = bounding_box.vertices[i]
            v2 = bounding_box.vertices[(i + 1) % len(bounding_box.vertices)]
            for p in border_polys_points:
                if Polygon.in_segment(v1, v2, p) and p not in bounding_box.vertices and p not in border_points:
                    border_points.append(p)

        city_points = Polygon.to_points(list(regions))
        in_city_points = []
        for p in city_points:
            if self.is_contained(p):
                in_city_points.append(p)
        for p in self.vertices:
            in_city_points.remove(p)

        for v in self.gates:
            pathfinder = Pathfinder(graph, in_city_points)
            min_point = border_points[0]
            min_path = pathfinder.find_path(v, min_point)
            if min_path is None:
                continue
            min_dist = Pathfinder.path_distance(min_path)
            for p in border_points:
                new_path = pathfinder.find_path(v, p)
                if new_path is None:
                    continue
                new_dist = Pathfinder.path_distance(new_path)
                if new_dist < min_dist:
                    min_path = new_path
                    min_dist = new_dist
            self.roads.append(min_path)

    def get_gates(self):
        """
        Returns the List of Points that defines the Gates

        Returns
        -------
        List of Points
            The List of Points that defines the Gates of the Wall
        """
        return self.gates

    def get_roads(self):
        """
        Returns the List of Lists of Points that defines the main roads in the city

        Returns
        -------
        List of List of Points
            The List of Lists of Points that defines the main roads in the city
        """
        return self.roads

    # PRIVATE HELPER METHODS
    def __push_polygons(self, graph, u, v):
        """
        Edit the graph and polygons so that bisected polygons align with the edge of the city wall

        Used a clipped version of the Voronoi graph, use a BFS to find the shortest path from the start of the wall
        edge to the end of the wall edge. From here, find the midpoint of each edge and determine which side of the if
        pointing away from the center using the sign of the dot product to determine if the angle between them is more
        or less than 180 degree.

        Parameters
        ----------
        graph : nx.Graph
            The Voronoi graph of the city, clipped so that it only contains the vertices on or inside of the wall
        u : Point
            The starting point of the wall edge
        v : Point
            The ending point of the wall edge

        Returns
        -------
        nx.Graph
            An update version of the graph such that it reflects the changed made to the polygons, to be used in
            Pathfinder
        """
        # Here we assume that the edge of the wall is not in the graph, otherwise there is no adjustment needed
        # Find the shortest path from start to end
        # Use this path to check which polygons are on the side of the path away from the origin
        print(f"__push_polygons({graph}, {u}, {v})")
        path = bfs_path(graph, u, v)
        if len(path) <= 2:
            return
        # Vector representing the edge of the wall
        wall_vector = Point(v.get_x() - u.get_x(), v.get_y() - u.get_y())
        # Find the midpoint of the edge
        push_polygons = set()
        edge_start = path.pop()
        while len(path) > 0:
            edge_end = path.pop()
            # The midpoint will be treated as the endpoint of a vector from the origin and used to determine which
            # normal vector is pointing away from the origin
            midpoint = Point((edge_start.get_x() + edge_end.get_x()) / 2,
                             (edge_start.get_y() + edge_end.get_y()) / 2)
            # Create <edge_start, edge_end> as an edge vector, normalize it
            edge_vector = Point(edge_end.get_x() - edge_start.get_x(),
                                edge_end.get_y() - edge_start.get_y())
            norm = edge_vector.simple_distance(edge_start)
            edge_vector.set(edge_vector.get_x(), edge_vector.get_y())
            # Find the normalized normal vector in relation to edge_vector
            normal = Point(-edge_vector.get_y() / norm, edge_vector.get_x() / norm)
            del norm
            # Find the dot product between the midpoint vector and the normal vector
            dot_product = midpoint.get_x() * normal.get_x() + midpoint.get_y() * normal.get_y()
            if dot_product > 0:
                # This is the point going away from the origin, find the polygon containing this midpoint + normal
                point = Point(midpoint.get_x() + normal.get_x(), midpoint.get_y() + normal.get_y())
            elif dot_product < 0:
                # Flip the direction
                point = Point(midpoint.get_x() - normal.get_x(), midpoint.get_y() - normal.get_y())
            else:
                continue
            print(f"Testing edge from {edge_start} to {edge_end}, midpoint: {midpoint}, point: {point}")
            point_edge_vector = Point(edge_end.get_x() - u.get_x(), edge_end.get_y() - u.get_y())
            new_vertex = u + project_vector(point_edge_vector, wall_vector)
            for r in self.regions:
                if r.is_contained(point):
                    push_polygons.add(r)
                    graph = move_vertex(r, edge_end, new_vertex, graph)
                    break
            # The end of this edge is by definition the start of the next edge
            edge_start = new_vertex

            return graph
