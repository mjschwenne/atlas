import math
from src.Backend.Point import Point


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
    slope = (p2.get_y() - p1.get_y()) * (p3.get_x() - p2.get_x()) - \
            (p2.get_x() - p1.get_x()) * (p3.get_y() - p2.get_y())

    # If slope_p1_p2 == slope_p2_p3 then the three points are collinear
    if slope == 0:
        return 0
    # If slope_p1_p2 > slope_p2_p3 then the three points are clockwise (right turn)
    elif slope > 0:
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


class Polygon:
    """
    This class represents a polygon as a list of vertex points ordered in clockwise order.

    Attributes
    ----------
    vertices : List of Point
        Store the vertices in a clockwise list
    """

    def __init__(self, vertices):
        """
        Represents a polygon in 2D space.

        Parameters
        ----------
        vertices : List of Point
            The vertices that define the boundaries of the Polygon. The vertices must be ordered clockwise.
        """
        self.vertices = vertices

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

            # To avoid an edge case where the loop will count crossing a vertex twice, if the point lines up
            # horizontally with any vertex being checked, we slightly move (+0.00000001) the y value of the point being
            # checked we move the y value back at the end of the loop
            if point.get_y() == cur_vertex.get_y() or point.get_y() == next_vertex.get_y():
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
        >>> print(in_segment(Point(0, 0), Point(5, 5), Point(1, 1.00000001)))
        True

        Example of an incorrect, but even close test.
        """
        # Case 1: Vertical Line.
        # If p3's y-coordinate is within the y-range of this line segment, return if they have the same x-coordinate
        if p1.get_x() == p2.get_x() and min(p1.get_y(), p2.get_y()) <= p3.get_y() <= max(p1.get_y(), p2.get_y()):
            return p1.get_x() == p3.get_x()
        # Case 2: Horizontal Line.
        # If p3's x-coordinate is within the x-range of this line segment, return if they have the same y-coordinate
        elif p1.get_y() == p2.get_y() and min(p1.get_x(), p2.get_x()) <= p3.get_x() <= max(p1.get_x(), p2.get_x()):
            return p1.get_y() == p3.get_y()
        # Case 3:
        # If the distance from p1 -> p2 -> p3 == to the distance from p1 directly to p2 then they are on the same line
        # as the optimal path from p1 to p2 is a straight line. Any deviation from this line will increase the distance
        # required to go to p3 first.
        # Because the simple_distance() method returns a float value, I only consider to the eight decimal places to
        # avoid rounding errors.
        elif float(int((p1.simple_distance(p3) + p3.simple_distance(p2)) * 100000000) / 100000000.0) == \
                float(int(p1.simple_distance(p2) * 100000000) / 100000000.0):
            return True
        else:
            return False
