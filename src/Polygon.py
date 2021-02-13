import math
from src import Point

class Polygon:

    def __init__(self, vertices):
        """
        Represents a polygon in 2D space.

        Parameters
        ----------
        vertices : List of Points
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
            point2 = self.vertices[i+1]

            # Finds a simple_distance between the two connected points
            perm += point1.simple_distance(point2)

        # Finds the distance back to the first point and adds that to perimeter
        perm += self.vertices[length].simple_distance(self.vertices[0])

        return perm

    def get_center(self):
        pass

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

    def is_contained(self):
        pass

    def is_bordering(self):
        pass
