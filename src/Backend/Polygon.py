import math
from src.Backend.Point import Point


def print_list(list_name, points):
    print(f"{list_name} = [", end=" ")
    for i in points:
        print(f"{i},", end=" ")
    print("]")


def _three_point_orientation(p1, p2, p3):
    """
    Returns the orientation of three points in the form of an integer

    Parameters
    ----------
    p1 : Point
        First point in the three point orientation
    p2 : Point
        Second point in the three point orientation
    p3 : Point
        Third point in the three point orientation

    Returns
    -------
    int
        collinear = 0
        clockwise = 1
        counter-clockwise = 2
    """
    slp = (p2.get_y() - p1.get_y()) * (p3.get_x() - p2.get_x()) - (p2.get_x() - p1.get_x()) * (p3.get_y() - p2.get_y())

    # If slope_p1_p2 == slope_p2_p3 then the three points are collinear
    if slp == 0:
        return 0
    # If slope_p1_p2 > slope_p2_p3 then the three points are clockwise (right turn)
    elif slp > 0:
        return 1
    # If slope_p1_p2 < slope_p2_p3 then the three points are counter-clockwise (left turn)
    else:
        return 2


def _intersects(p1, q1, p2, q2):
    """
    Returns true if line segment from p1 to q1 intersects line segment from p2 to q2

    Parameters
    ----------
    p1 : Point
        The first point in the first line segment
    q1 : Point
        The second point in the first line segment
    p2 : Point
        The first point in the second line segment
    q2 : Point
        The second point in the second line segment

    Returns
    -------
    bool
        True if the line segment from p1 to q1 intersects line segment from p2 to q2
    """
    p1_q1_p2_or = _three_point_orientation(p1, q1, p2)  # Orientation between p1, q1, p2
    p1_q1_q2_or = _three_point_orientation(p1, q1, q2)  # Orientation between p1, q1, p2

    p2_q2_p1_or = _three_point_orientation(p2, q2, p1)  # Orientation between p2, q2, p1
    p2_q2_q1_or = _three_point_orientation(p2, q2, q1)  # Orientation between p2, q2, q1

    # General case
    if p1_q1_p2_or != p1_q1_q2_or and p2_q2_p1_or != p2_q2_q1_or:
        return True

    # Special cases
    if p1_q1_p2_or == 0 and Polygon.in_segment(p1, q1, p2):
        return True
    if p1_q1_q2_or == 0 and Polygon.in_segment(p1, q1, q2):
        return True
    if p2_q2_p1_or == 0 and Polygon.in_segment(p2, q2, p1):
        return True
    if p2_q2_q1_or == 0 and Polygon.in_segment(p2, q2, q1):
        return True

    return False


def clockwise_order(vertices):
    """
    Given a list of vertices, return them ordered in clockwise order

    Parameters
    ----------
    vertices : List
        The vertices of a polygon

    Returns
    -------
    List
        The vertices ordered in clockwise order.
    """
    # Calculate an approximate center of this polygon.
    # We just need a point inside the shape.
    # We cannot use Polygon.get_center() because that methods makes an assumption about the order of the vertices.
    simple_center = Point(0, 0)
    for v in vertices:
        cx, cy = simple_center.get()
        cx += v.get_x()
        cy += v.get_y()
        simple_center.set(cx, cy)
    cx, cy = simple_center.get()
    cx = cx / len(vertices)
    cy = cy / len(vertices)
    simple_center.set(cx, cy)

    # Create a mapping between the original vertices and the translation of the polygons such that simple_center is the
    # origin.
    vert_map = {}
    for v in vertices:
        vert_map[Point(v.get_x() - simple_center.get_x(), v.get_y() - simple_center.get_y())] = v

    # Create a list of angle such that each angle is the angle between the new point and the positive x-axis.
    # Add pi so that the angle vary from 0 to 2pi rather than -pi to pi
    angles = {}
    for v in vert_map.keys():
        angles[math.atan2(v.get_x(), v.get_y()) + math.pi] = vert_map[v]

    # Rebuild the angles dictionary to be sorted from greatest to least
    sorted_angles = {}
    for a in sorted(angles, reverse=True):
        sorted_angles[a] = angles[a]

    return list(sorted_angles.values())


