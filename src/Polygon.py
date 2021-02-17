import math
from src.Point import Point


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
    slope_p1_p2 = (p2.get_y() - p1.get_y()) / (p2.get_x() - p1.get_x())
    slope_p2_p3 = (p3.get_y() - p2.get_y()) / (p3.get_x() - p2.get_x())

    # If slope_p1_p2 == slope_p2_p3 then the three points are collinear
    if slope_p1_p2 == slope_p2_p3:
        return 0
    # If slope_p1_p2 > slope_p2_p3 then the three points are clockwise (right turn)
    elif slope_p1_p2 > slope_p2_p3:
        return 1
    # If slope_p1_p2 < slope_p2_p3 then the three points are counter-clockwise (left turn)
    else:
        return 2


def _in_segment(p1, p2, p3):
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
    >>> print(_in_segment(Point(0, 0), Point(5, 5), Point(1, 1.00000001)))
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
    elif p1.simple_distance(p3) + p3.simple_distance(p2) == p1.simple_distance(p2):
        return True
    else:
        return False


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
    if p1_q1_p2_or == 0 and _in_segment(p1, q1, p2):
        return True
    if p1_q1_q2_or == 0 and _in_segment(p1, q1, q2):
        return True
    if p2_q2_p1_or == 0 and _in_segment(p2, q2, p1):
        return True
    if p2_q2_q1_or == 0 and _in_segment(p2, q2, q1):
        return True

    return False


if __name__ == '__main__':
    print(_in_segment(Point(0, 0), Point(5, 5), Point(-1, -1)))


class Polygon:
    """
    This class represents a polygon as a list of vertex points ordered in clockwise order.
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

        Parameters
        ----------
        point : Point
            The point to check if in this polygon

        Returns
        -------
        bool
            True if contained in the polygon
        """
        n = len(self.vertices)

        # If n < 3, it can't be closed, thus no point is contained
        if n < 3:
            return False

        max_x = max(self.vertices.get_x)
        ext = Point(max_x, point.get_y())
        count = 0

        for i in range(n - 1):
            cur_point = self.vertices[i]
            next_point = self.vertices[i + 1]

            if _intersects(cur_point, next_point, point, ext):
                count += 1

        return (count % 2) == 1

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
                if _in_segment(self.vertices[v], self.vertices[(v + 1) % len(self.vertices)], u):
                    return True
        return False
