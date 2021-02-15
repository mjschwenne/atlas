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
        in_city = True

        # Loops over every vertex of the region and checks to see if it is in the given City
        for point in self.vertices:
            if not city.is_contained(city, point):
                in_city = False
                break
        return in_city

    def in_city_walls(self, wall):
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
        in_wall = True

        # Loops over every vertex of the region and checks to see if it is in the given Wall
        for point in self.vertices:
            if not wall.is_contained(wall, point):
                in_wall = False
                break
        return in_wall
