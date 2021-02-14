from src.Polygon import Polygon


class Region(Polygon):

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

    def in_city(self):
        pass

    def in_city_walls(self, wall):
        """
        Determines if a Region is inside of the given Wall

        Parameters
        ----------
        wall : Wall
            The to check if the Region is inside of

        Returns
        -------
        bool
            True if the Region is inside the wall, false otherwise
        """
        in_wall = True
        for point in self.vertices:
            if not wall.is_contained(wall, point):
                in_wall = False
                break
        return in_wall
