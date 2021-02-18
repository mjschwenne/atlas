import math


class Point:
    """
    Point storing x and y coordinates with associated distance functions.

    Attributes
    ----------
    x : float
        The point's x value.
    y : float
        The point's y value.

    Methods
    -------
    set_x(x_new)
        Sets the x value of the point.
    set_y(y_new)
        Sets the y value of the point
    get_x()
        Gets the x value of the point
    get_y()
        Gets the y value of the point
    simple_distance(point)
        Finds the simple distance between this point and another point.
    manhattan_distance(point)
        Finds the manhattan distance between this point and another point.
    """

    def __init__(self, x, y):
        """
        Point Constructor

        Parameters
        ----------
        x : float
            The initial `x` value of this Point.
        y : float
            The initial `y` value of this Point.
        """
        self.x = x
        self.y = y

    def set(self, x_new, y_new):
        """
        Move the point by assigning a new `x` and `y` coordinates.

        Parameters
        ----------
        x_new : float
            The new `x` coordinate for this point
        y_new : float
            Thew new `y` coordinate for this point
        """
        self.x = x_new
        self.y = y_new

    def set_x(self, x_new):
        """
        Sets the value of `x` for a point.

        Parameters
        ----------
        x_new : float
            The new `x` value of the point.
        """
        self.x = x_new

    def set_y(self, y_new):
        """
        Sets the value of `y` for a point.

        Parameters
        ----------
        y_new
            The new `y` value of the point.
        """
        self.y = y_new

    def get(self):
        """
        Return the point coordinates in tuple form.

        Returns
        -------
        tuple
            A tuple in the form (`x`, `y`)
        """
        return self.x, self.y

    def get_x(self):
        """
        Gets the x value of the point

        Returns
        -------
        float
            The x value of the point
        """
        return self.x

    def get_y(self):
        """
        Gets the y value of the point

        Returns
        -------
        float
            The y value of the point
        """
        return self.y

    def simple_distance(self, point):
        """
        Finds the distance between this point and another point.

        Notes
        -----
        .. math:: d = \sqrt{(x_2 - x_1) + (y_2 - y_1)}

        Parameters
        ----------
        point : Point
            The point to find the distance between.

        Returns
        -------
        float
            The simple distance between this point and another point.
        """
        return math.sqrt(math.pow((point.x - self.x), 2.0) + math.pow((point.y - self.y), 2.0))

    def manhattan_distance(self, point):
        """
        Finds the manhattan distance between this point and another point,
        which is the total displacement in x and y.

        Parameters
        ----------
        point : Point
            The point to find the distance between.

        Returns
        -------
        float
            The manhattan distance between this point and another point.
        """
        return abs(self.x - point.x) + abs(self.y - point.y)

    def is_equal(self, point):
        """
        Returns true if this point is equal to point

        Parameters
        ----------
        point : Point
            The Point to see if it is equal to this point

        Returns
        -------
        bool
            Returns true if this point is equal to point
        """
        if self.get_x() == point.get_x() and self.get_y() == point.get_y():
            return True
        return False
