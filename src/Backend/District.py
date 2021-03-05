from src.Backend.Region import Region
from src.Backend.Polygon import Polygon
import random
import math
from src.Backend.Point import Point

_PI = math.pi


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


class BasicDistrict(District):

    def generate_district(self, region):
        self.generate_buildings(region, region)

    def generate_buildings(self, region, section):
        """
        Splits a given region into buildings randomly

        Parameters
        ----------
        region : Region
            The Region to split into buildings that stores the buildings list
        section : Polygon
            The possibly not Region Polygon that needs to be split
        """
        max_p1 = section.vertices[0]
        max_p2 = section.vertices[1]
        max_distance = max_p1.simple_distance(max_p2)

        # finds the longest length on an edge of the section
        for i in range(0, (len(section.vertices) - 1)):
            p1 = section.vertices[i]
            p2 = section.vertices[i + 1]
            distance = p1.simple_distance(p2)
            if max_distance < distance:
                max_distance = distance
                max_p1 = p1
                max_p2 = p2

        # find the angle of the edge
        if max_p1.get_x() == max_p2.get_x():
            edge_angle = _PI / 2
        elif max_p1.get_y() == max_p2.get_y():
            edge_angle = _PI
        elif max_p1.get_y() > max_p2.get_y():
            help_p = Point(max_p1.get_x(), max_p2.get_y())
            c = max_p2.simple_distance(max_p1)
            a = max_p1.simple_distance(help_p)
            edge_angle = math.sin(a / c)
        elif max_p1.get_y() < max_p2.get_y():
            help_p = Point(max_p2.get_x(), max_p1.get_y())
            c = max_p1.simple_distance(max_p2)
            a = max_p2.simple_distance(help_p)
            edge_angle = math.sin(a / c)

        random.seed()
        ran_p = Point(0, 0)

        # Finds a random value informed by chaos_level (when chaos is 0 it will always be half)
        cut_rand = random.uniform((1 - (0.5 * self.chaos_level + 0.5)), (0.5 * self.chaos_level + 0.5))

        # Finds a random point on the edge (using cut_rand) to cut the edge at.
        if max_p1.get_x() != max_p2.get_x():
            ran_p.set_x((max_p2.get_x() - max_p1.get_x()) * cut_rand + max_p1.get_x())
            ran_p.set_y(((max_p2.get_y() - max_p1.get_y()) / (max_p2.get_x() - max_p1.get_x())) *
                        (ran_p.get_x() - max_p1.get_x()) + max_p1.get_y())
        # If the line is vertical
        else:
            ran_p.set_x(max_p1.get_x())
            ran_p.set_y((max_p2.get_y() - max_p1.get_y()) * cut_rand + max_p1.get_y())

        # Find the random angle of the division from the angle of the edge
        cut_ang = edge_angle + math.pi / 2
        ran_ang = (random.uniform(-self.chaos_level, self.chaos_level) * (math.pi / 12)) + cut_ang

        # Slit the region into two parts
        parts = section.split(ran_p, ran_ang)

        for part in parts:
            if part.area() <= self.min_building_size + (random.uniform(0, self.chaos_level) * self.min_building_size):
                # if random.random() < self.probability_of_empty_space:
                region.buildings.append(part)
            else:
                self.generate_buildings(region, part)


class Armory(BasicDistrict):

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
            return -1000
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
            return -1000
        return rating