class Polygon:
    """
    This class represents a polygon as a list of vertex points ordered in clockwise order.

    Attributes
    ----------
    vertices : List of Point
        Store the vertices in a clockwise list
    """

    def __init__(self, vertices, reorder=False):
        """
        Represents a polygon in 2D space.

        Parameters
        ----------
        vertices : List of Point
            The vertices that define the boundaries of the Polygon. The vertices must be ordered clockwise.
        """
        if not reorder:
            self.vertices = vertices
        else:
            self.vertices = clockwise_order(vertices)

        if len(self.vertices) != len(vertices):
            print(f"Received {len(vertices)} vertices, used {len(self.vertices)} vertices")
            print_list("vertices", vertices)
            print_list("used vertices", self.vertices)
            remove_vertices = [i for i in self.vertices if vertices.count(i) > 1]
            print_list("removed vertices", remove_vertices)

    def set_vertices(self, vertices):
        """
        Sets the vertices of the polygon

        Parameters
        ----------
        vertices : List of points
            The new vertices
        """
        self.vertices = vertices

    def get_vertices(self):
        """
        Gets the vertices of the polygon

        Returns
        -------
        List of Points
            The vertices
        """
        return self.vertices

    def get_perimeter(self):
        """
        Finds the perimeter of the polygon

        Returns
        -------
        float
            The perimeter of the polygon
        """
        perm = 0.0  # The polygon's perimeter
        length = len(self.vertices) - 1  # Number of points in vertices indexed at 0

        # Calculates perimeter
        for i in range(length):
            # Gets two connected points
            point1 = self.vertices[i]
            point2 = self.vertices[i + 1]

            # Finds a simple_distance between the two connected points
            perm += point1.simple_distance(point2)

        # Finds the distance back to the first point and adds that to perimeter
        perm += self.vertices[length].simple_distance(self.vertices[0])

        return perm

    def get_center(self):
        """
        Finds the centroid of the polygon.

        Returns
        -------
        Point
            Point representing the centroid of the polygon

        Notes
        -----
        We are using the general formula for a centroid, expressed below.

        .. math::

            C_x = \\frac{1}{6A} \\sum_{i=0}^{n-1}\\left(\\left(x_i + x_{i+1}\\right) \\times
            \\left(x_1 y_{i+1} - x_{i+1} y_i \\right) \\right) \\\\
            C_y = \\frac{1}{6A} \\sum_{i=0}^{n-1}\\left(\\left(y_i + y_{i+1}\\right) \\times
            \\left(x_1 y_{i+1} - x_{i+1} y_i \\right) \\right)

        Where `A` is defined as the area using the shoelace method.

        .. math::
            A = \\frac{1}{2} \\sum_{i=0}^{n-1}\\left(x_i y_{i+1} - x_{i+1} y_i\\right)

        More information can be found `here <https://en.wikipedia.org/wiki/Centroid#Of_a_polygon>`_.
        """
        # initialize the centroid and other variables
        centroid = Point(0, 0)
        signed_area = 0
        # Loop in a counterclockwise direction to produce a positive area calculation
        # Iterate over [n - 1, n - 2, n - 3,..., 0]
        for v in range(len(self.vertices) - 1, -1, -1):
            x0, y0 = self.vertices[v].get()
            x1, y1 = self.vertices[(v + 1) % len(self.vertices)].get()
            # Calculate the signed area of this triangle as a 2x2 matrix determinant
            a = x0 * y1 - x1 * y0
            signed_area += a
            # Update the centroid to include the next triangle
            cx, cy = centroid.get()
            centroid.set(cx + a * (x0 + x1), cy + a * (y0 + y1))
        # Calculate the finial position of the centroid
        signed_area *= 3  # This is 0.5 * 6, see formula for more details
        if signed_area == 0:
            print("THIS IS GOING TO CRASH SOMETHING")
        centroid.set_x(centroid.get_x() / signed_area)
        centroid.set_y(centroid.get_y() / signed_area)
        return centroid

    def is_convex(self):
        """
        Returns true if the polygon is convex and has no intersecting lines.

        Returns
        -------
        bool
            Returns true if the polygon is convex and has no intersecting lines, or false if not.

        Notes
        -----
        This method will return false if the number of vertices in the polygon is less than 3 or if any of the vertices
        repeat.
        """
        # Fewer than 3 vertices can not be convex
        if len(self.vertices) < 3:
            return False

        # Initial values for convex check loop
        old_x = self.vertices[-2].get_x()  # Two points back from start
        old_y = self.vertices[-2].get_y()  # Two points back from start
        new_x = self.vertices[-1].get_x()  # One point back from start
        new_y = self.vertices[-1].get_y()  # One point back from start
        # The direction from Pn to P1, where Pn is the last Point in vertices
        new_direction = math.atan2(new_y - old_y, new_x - old_x)
        angle_sum = 0.0  # Angle sum used for checking intersectionality

        orientation = 0.0

        i = 0

        # Check Loop
        for point in self.vertices:
            # Changing old new values to old values
            old_x = new_x
            old_y = new_y
            old_direction = new_direction

            # Find the new values
            new_x = point.get_x()
            new_y = point.get_y()
            new_direction = math.atan2(new_y - old_y, new_x - old_x)

            # If the point is a repeat of the last point, not convex
            if old_x == new_x and old_y == new_y:
                return False

            # Calculate angle and check the angle as being within the bounds of convex polygon angle
            angle = new_direction - old_direction
            if angle <= -math.pi:
                angle += math.pi * 2
            elif angle > math.pi:
                angle -= math.pi * 2

            # Initial value of orientation
            if i == 0:
                if angle == 0.0:
                    return False
                orientation = 1.0
                if angle <= 0.0:
                    orientation = -1.0
            else:
                if orientation * angle <= 0.0:
                    return False

            # Add angle to angle sum for final intersectionality check
            angle_sum += angle

            i += 1

        # Final intersectionality check
        # If the angle is a full rotation (in radians) it doesn't intersect
        return round(abs(angle_sum), 5) == round(math.pi * 2, 5)

    def is_contained(self, point):
        """
        Returns true if Point point is located on the edge of or in this Polygon.

        Parameters
        ----------
        point : Point
            The point to check if in this polygon

        Returns
        -------
        bool
            True if contained in the polygon

        Notes
        -----
        This method utilises the Ray-casting algorithm. A horizontal ray from point increasing to infinity will
        intersect with the polygon an odd number of times if it is located inside the polygon and an even number of
        times if point is located outside the polygon.

        You can find more information about the algorithm here: https://rosettacode.org/wiki/Ray-casting_algorithm
        """
        n = len(self.vertices)

        # If n < 3, it can't be closed, thus no point is contained
        if n < 3:
            return False

        # Finds the max x of the polygon used as the x value for the furthest extent of the ray
        max_x = self.vertices[0].get_x()
        for p in self.vertices:
            if p.get_x() > max_x:
                max_x = p.get_x()
            if p == point:
                return True

        if max_x < point.get_x():
            return False

        ext = Point(max_x, point.get_y())  # The furthest extent of the ray needed for the algorithm
        intersect_count = 0  # count of number of times the ray crosses an edge of the polygon
        i = 0  # index of vertices in the polygon
        original_y = point.get_y()  # Stores the y value of the point to put back later if the y value has to be changed

        # Finds how many times the ray crosses the an edge of the polygon
        while True:
            next_value = (i + 1) % n  # The next vertex index
            cur_vertex = self.vertices[i]  # The current point (vertex) to start the edge of the polygon
            next_vertex = self.vertices[next_value]  # The next point (vertex) to end the edge of the polygon

            # Need to reset the y value of checking point each loop in case the point is level and in_segment with both
            # points, also avoids a double change of the y value
            point.set_y(original_y)
            ext.set_y(original_y)

            # To avoid an edge case where the loop will count crossing a vertex twice, if the point lines up
            # horizontally with any vertex being checked, we slightly move (+0.00000001) the y value of the point being
            # checked we move the y value back at the end of the loop
            if (point.get_y() == cur_vertex.get_y() or point.get_y() == next_vertex.get_y()) and \
                    not self.in_segment(cur_vertex, next_vertex, point):
                point.set_y(point.get_y() + 0.00000001)
                ext.set_y(ext.get_y() + 0.00000001)

            # If the ray intersects the current edge of the polygon we increase the intersect_count by one
            if _intersects(cur_vertex, next_vertex, point, ext):
                # If the point and the line segment are collinear we return if the point is in_segment with the edge
                if _three_point_orientation(cur_vertex, next_vertex, point) == 0:
                    return Polygon.in_segment(cur_vertex, next_vertex, point)
                intersect_count += 1

            # We set the new current index to the old next index
            i = next_value

            # We break the loop if the i returns to 0 (The first vertex in the polygon)
            if i == 0:
                break

        # We reset the y value of the point to make sure we haven't changed the value.
        point.set_y(original_y)

        # If the ray intersected an odd amount of times the point is inside, if not it is outside
        return intersect_count % 2 == 1

    def is_bordering(self, other):
        """
        Checks to see if a given polygon borders this polygon.

        Parameters
        ----------
        other : Polygon
            The polygon we need to check for a border

        Returns
        -------
        bool
            True if the two share and edge, false otherwise.

        Notes
        -----
        I have not been able to find a way to do this in less than :math:`O(n^2)` complexity, which is acceptable
        so long as we do not compare every polygon to every other polygon in the city. That will tank performance.

        This will not catch intersecting polygons unless one vertex sits on an edge of the other.
        """
        for v in range(len(self.vertices)):
            for u in other.vertices:
                if Polygon.in_segment(self.vertices[v], self.vertices[(v + 1) % len(self.vertices)], u):
                    return True
        return False

    @staticmethod
    def to_polygon(vertices):
        """
        Returns a polygon given a list of lists, i.e. [[1, 2], [3, 4], [5, 6]] => polygon with those vertices

        Parameters
        ----------
        vertices : list of lists
            the vertices of the polygon in the form of a list of lists

        Returns
        -------

        """
        return Polygon(Point.to_points(vertices))

    @staticmethod
    def to_points(polygons):
        """
        Takes a list of polygons and converts it to a list of points

        Parameters
        ----------
        polygons : List of Polygons
            list of Polygons

        Returns
        -------
        List of Points
            List of all vertices in the list of Polygons
        """
        points = {polygons[0].vertices[0]}
        for poly in polygons:
            for p in poly.vertices:
                points.add(p)
        return list(points)

    @staticmethod
    def in_segment(p1, p2, p3):
        """
        Returns true if p3 is in the line segment from p1 to p2.

        Parameters
        ----------
        p1 : Point
            First point of the line segment
        p2 : Point
            Second point of the line segment
        p3 : Point
            The point to see if it is in the line segment

        Returns
        -------
        bool
            True if p3 is in the line segment from p1 to p2

        Notes
        -----
        After checking for vertical and horizontal lines, we know that the `p3` is only on the line segment between
        `p1` and `p2` if the distance from `p1` to `p2` thorough `p3` is the same as the distance from `p1` directly
        to `p2`.

        This method is only accurate to approximately eight decimal places, after which internal rounding can affect the
        result.
        >>> print(Polygon.in_segment(Point(0, 0), Point(5, 5), Point(1, 1.00000001)))
        True

        Example of an incorrect, but very close test.
        """
        # Case 1: Vertical Line.
        # If p3's y-coordinate is within the y-range of this line segment, return if they have the same x-coordinate
        if round(p1.get_x(), 8) == round(p2.get_x(), 8) and \
                min(p1.get_y(), p2.get_y()) <= p3.get_y() <= max(p1.get_y(), p2.get_y()):
            return round(p1.get_x(), 8) == round(p3.get_x(), 8)
        # Case 2: Horizontal Line.
        # If p3's x-coordinate is within the x-range of this line segment, return if they have the same y-coordinate
        elif round(p1.get_y(), 8) == round(p2.get_y(), 8) and min(p1.get_x(), p2.get_x()) <= p3.get_x() <= max(
                p1.get_x(), p2.get_x()):
            return round(p1.get_y(), 8) == round(p3.get_y(), 8)
        # Case 3:
        # If the distance from p1 -> p2 -> p3 == to the distance from p1 directly to p2 then they are on the same line
        # as the optimal path from p1 to p2 is a straight line. Any deviation from this line will increase the distance
        # required to go to p3 first.
        # Because the simple_distance() method returns a float value, I only consider to the eight decimal places to
        # avoid rounding errors.
        elif round(p1.simple_distance(p2), 8) == round(p1.simple_distance(p3) + p3.simple_distance(p2), 8):
            return True
        else:
            return False

    def split(self, p, ang, gap):
        """
        splits a polygon along a point and an angle relative to edge of p

        Parameters
        ----------
        p : Point
            The starting point of the cut
        ang : float
            The angle of the line to cut down in radians
        gap : float
            width of the cut between the split polygon

        Returns
        -------
        List of Polygons
            A list of polygons from the resulting split
        """
        x = self.furthest_point(p)
        ext_p = Polygon.find_ext_point(x, ang, p)

        edge = self.find_intersecting_edge(p, ext_p)

        inter_p = self.intersection(edge[0], edge[1], p, ext_p)

        return self.cut_gap(p, inter_p, gap)

    def cut(self, p1, p2):
        """
        Cuts a polygon along two points

        Parameters
        ----------
        p1 : Point
            First Point
        p2 : Point
            Second Point

        Returns
        -------
        List of Polygons
            Two new polygons formed by the cut
        """
        new_vertices = self.vertices.copy()
        pointer = 1
        for i in range(0, len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            if Polygon.in_segment(v1, v2, p1) and p1 not in self.vertices:
                new_vertices.insert(pointer, p1)
                pointer += 1
            if Polygon.in_segment(v1, v2, p2) and p2 not in self.vertices:
                new_vertices.insert(pointer, p2)
                pointer += 1
            pointer += 1

        is_poly1 = True
        poly1_point_list = []
        poly2_point_list = []
        for v in new_vertices:
            if v == p1 or v == p2:
                is_poly1 = not is_poly1
                poly1_point_list.append(v)
                poly2_point_list.append(v)
                continue
            if is_poly1:
                poly1_point_list.append(v)
            else:
                poly2_point_list.append(v)

        return [Polygon(poly1_point_list), Polygon(poly2_point_list)]

    def cut_gap(self, p1, p2, gap):
        """
        Cuts a polygon along two points

        Parameters
        ----------
        p1 : Point
            First Point
        p2 : Point
            Second Point
        gap : float
            width of the cut

        Returns
        -------
        List of Polygons
            Two new polygons formed by the cut
        """
        if gap == 0:
            return self.cut(p1, p2)
        new_vertices = self.vertices.copy()
        pointer = 1
        for i in range(0, len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            if Polygon.in_segment(v1, v2, p1):
                ang = math.atan2((v2.get_y() - v1.get_y()), (v2.get_x() - v1.get_x()))
                vector = Point(math.cos(ang), math.sin(ang))
                first_p = Point(round(p1.get_x() - gap * vector.get_x(), 8),
                                round(p1.get_y() - gap * vector.get_y(), 8))
                second_p = Point(round(p1.get_x() + gap * vector.get_x(), 8),
                                 round(p1.get_y() + gap * vector.get_y(), 8))

                if self.in_segment(v1, v2, first_p):
                    new_vertices.insert(pointer, first_p)
                    pointer += 1
                new_vertices.insert(pointer, p2)
                pointer += 1
                if self.in_segment(v1, v2, second_p):
                    new_vertices.insert(pointer, second_p)
                    pointer += 1
            if Polygon.in_segment(v1, v2, p2):
                ang = math.atan2((v2.get_y() - v1.get_y()), (v2.get_x() - v1.get_x()))
                vector = Point(math.cos(ang), math.sin(ang))
                first_p = Point(round(p2.get_x() - gap * vector.get_x(), 8),
                                round(p2.get_y() - gap * vector.get_y(), 8))
                second_p = Point(round(p2.get_x() + gap * vector.get_x(), 8),
                                 round(p2.get_y() + gap * vector.get_y(), 8))

                if self.in_segment(v1, v2, first_p):
                    new_vertices.insert(pointer, first_p)
                    pointer += 1
                new_vertices.insert(pointer, p2)
                pointer += 1
                if self.in_segment(v1, v2, second_p):
                    new_vertices.insert(pointer, second_p)
                    pointer += 1
            pointer += 1

        is_poly1 = True
        poly1_point_list = []
        poly2_point_list = []
        for v in new_vertices:
            if v == p1 or v == p2:
                is_poly1 = not is_poly1
                continue
            if is_poly1:
                poly1_point_list.append(v)
            else:
                poly2_point_list.append(v)

        return [Polygon(poly1_point_list), Polygon(poly2_point_list)]

    @staticmethod
    def intersection(p1, p2, p3, p4):
        """
        Finds the point of intersection given twp line segments
        Parameters
        ----------
        p1 : Point
            The first point in the first line segment
        p2 : Point
            The second point in the first line segment
        p3 : Point
            The first point in the second line segment
        p4 : Point
            The second point in the second line segment

        Returns
        -------
        Point
            The intersection
        """
        # Standard Form of Line Segment from p1 to p2
        a1 = p2.get_y() - p1.get_y()
        b1 = p1.get_x() - p2.get_x()
        c1 = (a1 * p1.get_x()) + (b1 * p1.get_y())

        # Standard Form of Line Segment from p3 to p4
        a2 = p4.get_y() - p3.get_y()
        b2 = p3.get_x() - p4.get_x()
        c2 = (a2 * p3.get_x()) + (b2 * p3.get_y())

        # Denominator for system of equations calculations below
        d = ((a1 * b2) - (a2 * b1))

        # If the line segments are parallel return None (the line segments have no intersection)
        # This also handles collinear lines (which would otherwise return multiple intersection points)
        if d == 0:
            return None

        # Solve for x using the system of equations above
        inter_x = ((b2 * c1) - (b1 * c2)) / d

        # Solve for y using the system of equations above
        inter_y = ((a1 * c2) - (a2 * c1)) / d

        return Point(round(inter_x, 8), round(inter_y, 8))

    def area(self):
        """
        Finds the area of the polygon

        Returns
        -------
        float
            The area of the polygon
        """
        a = 0
        for i in range(0, len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            a += v1.get_x() * v2.get_y() - v1.get_y() * v2.get_x()
        return abs(a / 2.0)

    def furthest_point(self, point):
        """
        Finds the furthest point in this polygon from a give point

        Parameters
        ----------
        point : Point
            The point to compare for every polygon vertices

        Returns
        -------
        Point
            The furthest point from the given point in the polygon
        """
        max_point = self.vertices[0]
        max_dist = self.vertices[0].simple_distance(point)
        for v in self.vertices:
            new_dist = v.simple_distance(point)
            if new_dist > max_dist:
                max_point = v
                max_dist = new_dist
        return max_point

    @staticmethod
    def intersect_segment(p1, p2, p3, p4):
        """
        Returns True if two line segments defined by 4 points intersect

        Parameters
        ----------
        p1 : Point
            First point in the first line segment
        p2 : Point
            Second point in the second line segment
        p3 : Point
            First point in the second line segment
        p4 : Point
            Second point in the second line segment

        Returns
        -------
        bool
            True if the two line segments intersect
        """
        inter = Polygon.intersection(p1, p2, p3, p4)
        if inter is not None and Polygon.in_segment(p1, p2, inter):
            return True
        return False

    @staticmethod
    def intersect_segment_alt(p1, p2, p3, p4):
        """
        Returns True if two line segments defined by 4 points intersect

        Parameters
        ----------
        p1 : Point
            First point in the first line segment
        p2 : Point
            Second point in the second line segment
        p3 : Point
            First point in the second line segment
        p4 : Point
            Second point in the second line segment

        Returns
        -------
        bool
            True if the two line segments intersect
        """
        inter = Polygon.intersection(p1, p2, p3, p4)
        if inter is not None and (Polygon.in_segment(p1, p2, inter) and Polygon.in_segment(p3, p4, inter)):
            return True
        return False

    @staticmethod
    def find_ext_point(furthest_point, ang, initial_p):
        """
        Find an extreme point given a furthest_point, an angle, and an initial point

        Parameters
        ----------
        furthest_point : Point
            the furthest point for reference to find an extreme point
        ang : float
            the angle towards the extreme point
        initial_p : Point
            the initial point for the line towards the extreme point

        Returns
        -------
        Point
            the extreme point
        """
        simple_dist = initial_p.simple_distance(furthest_point)
        if (ang % (math.pi / 2)) == 0 and (ang % math.pi) != 0:
            return Point(initial_p.get_x(), initial_p.get_y()+simple_dist)
        elif (ang % math.pi) == 0:
            return Point(initial_p.get_x()+simple_dist, initial_p.get_y())
        else:
            m = round(math.tan(ang), 8)
            n = initial_p.get_y() - (m * initial_p.get_x())
            if furthest_point.get_x() != initial_p.get_x():
                p = Point(furthest_point.get_x(), n + m * furthest_point.get_x())
            else:
                p = Point((furthest_point.get_y() - n) / m, furthest_point.get_y())
            return p

    def find_intersecting_edge(self, p, ext_p):
        """
        Given a line segment this method returns an edge that that line segment intersects

        Parameters
        ----------
        p : point
            the first point of the line segment
        ext_p : Point
            the second point of the line segment

        Returns
        -------
        list of Points
            the edge on the polygon that the line segment crosses
        """
        for i in range(0, len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]

            if Polygon.intersect_segment(v1, v2, p, ext_p) and not self.in_segment(v1, v2, p):
                return v1, v2
        return None

    def find_intersecting_edges(self, p, ext_p):
        """
        Given a line segment this method returns edges that that line segment intersects, this is used because of an
        edge case in the find_intersecting_edges

        Parameters
        ----------
        p : point
            the first point of the line segment
        ext_p : Point
            the second point of the line segment

        Returns
        -------
        list of list of points
            the edge on the polygon that the line segment crosses
        """
        for i in range(0, len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]

            if Polygon.intersect_segment_alt(v1, v2, p, ext_p) and not self.in_segment(v1, v2, p):
                return v1, v2
        return None

    def is_rectangle(self):
        """
        Check a given polygon to see if it is a rectangle

        Returns
        -------
        bool
            True if the polygon is a rectangle
        """
        pi2 = math.pi/2
        pi = math.pi
        for i in range(0, len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            ang = abs(math.atan2((v1.get_y() - v2.get_y()), (v1.get_x() - v2.get_x())))
            if ang != pi and ang != pi2 and ang != 0:
                return False
        return True

    def rectangle_inside(self, p1, p2):
        """
        Finds a rectangle given an edge of the polygon

        Parameters
        ----------
        p1 : Point
            one edge vertices
        p2 : Point
            second edge vertices

        Returns
        -------
        Polygon
            The rectangle inside the polygon
        """
        if p1 not in self.vertices or p2 not in self.vertices:
            return Polygon([])
        if self.is_rectangle():
            return self

        ang = math.atan2((p1.get_y() - p2.get_y()), (p1.get_x() - p2.get_x())) + (math.pi / 2)

        ext_p1 = Polygon.find_ext_point(self.furthest_point(p1), ang, p1)
        ext_p2 = Polygon.find_ext_point(self.furthest_point(p2), ang, p2)

        edge_p1 = self.find_intersecting_edge(p1, ext_p1)
        edge_p2 = self.find_intersecting_edge(p2, ext_p2)

        i_p1 = Polygon.intersection(p1, ext_p1, edge_p1[0], edge_p1[1])
        i_p2 = Polygon.intersection(p2, ext_p2, edge_p2[0], edge_p2[1])

        dist_p1_i = p1.simple_distance(i_p1)
        dist_p2_i = p2.simple_distance(i_p2)

        if dist_p1_i > dist_p2_i:
            u = Point(i_p1.get_x() - p1.get_x(), i_p1.get_y() - p1.get_y())
            mag = math.sqrt(pow(u.get_x(), 2) + pow(u.get_y(), 2))
            u.set_x(u.get_x() / mag)
            u.set_y(u.get_y() / mag)
            new_p = Point(p1.get_x() + dist_p2_i * u.get_x(), p1.get_y() + dist_p2_i * u.get_y())
            return Polygon([p2, i_p2, new_p, p1])
        else:
            u = Point(i_p2.get_x() - p2.get_x(), i_p2.get_y() - p2.get_y())
            mag = math.sqrt(pow(u.get_x(), 2) + pow(u.get_y(), 2))
            u.set_x(u.get_x() / mag)
            u.set_y(u.get_y() / mag)
            new_p = Point(p2.get_x() + dist_p1_i * u.get_x(), p2.get_y() + dist_p1_i * u.get_y())
            return Polygon([p1, i_p1, new_p, p2])

    def furthest_conglomerate_point(self, p):
        """
        Finds a point that has the furthest x value among all points in the polygon and has the furthest y value among
        all points in the polygon

        Parameters
        ----------
        p : Point
            the point to find the furthest point from
        """
        x = p.get_x()
        y = p.get_y()
        max_point = Point(self.vertices[0].get_x(), self.vertices[0].get_y())
        max_x_dist = x - max_point.get_x()
        max_y_dist = y - max_point.get_y()
        for v in self.vertices:
            if max_x_dist < x - v.get_x():
                max_point.set_x(v.get_x())
                max_x_dist = x - v.get_x()
            if max_y_dist < y - v.get_y():
                max_point.set_y(v.get_y())
                max_y_dist = x - v.get_y()
        return max_point

    def furthest_bounding_point(self, p):
        # make bounding polygon
        g_x = self.vertices[0].get_x()
        g_y = self.vertices[0].get_y()
        l_x = self.vertices[0].get_x()
        l_y = self.vertices[0].get_y()
        for v in self.vertices:
            x = v.get_x()
            y = v.get_y()
            if x > g_x:
                g_x = x
            if x < l_x:
                l_x = x
            if y > g_y:
                g_y = y
            if y < l_y:
                l_y = y
        bound = Polygon([Point(l_x, l_y), Point(g_x, l_y), Point(g_x, g_y), Point(l_x, g_y)])
        return bound.furthest_point(p)

    def crazy_far_furthest_point(self, p):
        larger = self.scale_of_polygon(10)
        return larger.furthest_conglomerate_point(p)

    def cut_out(self, interior_polygon):
        """
        Cuts a larger polygon into parts without an interior polygon part

        Parameters
        ----------
        interior_polygon : Polygon
            The polygon to cut out

        Returns
        -------
        list of Polygons
            the parts of the original polygon without the interior polygon
        """
        poly_list = []
        if not interior_polygon.inside(self):
            return None
        running_poly = self
        for i in range(0, len(interior_polygon.vertices)):
            v1 = interior_polygon.vertices[i]
            v2 = interior_polygon.vertices[(i + 1) % len(interior_polygon.vertices)]
            ang = math.atan2((v1.get_y() - v2.get_y()), (v1.get_x() - v2.get_x()))
            if not (v1 in self.vertices and v2 in self.vertices):
                new_polys = running_poly.split(v1, ang, 0)
                print_list("Poly0", new_polys[0].vertices)
                print_list("Poly1", new_polys[1].vertices)
                if interior_polygon.inside(new_polys[1]):
                    running_poly = new_polys[1]
                    poly_list.append(new_polys[0])
                else:
                    running_poly = new_polys[0]
                    poly_list.append(new_polys[1])
                print_list("Running Poly", running_poly.vertices)
        return poly_list

    def cut_out_2(self, interior_polygon):
        """
        Cuts out a shape from a larger polygon if the interior polygon is a scaled down version of the larger polygon

        Parameters
        ----------
        interior_polygon : Polygon
            the scaled down version of the larger polygon to cut out

        Returns
        -------
        list of Polygons
            the cut out parts on the exterior of the larger polygon
        """
        if len(self.vertices) != len(interior_polygon.vertices):
            return None
        # make vertices pairs
        vertices_pairs = []
        for i in range(0, len(self.vertices)):
            v = self.vertices[i]
            p = interior_polygon.vertices[i]
            vertices_pairs.append((v, p))

        # make exterior polys
        poly_list = []
        for i in range(0, len(vertices_pairs)):
            p1 = vertices_pairs[i]
            p2 = vertices_pairs[(i + 1) % len(vertices_pairs)]
            poly_list.append(Polygon([p1[0], p1[1], p2[1], p2[0]]))
        return poly_list

    def cut_out_gap_2(self, interior_polygon, scalar):
        """
        Cuts out a shape from a larger polygon if the interior polygon is a scaled down version of the larger polygon
        with a gap

        Parameters
        ----------
        interior_polygon : Polygon
            the scaled down version of the larger polygon to cut out
        scalar : float
            the scalar to put on the interior polygon to make the gap

        Returns
        -------
        list of Polygons
            the cut out parts on the exterior of the larger polygon
        """
        new_interior_polygon = interior_polygon.scale_of_polygon(scalar)
        return self.cut_out_2(new_interior_polygon)

    def easy_cut(self, p, ang, gap):
        if self.on_edge(p):
            return self.split(p, ang, gap)
        furthest_point = self.furthest_point(p)
        ext_1 = Polygon.find_ext_point(furthest_point, ang, p)
        dist = ext_1.simple_distance(p) * 2
        u = Point(p.get_x() - ext_1.get_x(), p.get_y() - ext_1.get_y())
        mag = math.sqrt(pow(u.get_x(), 2) + pow(u.get_y(), 2))
        u.set_x(u.get_x() / mag)
        u.set_y(u.get_y() / mag)
        ext_2 = Point(ext_1.get_x() + dist * u.get_x(), ext_1.get_y() + dist * u.get_y())

        edge1 = self.find_intersecting_edges(p, ext_1)
        edge2 = self.find_intersecting_edges(p, ext_2)

        i_1 = Polygon.intersection(p, ext_1, edge1[0], edge1[1])
        i_2 = Polygon.intersection(p, ext_1, edge2[0], edge2[1])

        return self.cut_gap(i_1, i_2, gap)

    def on_edge(self, p):
        """
        Checks to see if a given point p is on any edge of the polygon

        Parameters
        ----------
        p : Point
            The point to check to see if it is on any edge of the polygon

        Returns
        -------
        bool
            True if p is on any edge of the polygon
        """
        for i in range(0, len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]
            if Polygon.in_segment(v1, v2, p):
                return True
        return False

    def inside(self, larger_polygon):
        """
        Checks a given polygon to see if it is in a larger polygon

        Parameters
        ----------
        larger_polygon : Polygon
            The larger polygon that could contain the given polygon

        Returns
        -------
        bool
            True if the given polygon is in larger_polygon
        """
        for v in self.vertices:
            if not larger_polygon.is_contained(v):
                return False
        return True

    def scale_of_polygon(self, scalar):
        """
        Scales a polygon by a scalar and returns a new scaled polygon centered on the original polygon's center

        Parameters
        ----------
        scalar : float
            The scalar to scale the polygon by (could be positive or negative for shrink or grow)

        Returns
        -------
        Polygon
            The new scaled polygon centered on the original polygon's center
        """

        scale_poly_vertices = []
        if scalar == 1:
            return self
        center = self.get_center()
        for p in self.vertices:
            scale_poly_vertices.append(Point((p.get_x() * scalar), (p.get_y() * scalar)))
        poly = Polygon(scale_poly_vertices)
        poly.move_center_to(center)

        return poly

    def move_polygon_by_center(self, left_right_distance, up_down_distance):
        """
        Moves a polygon's center by left_right_distance left or right, and up_down_distance up or down.

        Parameters
        ----------
        left_right_distance : float
            the distance to move the center of the polygon by left or right
        up_down_distance : float
            the distance to move the center of the polygon by up or down
        """
        for v in self.vertices:
            v.set_x(v.get_x() + left_right_distance)
            v.set_y(v.get_y() + up_down_distance)

    def move_center_to(self, p):
        """
        Moves a polygon's center to a given point p

        Parameters
        ----------
        p : Point
            The new center for the polygon
        """
        center = self.get_center()
        left_right_distance = p.get_x() - center.get_x()
        up_down_distance = p.get_y() - center.get_y()
        self.move_polygon_by_center(left_right_distance, up_down_distance)

    def __eq__(self, other):
        """
        Test to see if another Polygon is equal to this one.

        Parameters
        ----------
        other : Polygon
            The other Polygon

        Returns
        -------
        bool
            True if the two polygons have the same coordinate list, false otherwise
        """
        # If there is a different number of vertices, the polygons cannot be the same
        if len(self.vertices) != len(other.vertices):
            return False
        sorted_self_vertices = self.vertices.copy()
        sorted_self_vertices.sort()
        sorted_other_vertices = other.vertices.copy()
        sorted_other_vertices.sort()
        for i in range(len(sorted_self_vertices)):
            if sorted_self_vertices[i] != sorted_other_vertices[i]:
                return False
        return True

    def __hash__(self):
        """
        Hash the tuples of the vertices
        """
        sorted_vertices = self.vertices.copy()
        sorted_vertices.sort()
        return hash(tuple(sorted_vertices))
