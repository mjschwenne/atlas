from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
from src.Backend.Pathfinder import Pathfinder
from scipy.spatial import ConvexHull


class Wall(Polygon):
    """
    This class represents a Wall using a Polygon

    Attributes
    ----------
    gates : list of Points
        The vertices in the polygon representing the wall that are gates.
    """

    def __init__(self, regions, graph, bounding_box):
        """
        Constructs a wall given a list of Regions

        Parameters
        ----------
        regions : List of Regions
            A list of Regions of the city
        graph : Graph
            Networkx Graph of regions
        bounding_box : Polygon
            The max polygon of the city (the bounding box of the city)
        """
        in_city_list = []

        for p in regions:
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

        # Reformat Polygons cut by Wall

        # Finds the Roads and Gates
        center_poly = None
        for p in regions:
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

    def set_gates(self, new_gates):
        """
        Sets the List of Points that defines the Gates of a Wall

        Parameters
        ----------
        new_gates : List of Points
            The new List of Points that defines the Gates of the Wall
        """
        self.gates = new_gates
