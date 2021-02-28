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
                    if isinstance(reg.get_district(), District):
                        rating += 1
        if region.in_city(city):
            rating -= 100
        if region.in_walls(wall):
            rating -= 100
        return rating

    def generate_district(self):
        pass


class Armory(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Farmland):
                        rating += 0
                    elif isinstance(dis, Housing):
                        rating += -20
                    elif isinstance(dis, Smithing):
                        rating += 30
                    elif isinstance(dis, Docks):
                        rating += 10
                    elif isinstance(dis, Cathedral):
                        rating += -10
                    elif isinstance(dis, Castle):
                        rating += 20
                    elif isinstance(dis, Slum):
                        rating += 20
                    elif isinstance(dis, Armory):
                        rating += -20
                    elif isinstance(dis, Precinct):
                        rating += 10
                    elif isinstance(dis, WarCamp):
                        rating += 40
        return rating


class Castle(District):

    # Overrides District's determine Rating
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
                if isinstance(reg.get_district(), Castle):
                    return -10000
                if region.is_bordering(reg):
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += 20
                    elif isinstance(dis, Cathedral):
                        rating += 30
                    elif isinstance(dis, Gate):
                        rating += 10
                    elif isinstance(dis, Slum):
                        rating += -1000
                    elif isinstance(dis, Armory):
                        rating += 20
                    elif isinstance(dis, Market):
                        rating += 10
                    elif isinstance(dis, Precinct):
                        rating += 10
                    elif isinstance(dis, WarCamp):
                        rating += -100
        if region.in_walls(wall):
            rating += 1000
        return rating


