import random
import math
from queue import SimpleQueue

from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
import networkx as nx
import numpy as np
from scipy.spatial import Voronoi as Vor


def remove_vertices(G, vertices):
    """
    Remove all vertices in `vertices` from the graph `G`

    Parameters
    ----------
    G : nx.Graph
        The Graph from which vertices will be removed
    vertices : list
        The list of vertices in G to be removed

    Returns
    -------
    nx.Graph
        A copy of the graph `G` without the vertices listed in `vertices`
    """
    return G.copy().remove_nodes_from(vertices)


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
    Queue
        A queue with the path from `source` to `destination` already enqueued.
    """
    vertex_dict = dict(nx.bfs_predecessors(G, source))
    # Build a stack from destination to source which can be transferred into a queue
    stack = [destination, vertex_dict[destination]]
    while stack[-1] != source:
        stack.append(vertex_dict[stack[-1]])
    # Build the queue
    queue = SimpleQueue()
    while len(stack) > 0:
        queue.put(stack[-1])
        stack.pop()
    return queue


def merge(comp_ptr, u_rep, v_rep):
    """
    Merge the smaller component into the larger one

    Parameters
    ----------
    comp_ptr : Dict of Point
        The list of component pointers
    u_rep : Point
        The component representative for the first component
    v_rep : Point
        The component representative for the first component
    """
    # Find the sizes of the components
    if type(comp_ptr[u_rep]) is int:
        u_size = -comp_ptr[u_rep]
    else:
        return
    if type(comp_ptr[v_rep]) is int:
        v_size = -comp_ptr[v_rep]
    else:
        return

    if u_size < v_size:
        # Update the component representative for both vertices
        comp_ptr[u_rep] = v_rep
        comp_ptr[v_rep] = -(u_size + v_size)
    else:
        # Update the component representative for both vertices
        comp_ptr[v_rep] = u_rep
        comp_ptr[u_rep] = -(u_size + v_size)


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
        self.seeds = []
        self.polygons = []
        self.graph = nx.Graph()
        self.num_district = num_district
        self.bounds = bounds
        self.generate_seeds()
        self.voronoi = Vor(Point.to_list(self.seeds))
        self.generate_graph()

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
                known_end = None
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
            edge_vertices = [bound_start, bound_end]
            for vert in self.graph:
                if Polygon.in_segment(bound_start, bound_end, vert):
                    edge_vertices.append(vert)
            # Thanks to python magic methods, these are sorted from min y t0 max y and from min to max x if y is equal
            edge_vertices.sort()
            # Add the edges
            for vert in range(len(edge_vertices) - 1):
                start = edge_vertices[vert]
                end = edge_vertices[vert + 1]
                self.graph.add_edge(start, end, weight=start.simple_distance(end))

    def generate_polygons(self):
        """
        Take the graph of the Voronoi diagram and generate the polygon tesselation of the plane.

        Stores the polygons in a class attribute list
        """
        pass

    def relax(self):
        pass

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

    def __comp_rep(self, comp_ptr, u):
        """
        Find the component representative for the input vertex

        Parameters
        ----------
        comp_ptr : Dict
            The dictionary of component pointers
        u : Point
            The vertex of interest

        Returns
        -------
        Point :
            The component representative of the component u is a part of
        """
        # The pointer for the representative vertex is equal to negative the size of the component
        if comp_ptr[u] < 0:
            return u
        else:
            # Recurse to find the component representative, using path compression so that the next access is faster
            rep = self.__comp_rep(comp_ptr, comp_ptr[u])
            comp_ptr[u] = rep
            return rep

    def __components(self, G):
        """
        Find the components of graph G

        Parameters
        ----------
        G : nx.Graph
            The graph to find the connected components in

        Returns
        -------
        Dict of Point
            A dictionary such that each Point in the dictionary points to it's component representative or the size of
            the component that it represents
        """
        # Create and initialize the lists
        # comp_ptr is seeded with -1 as each vertex is in its own component at the start of the algorithm
        # comp_list is seeded with a list containing n for the same reason as comp_ptr gets -1
        comp_ptr = {}
        for v in G:
            comp_ptr[v] = -1

        # For each vertex, look at all of its adjacent vertices
        for u in G:
            for v in G[u]:
                # if the component representatives are different, merge the components
                u_rep = self.__comp_rep(comp_ptr, u)
                v_rep = self.__comp_rep(comp_ptr, v)
                if u_rep != v_rep:
                    merge(comp_ptr, u_rep, v_rep)
        return comp_ptr
