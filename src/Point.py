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
        Sets the y value of the point.
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
            The initial x value of this Point.
        y : float
            The initial x value of this Point.
        """
        self.x = x
        self.y = y

    def set_x(self, x_new):
        """
        Sets the value of `x` for a point.

        Parameters
        ----------
        x_new : float
            The new `x` value of the point.
        """
        self.x = x_new

    def get_x(self):
        """
        Fetch the value of `x`.

        Returns
        -------
        float:
            `x`-coordinate of this Point.
        """
        return self.x

    def set_y(self, y_new):
        """
        Sets the value of `y` for a point.

        Parameters
        ----------
        y_new
            The new `y` value of the point.
        """
        self.y = y_new

    def get_y(self):
        """
        Fetch the value of `y`.

        Returns
        -------
        float:
            `y`-coordinate of this Point.
        """
        return self.y

    def simple_distance(self, point):
        """
        Finds the distance between this point and another point.

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
        return math.sqrt(math.pow((point.x - self.x), 2) + math.pow((point.y - self.y), 2))

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
