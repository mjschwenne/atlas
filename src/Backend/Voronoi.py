import random
import math
from collections import deque
from itertools import cycle

from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
import networkx as nx
import numpy as np
from scipy.spatial import Voronoi as Vor


def print_list(list_name, points):
    print(f"{list_name} = [", end=" ")
    for i in points:
        print(f"{i},", end=" ")
    print("]")


def print_dict(dict_name, points):
    print(f"{dict_name} = [", end=" ")
    for i in points.keys():
        print(f"{i} : {points[i]}", end=" ")
    print("]")


def remove_vertices(G, vertices):
    """
    Remove all vertices in `vertices` from the graph `G`

    Parameters
    ----------
    G : nx.Graph
        The graph from which vertices will be removed
    vertices : list
        The list of vertices in G to be removed

    Returns
    -------
    nx.Graph
        A copy of the graph `G` without the vertices listed in `vertices`
    """
    h = G.copy()
    h.remove_nodes_from(vertices)
    return h


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


class Voronoi:
    """
    Generates and stores a Voronoi diagram as a graph and list of polygons

    Attributes
    ----------
    seeds : List
        List of points which are the seeds for the voronoi diagram
    polygons : List
        List of polygons where each polygon is one voronoi cell
    graph : nx.Graph
        The graph representation of the voronoi ridges
    num_district : int
        The number of districts in the map, or the number of seed points
    bounds : Polygon
        The bounding polygon
    """

    def __init__(self, num_district, bounds):
        self.num_district = num_district
        self.bounds = bounds

        self.__run()

    def __run(self, new_seeds=None):
        """
        Flush the existing data, then construct the Voronoi diagram, graph and polygons
        """
        self.seeds = []
        self.polygons = set()
        self.graph = nx.Graph()

        if new_seeds is None:
            self.generate_seeds()
        else:
            self.seeds = new_seeds
        self.voronoi = Vor(Point.to_list(self.seeds))
        self.generate_graph()
        self.generate_polygons()

    def generate_seeds(self):
        """
        Generate random Points which are used as seeds in the construction of a voronoi diagram.

        The notes are more concentrated in the middle of the map.
        """
        random.seed()
        delta_angle = random.random() * 2 * math.pi

        for p in range(self.num_district):
            a = delta_angle + math.sqrt(p) * 5
            r = 0 if p == 0 else 10 + p * (2 + random.random())
            self.seeds.append(Point(math.cos(a) * r, math.sin(a) * r))

    def generate_graph(self):
        """
        Uses scipy and QHull to generate a voronoi diagram based off the the seeds from generate_seeds, then build
        a NetworkX graph and list of polygons to match.

        Notes
        -----
        For vertices with two defined endpoint, creating the graph is not hard. However, for vertices with an infinite
        end the process is more complex.

        From the definition of a voronoi ridge, it is the perpendicular bisector of the line segment between two voronoi
        points, and thus a tangent line. Model the tangent as a vector, using a Point object to store the end of the
        vector, assuming the other end is at the origin. Normalize it into a unit vector and find the normal vector,
        which has an x coordinate equal to the negative y of the tangent and a y coordinate equal to the x coordinate of
        the tangent.

        Now we have a vector which is perpendicular to the segment between the voronoi points, but because this is a
        ray, we need to account for which direction the infinite end extents. It can NEVER go towards the origin as that
        it where the center of the diagram is and the most other points. So we find the midpoint between the two
        voronoi points of interest, also modelling it as a vector like the tangent. Because the midpoint actually starts
        at the origin, unlike the tangent which originates from one of the voronoi points, the midpoint vector will
        always point away from the origin.

        The dot product of two vectors is :math:`a \\cdot b = ||a|| \\times ||b|| \\times \\cos(\\theta)` where
        :math:`\\theta` is the angle between the two vectors. We do not care about the product of the magnitudes, but we
        can use the cosine to our advantage. The cosine is positive if :math:`\\theta` is within
        :math:`\\pm\ \\frac{\\pi}{2}` radians. We need the direction of this ray to be no more than
        :math:`\\frac{\\pi}{2}` radians from the midpoint vector or else it is closer to pointing at the origin and
        thus pointing in the wrong direction. If the dot product between the normal vector and the midpoint vector is
        negative, be multiply the normal vector by negative 1 to invert the direction it points.

        Finally we take a large value that is outside the display range of the map, scale the voronoi directional
        vector by that amount and then add it to the position of the known end of the ray.
        """
        # Assume that the voronoi diagram has already been generated by QHull and SciPy
        # Start to add voronoi vertices to the graph
        for v in self.voronoi.vertices:
            if self.bounds.is_contained(Point.to_point(v.tolist())):
                self.graph.add_node(Point.to_point(v.tolist()))
        # Add edges to the graph
        for e in self.voronoi.ridge_dict:
            # Find the endpoints of this edge, if they exist, by finding the Points at the endpoints or setting a
            # point to infinity equal to None
            vertex_pair = (self.voronoi.ridge_dict[e][0], self.voronoi.ridge_dict[e][1])

            v1 = None
            v2 = None
            if vertex_pair[0] != -1:
                v1 = Point.to_point(self.voronoi.vertices[vertex_pair[0]].tolist())
                if not self.bounds.is_contained(v1):
                    v1 = None
            if vertex_pair[1] != -1:
                v2 = Point.to_point(self.voronoi.vertices[vertex_pair[1]].tolist())
                if not self.bounds.is_contained(v2):
                    v2 = None

            if v1 is not None and v2 is not None:
                self.graph.add_edge(v1, v2, weight=v1.simple_distance(v2))
            else:
                # Find which endpoint goes to infinity
                if v1 is None and v2 is not None:
                    known_end = v2
                elif v2 is None and v1 is not None:
                    known_end = v1
                else:
                    continue
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
                t = self.__find_bounds(known_end, voronoi_direction)
                if t is not None:
                    other_end = Point(known_end.get_x() + t * voronoi_direction.get_x(),
                                      known_end.get_y() + t * voronoi_direction.get_y())
                    self.graph.add_node(other_end)
                    self.graph.add_edge(known_end, other_end, weight=known_end.simple_distance(other_end))
        # Add the perimeter to the graph
        bound_points = self.bounds.vertices
        len_bound_points = len(bound_points)
        for v in bound_points:
            self.graph.add_node(v)
        # Find the link the perimeter vertices
        for v in range(len_bound_points):
            bound_start = bound_points[v]
            bound_end = bound_points[(v + 1) % len_bound_points]
            edge_vertices = []
            for vert in self.graph:
                if Polygon.in_segment(bound_start, bound_end, vert):
                    edge_vertices.append(vert)
            # Thanks to python magic methods, these are sorted from min y to max y and from min to max x if y is equal
            edge_vertices.sort()
            # Add the edges
            for vert in range(len(edge_vertices) - 1):
                start = edge_vertices[vert]
                end = edge_vertices[vert + 1]
                # print(f"Adding perimeter edge between {start} and {end}")
                self.graph.add_edge(start, end, weight=start.simple_distance(end))

    def generate_polygons(self):
        """
        Take the graph of the Voronoi diagram and generate the polygon tesselation of the plane.

        Stores the polygons in a class attribute list
        """
        # print(self.voronoi.vertices)
        for r in self.voronoi.regions:
            # If the region is not complete according to QHull and SciPy
            border = False
            if -1 in r:
                border = True
            else:
                for v in r:
                    point = self.voronoi.vertices[v]
                    if not self.bounds.is_contained(Point(point[0], point[1])):
                        border = True
                        del point
                        break
                    del point

            if not border and len(r) > 0:
                vertices = []
                for p in r:
                    point = self.voronoi.vertices[p]
                    vertices.append(Point(point[0], point[1]))
                self.polygons.add(Polygon(vertices, reorder=True))
            elif len(r) > 0:
                # Use a deque object to build a path along the inside of the graph. From here, connect to the
                # boundary vertices adjacent to the endpoints. The path will always have a length of r - 1 as we
                # either have a -1 in the vertex list somewhere or there is one vertex outside the bounding box.
                # Assuming a reasonable bounding polygon which is large enough to encapsulate all of the seed points
                # is not possible to have multiple vertices because they MUST converge to create an enclosed polygon.
                path = deque()
                vertex_origin = r.copy()
                vertices = cycle(vertex_origin)
                path_length = len(r)
                while len(path) < path_length:
                    v = next(vertices)
                    # Remove a -1 vertex, or a ray to infinity
                    if v == -1:
                        path_length -= 1
                        vertex_origin.remove(v)
                        vertices = cycle(vertex_origin)
                        continue
                    point = self.voronoi.vertices[v]
                    vertex = Point(point[0], point[1])
                    # Remove one from the path length for a vertex outside of the bounding polygon
                    # Also remove the vertex from the cycle list
                    if not self.bounds.is_contained(vertex):
                        path_length -= 1
                        vertex_origin.remove(v)
                        vertices = cycle(vertex_origin)
                        continue
                    # Case 1: empty path
                    if len(path) == 0:
                        path.append(vertex)
                        continue
                    # Case 2: non-empty path, and vertex is adjacent to the first endpoint
                    if vertex in self.graph[path[0]] and vertex not in path:
                        path.appendleft(vertex)
                        continue
                    # Case 3: non-empty path and vertex is adjacent to the second endpoint
                    if vertex in self.graph[path[-1]] and vertex not in path:
                        path.append(vertex)
                    # Case 4: non-empty path and vertex is not adjacent to either endpoint
                    # Move to the next iteration of the while loop, which will be done passively
                del vertices
                # Add the vertices on the graph boundary to the path, starting with the front end
                bound_points = self.bounds.vertices
                len_bound_points = len(bound_points)
                # Skip if the region is completely outside of the bounding polygon
                if len(path) == 0:
                    continue
                for v in self.graph[path[0]]:
                    for bound in range(len_bound_points):
                        bound_start = bound_points[bound]
                        bound_end = bound_points[(bound + 1) % len_bound_points]
                        # print(f"Is {v} on the segment between {bound_start} and {bound_end}? {Polygon.in_segment(bound_start, bound_end, v)}")
                        if Polygon.in_segment(bound_start, bound_end, v):
                            path.appendleft(v)
                            break
                    # I think that this will break the outer loop. If the inner loop finishes, it will call the else and
                    # that will keep the outer loop going. If it is broken, it will skip the else and then break the
                    # outer loop...?
                    else:
                        continue
                    break
                # print_list("adj", list(self.graph[path[0]].keys()))
                # print_list("path", path)
                # Find the boundary vertex for the back end of the path
                for v in self.graph[path[-1]]:
                    for bound in range(len_bound_points):
                        bound_start = bound_points[bound]
                        bound_end = bound_points[(bound + 1) % len_bound_points]
                        if Polygon.in_segment(bound_start, bound_end, v) and v not in path:
                            path.append(v)
                            break
                    else:
                        continue
                    break
                # print_list("path", path)
                # Next, find all of the internal vertices in the graph and remove them to have just the perimeter ones
                internal_vertices = list(self.graph.adj.keys())
                for v in range(len_bound_points):
                    bound_start = bound_points[v]
                    bound_end = bound_points[(v + 1) % len_bound_points]
                    for vert in self.graph:
                        if Polygon.in_segment(bound_start, bound_end, vert) and vert in internal_vertices:
                            internal_vertices.remove(vert)
                perimeter_graph = remove_vertices(self.graph, internal_vertices)
                # BFS from the end points of the path, then add it to the path
                # Start at route[1] because route[0] is already in path
                route = bfs_path(perimeter_graph, path[0], path[-1])
                for v in range(1, len(route)):
                    path.appendleft(route[v])
                # path is now the vertex list of the polygon
                polygon = Polygon(path, reorder=True)
                self.polygons.add(polygon)

    def relax(self):
        """
        Finds the centroid of each polygons and sets that to be the seed point of the next generation of voronoi diagram
        """
        centroids = []
        for p in self.polygons:
            centroids.append(p.get_center())
        self.__run(centroids)

    # PRIVATE HELPER METHODS
    def __find_bounds(self, known_end, voronoi_direction):
        """
        Finds a scalar t such that voronoi_direction times t plus known_end in on the bounding box

        Parameters
        ----------
        known_end : Point
            The fixed end of the voronoi ray
        voronoi_direction : Point
            Unit vector representing the direction of the voronoi ray

        Returns
        -------
        float :
            The scalar for the voronoi direction vector so that the ray ends at the bounding box
        """
        # Possible bug IF the ray coincides with the bounding box
        # Build the parametrized matrix equation for the ray
        ray_start = np.array([[known_end.get_x()], [known_end.get_y()]])
        ray_slope = np.array([[voronoi_direction.get_x()], [voronoi_direction.get_y()]])
        # Test against the bounding points
        bound_points = self.bounds.vertices
        len_bound_points = len(bound_points)
        for v in range(len_bound_points):
            bound_start = np.array([[bound_points[v].get_x()], [bound_points[v].get_y()]])
            bound_end = np.array([[bound_points[(v + 1) % len_bound_points].get_x()],
                                  [bound_points[(v + 1) % len_bound_points].get_y()]])
            a = np.concatenate((ray_slope, np.array([[-1]]) * (bound_end - bound_start)), axis=1)
            b = bound_start - ray_start
            try:
                parameters_intersect = np.linalg.solve(a, b)
            except np.linalg.LinAlgError:
                continue
            if parameters_intersect[0][0] >= 0 and 0 <= parameters_intersect[1][0] <= 1:
                return parameters_intersect[0][0]
