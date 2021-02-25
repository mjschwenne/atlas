from src.Backend.Region import Region
class District:

    def __init__(self, chaos_level, probability_of_empty_space, min_building_size):
        """
        District constructor

        Parameters
        ----------
        chaos_level : float
            The initial value of chaos_level for this district
        probability_of_empty_space : float
            The initial value of chaos_level for this district
        min_building_size : float
            The initial value of min_building_size for this district
        """
        self.chaos_level = chaos_level
        self.probability_of_empty_space = probability_of_empty_space
        self.min_building_size = min_building_size

    def set_chaos_level(self, new_chaos_level):
        """
        Sets the value of 'chaos_level' for a district

        Parameters
        ----------
        new_chaos_level : float
            The new value of 'chaos_level' of the district
        """
        self.chaos_level = new_chaos_level

    def get_chaos_level(self):
        """
        Gets the 'chaos_level' of the district

        Returns
        -------
        float
            The 'chaos_level' of the district
        """
        return self.chaos_level

    def set_probability_of_empty_space(self, new_probability_of_empty_space):
        """
        Sets the value of 'probability_of_empty_space' for a district

        Parameters
        ----------
        new_probability_of_empty_space : float
            The new value of 'probability_of_empty_space' of the district
        """
        self.probability_of_empty_space = new_probability_of_empty_space

    def get_probability_of_empty_space(self):
        """
        Gets the 'probability_of_empty_space' of the district

        Returns
        -------
        float
            The 'probability_of_empty_space' of the district
        """
        return self.probability_of_empty_space

    def set_min_building_size(self, new_min_building_size):
        """
        Sets the value of 'min_building_size' for a district

        Parameters
        ----------
        new_min_building_size : float
            The new value of 'min_building_size' of the district
        """
        self.min_building_size = new_min_building_size

    def get_min_building_size(self):
        """
        Gets the 'min_building_size' of the district

        Returns
        -------
        float
            The 'min_building_size' of the district
        """
        return self.min_building_size

    @staticmethod
    def determine_rating(region, other_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        other_regions : List of Regions
            Every other region
        wall : Wall
            The wall of the city
        city : Polygon
            The Polygon Representing the City

        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = 0
        for reg in other_regions:
            if region != reg:
                if region.is_bordering(reg):
                    if Region.isinstance(reg.get_district()):
                        rating += 1
        if region.in_city(city):
            rating -= 100
        if region.in_walls(wall):
            rating -= 100
        return rating

    def generate_district(self):
        pass
