from src.Polygon import Polygon


class Wall(Polygon):

    def __init__(self, vertices, gates):
        """
        Constructor for Wall

        Parameters
        ----------
        vertices : List of Points
            The vertices that define the Wall/Polygon
        gates : List of Points
            The vertices that define where gates are on the wall
        """
        super().__init__(vertices)
        self.gates = gates

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

    def create_wall(self):
        pass