class Cathedral(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += 20
                    elif isinstance(dis, Smithing):
                        rating += -10
                    elif isinstance(dis, Market):
                        rating += 10
                    elif isinstance(dis, Cathedral):
                        rating += -100
                    elif isinstance(dis, Castle):
                        rating += 30
                    elif isinstance(dis, Slum):
                        rating += -10
                    elif isinstance(dis, Armory):
                        rating += -10
                    elif isinstance(dis, Precinct):
                        rating += -10
                    elif isinstance(dis, WarCamp):
                        rating += -10
        if region.in_city(city):
            rating += 20
        if region.in_walls(wall):
            rating += 100
        return rating


class Docks(District):

    # Overrides District's determine Rating
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
        if (not region.get_is_water()) and (not region.get_has_river()):
            return -1000
        for reg in other_regions:
            if region != reg:
                if region.is_bordering(reg):
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += 20
                    elif isinstance(dis, Smithing):
                        rating += 20
                    elif isinstance(dis, Market):
                        rating += 30
                    elif isinstance(dis, Docks):
                        rating += 40
                    elif isinstance(dis, Slum):
                        rating += 10
                    elif isinstance(dis, Armory):
                        rating += 10
                    elif isinstance(dis, Precinct):
                        rating += 10
                    elif isinstance(dis, WarCamp):
                        rating += 10
        if region.in_walls(wall):
            rating -= 100
        return rating


class Farmland(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Farmland):
                        rating += 50
                    elif isinstance(dis, Housing):
                        rating += 10
                    elif isinstance(dis, Market):
                        rating += 10
                    elif isinstance(dis, Precinct):
                        rating -= 10
        if region.in_city(city):
            rating -= 100
        if region.in_walls(wall):
            rating -= 1000
        return rating


class Gate(District):

    # Overrides District's determine Rating
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
        on_gate = False
        for ver in wall.get_gates():
            if region.is_contained(ver):
                on_gate = True
                break
        if not on_gate:
            return -1000
        for reg in other_regions:
            if region != reg:
                if region.is_bordering(reg):
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += 20
                    elif isinstance(dis, Market):
                        rating += 10
                    elif isinstance(dis, Castle):
                        rating += 10
                    elif isinstance(dis, WarCamp):
                        rating += 20
        return rating


class Housing(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Farmland):
                        rating += 10
                    elif isinstance(dis, Housing):
                        rating -= 20
                    elif isinstance(dis, Smithing):
                        rating += 30
                    elif isinstance(dis, Market):
                        rating += 20
                    elif isinstance(dis, Docks):
                        rating += 20
                    elif isinstance(dis, Cathedral):
                        rating += 20
                    elif isinstance(dis, Castle):
                        rating += 20
                    elif isinstance(dis, Gate):
                        rating += 20
                    elif isinstance(dis, Slum):
                        rating += -10
                    elif isinstance(dis, Armory):
                        rating += -20
                    elif isinstance(dis, Precinct):
                        rating += 20
                    elif isinstance(dis, WarCamp):
                        rating += -40
        return rating


class Market(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += 20
                    elif isinstance(dis, Smithing):
                        rating += 20
                    elif isinstance(dis, Market):
                        rating += 20
                    elif isinstance(dis, Docks):
                        rating += 30
                    elif isinstance(dis, Cathedral):
                        rating += 10
                    elif isinstance(dis, Castle):
                        rating += 10
                    elif isinstance(dis, Gate):
                        rating += 10
                    elif isinstance(dis, Slum):
                        rating += -10
                    elif isinstance(dis, WarCamp):
                        rating += -50
        if region.in_city(city):
            rating += 10
        if region.in_walls(wall):
            rating += 30
        return rating


class Precinct(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Farmland):
                        rating += -10
                    elif isinstance(dis, Housing):
                        rating += 20
                    elif isinstance(dis, Smithing):
                        rating += 10
                    elif isinstance(dis, Docks):
                        rating += 10
                    elif isinstance(dis, Cathedral):
                        rating += -10
                    elif isinstance(dis, Castle):
                        rating += 10
                    elif isinstance(dis, Slum):
                        rating += 30
                    elif isinstance(dis, Armory):
                        rating += 10
                    elif isinstance(dis, Precinct):
                        rating += -50
                    elif isinstance(dis, WarCamp):
                        rating += -20
        if region.in_city(city):
            rating += 20
        if region.in_walls(wall):
            rating += 40
        return rating


class Slum(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += -10
                    elif isinstance(dis, Smithing):
                        rating += -10
                    elif isinstance(dis, Market):
                        rating += -10
                    elif isinstance(dis, Docks):
                        rating += 10
                    elif isinstance(dis, Cathedral):
                        rating += -10
                    elif isinstance(dis, Castle):
                        rating += -1000
                    elif isinstance(dis, Slum):
                        rating += 40
                    elif isinstance(dis, Armory):
                        rating += 20
                    elif isinstance(dis, Precinct):
                        rating += 30
                    elif isinstance(dis, WarCamp):
                        rating += 30
        if region.in_walls(wall):
            rating += -100
        return rating


class Smithing(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += 30
                    elif isinstance(dis, Market):
                        rating += 20
                    elif isinstance(dis, Docks):
                        rating += 20
                    elif isinstance(dis, Cathedral):
                        rating += -10
                    elif isinstance(dis, Slum):
                        rating += -10
                    elif isinstance(dis, Armory):
                        rating += 30
                    elif isinstance(dis, Precinct):
                        rating += 10
        if region.in_city(city):
            rating += 20
        if region.in_walls(wall):
            rating += 20
        return rating


class WarCamp(District):

    # Overrides District's determine Rating
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
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += -40
                    elif isinstance(dis, Market):
                        rating += -50
                    elif isinstance(dis, Docks):
                        rating += 10
                    elif isinstance(dis, Cathedral):
                        rating += -50
                    elif isinstance(dis, Castle):
                        rating += -100
                    elif isinstance(dis, Gate):
                        rating += 20
                    elif isinstance(dis, Slum):
                        rating += 30
                    elif isinstance(dis, Armory):
                        rating += 40
                    elif isinstance(dis, Precinct):
                        rating += -20
                    elif isinstance(dis, WarCamp):
                        rating += 100
        if region.in_city(city):
            rating -= 100
        if region.in_walls(wall):
            rating -= 1000
        return rating
