import math


class Point:
    """
    Point with associated distance functions

    Attributes
    ----------
    x : float
        The point's x value
    y : float
        The point's y value

    Methods
    -------
    set_x(x_new)
        Sets the x value of the point
    set_y(y_new)
        Sets the y value of the point
    get_x()
        Gets the x value of the point
    get_y()
        Gets the y value of the point
    simple_distance(point)
        Finds the simple distance between this point and another point
    manhattan_distance(point)
        Finds the manhattan distance between this point and another point
    """
    x = 0  # The point's x value
    y = 0  # The point's y value

    def __init__(self, x_init, y_init):
        """
        Point Constructor

        Parameters
        ----------
        self : Point
            The point being constructed
        x_init : float
            The initial x value of this Point
        y_init : float
            The initial x value of this Point
        """
        self.x = x_init
        self.y = y_init

    def set_x(self, x_new):
        """
        Sets the value of x for a point

        Parameters
        ----------
        self : Point
            The point
        x_new
            The new x value of the point
        """
        self.x = x_new

    def set_y(self, y_new):
        """
        Sets the value of y for a point

        Parameters
        ----------
        self : Point
            The point
        y_new
            The new y value of the point
        """
        self.y = y_new

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
        Finds the distance between this point and another point

        Parameters
        ----------
        self : Point
            The initial point
        point : Point
            The point to find the distance between

        Returns
        -------
        float
            The simple distance between this point and another point
        """
        return math.sqrt(math.pow((point.x - self.x), 2) + math.pow((point.y - self.y), 2))

    def manhattan_distance(self, point):
        """
        Finds the manhattan distance between this point and another point

        Parameters
        ----------
        self : Point
            The initial point
        point : Point
            The point to find the distance between

        Returns
        -------
        float
            The manhattan distance between this point and another point
        """
        return abs(self.x - point.x) + abs(self.y - point.y)
