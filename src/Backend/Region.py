from src.Backend.Polygon import Polygon


class Region(Polygon):
    """
    Region storing a list of Vertices and a District with functions to determine what the Region is in

    Attributes
    ----------
    district : District
        The district of the Region
    vertices : list of Points
        The points that define the boarders of the Region

    Methods
    -------
    get_district()
        Gets the district value of the Region
    set_district(new_district)
        Sets the district value of the Region
    get_vertices()
        Gets the vertices value of the Region
    set_vertices(new_vertices)
        Sets the vertices value of the Region
    in_city(city)
        Determines if the Region is inside the provided City
    in_wall(wall)
        Determines if the Region is inside the provided wall

    """

    def __init__(self, district, vertices):
        """
        Region constructor

        Parameters
        ----------
        district : District
            The initial value of 'district' for this region
        vertices : List of Points
            The vertices that define the boundaries of the region/polygon
        """
        super().__init__(vertices)
        self.district = district

    def get_district(self):
        """
        Gets the 'district' of the region

        Returns
        -------
        district
            The 'district' of the region
        """
        return self.district

    def set_district(self, new_district):
        """
        Sets the value of 'district' for a region

        Parameters
        ----------
        new_district : district
            The new value of 'district' of the region
        """
        self.district = new_district

    def set_vertices(self, new_vertices):
        """
        Sets the value of 'vertices' for a Region

        Parameters
        ----------
        new_vertices : List of Points
            The new value of 'vertices' for the Region
        """
        self.vertices = new_vertices

    def get_vertices(self):
        """
        Gets the 'vertices' of a Region

        Returns
        -------
        list of Points
            Returns the 'vertices' of the Region
        """
        return self.vertices

    def in_city(self, city):
        """
        Determines if a Region is inside of the given City

        Parameters
        ----------
        city : Polygon
            The City to check if the Region is inside of

        Returns
        -------
        bool
            True if the Region is inside the City, false otherwise
        """

        # Loops over every vertex of the region and checks to see if it is in the given City
        for point in self.vertices:
            if not city.is_contained(point):
                return False
        return True

    def in_walls(self, wall):
        """
        Determines if a Region is inside of the given Wall

        Parameters
        ----------
        wall : Wall
            The wall to check if the Region is inside of

        Returns
        -------
        bool
            True if the Region is inside the wall, false otherwise
        """

        # Loops over every vertex of the region and checks to see if it is in the given Wall
        for point in self.vertices:
            if not wall.is_contained(point):
                return False
        return True
