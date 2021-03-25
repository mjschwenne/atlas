from src.Backend.Region import Region
from src.Backend.Polygon import Polygon
import random
import math
from src.Backend.Point import Point

_PI = math.pi


class District:

    def __init__(self):
        """
        District constructor

        """
        self.chaos_level = 0
        self.probability_of_empty_space = 0
        self.min_building_size = 0

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
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            if isinstance(reg.get_district(), District):
                rating += 1
        if region.in_city(city):
            rating -= 100
        if region.in_walls(wall):
            rating -= 100
        return rating

    def generate_buildings(self, region, section, chaos_level, probability_of_empty_space, min_building_size):
        """
        Splits a given region into buildings randomly

        Parameters
        ----------
        chaos_level : float
            The chaos_value for how chaotic the buildings are
        probability_of_empty_space : float
            The amount of empty space to be made
        min_building_size : float
            The minimum building size
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
        edge_angle = math.atan2((max_p2.get_y() - max_p1.get_y()), (max_p2.get_x() - max_p1.get_x()))

        random.seed()
        ran_p = Point(0, 0)

        # Finds a random value informed by chaos_level (when chaos is 0 it will always be half)
        cut_rand = random.uniform((1 - (0.5 * chaos_level + 0.5)), (0.5 * chaos_level + 0.5))

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
        ran_ang = (random.uniform(-chaos_level, chaos_level) * (math.pi / 12)) + cut_ang

        # Find the random gap width
        gap = max_distance * 0.01 + random.uniform(0, chaos_level) * (max_distance * 0.01)

        # Slit the region into two parts
        parts = section.split(ran_p, ran_ang, gap)

        for part in parts:
            if round(part.area(), 8) <= min_building_size + \
                    (random.uniform(0, chaos_level) * min_building_size):
                if random.uniform(0, 1) >= probability_of_empty_space and len(part.vertices) > 2:
                    if part.area() > min_building_size * 0.2:
                        region.buildings.append(part)
            else:
                self.generate_buildings(region, part, chaos_level, probability_of_empty_space, min_building_size)

class BasicDistrict(District):

    def __init__(self, chaos_level, probability_of_empty_space, min_building_size):
        """
        Basic District constructor

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
        edge_angle = math.atan2((max_p2.get_y() - max_p1.get_y()), (max_p2.get_x() - max_p1.get_x()))

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

        # Find the random gap width
        gap = max_distance * 0.01 + random.uniform(0, self.chaos_level) * (max_distance * 0.01)

        # Slit the region into two parts
        parts = section.split(ran_p, ran_ang, gap)

        for part in parts:
            if round(part.area(), 8) <= self.min_building_size + \
                    (random.uniform(0, self.chaos_level) * self.min_building_size):
                if random.uniform(0, 1) >= self.probability_of_empty_space and len(part.vertices) > 2:
                    if part.area() > self.min_building_size * 0.2:
                        region.buildings.append(part)
            else:
                self.generate_buildings(region, part)


class Armory(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += -10
            elif isinstance(dis, Industrial):
                rating += 20
            elif isinstance(dis, Shops):
                rating += 10
            elif isinstance(dis, Armory):
                rating += -10
            elif isinstance(dis, Cathedral):
                rating += -10
            elif isinstance(dis, Castle):
                rating += 20
            elif isinstance(dis, Precinct):
                rating += 10

        if region.in_walls(wall):
            rating += 10
        if region.in_city(city):
            rating += 10

        return rating


class Castle(District):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbors, other_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        neighbors : list of Regions
            the neighboring regions
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
                    return -1000
        for reg in neighbors:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += 10
            elif isinstance(dis, HousingLow):
                rating += -10
            elif isinstance(dis, Industrial):
                rating += -100
            elif isinstance(dis, Shops):
                rating += 20
            elif isinstance(dis, Slum):
                rating += -100
            elif isinstance(dis, Armory):
                rating += 20
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += 30
            elif isinstance(dis, Precinct):
                rating += 10
            elif isinstance(dis, Courtyard):
                rating += 10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_walls(wall):
            rating += 200
        return rating


class Cathedral(District):

    def generate_district(self, region):
        average_side_length = region.get_perimeter()/len(region.vertices)
        center = region.get_center()
        points = []
        for point in region.vertices:
            if center.get_x() - point.get_x() > 0:
                new_x = point.get_x() + average_side_length*0.25
            else:
                new_x = point.get_x() - average_side_length*0.25
            if center.get_y() - point.get_y() > 0:
                new_y = point.get_y() + average_side_length*0.25
            else:
                new_y = point.get_y() - average_side_length*0.25
            points.append(Point(new_x, new_y))

        polys = []


    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += 10
            elif isinstance(dis, HousingMid):
                rating += 10
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Industrial):
                rating += -50
            elif isinstance(dis, Shops):
                rating += 30
            elif isinstance(dis, Slum):
                rating += -10
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += -50
            elif isinstance(dis, Castle):
                rating += 30
            elif isinstance(dis, Courtyard):
                rating += 10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_city(city):
            rating += 10
        if region.in_walls(wall):
            rating += 20
        return rating


class Courtyard(District):

    def generate_district(self, region):
            center = region.get_center()
            points = []
            for point in region.vertices:
                length = center.get_x() - point.get_x()
                if length > 0:
                    new_x = center.get_x() - abs((length * 0.25))
                else:
                    new_x = center.get_x() + abs((length * 0.25))
                length = center.get_y() - point.get_y()
                if length > 0:
                    new_y = center.get_y() - abs((length * 0.25))
                else:
                    new_y = center.get_y() + abs((length * 0.25))
                points.append(Point(new_x, new_y))

            region.buildings.append(Polygon(points))

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingLow):
                rating += -10
            elif isinstance(dis, Industrial):
                rating += 30
            elif isinstance(dis, Shops):
                rating += 10
            elif isinstance(dis, Slum):
                rating += -30
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += 10
            elif isinstance(dis, Castle):
                rating += 10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_city(city):
            rating += 10
        if region.in_walls(wall):
            rating += 20
        return rating


class Farmland(District):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingLow):
                rating += 10
            elif isinstance(dis, Industrial):
                rating += 10
            elif isinstance(dis, Slum):
                rating += 10
            elif isinstance(dis, Farmland):
                rating += 20
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_city(city):
            rating -= 20
        if region.in_walls(wall):
            return -10
        return rating


class Gate(District):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        on_gate = False
        for ver in wall.get_gates():
            if region.is_contained(ver):
                on_gate = True
                break
        if not on_gate:
            return -10
        return 100


class HousingHigh(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += 30
            elif isinstance(dis, HousingMid):
                rating += 20
            elif isinstance(dis, HousingLow):
                rating += -10
            elif isinstance(dis, Industrial):
                rating += -20
            elif isinstance(dis, Shops):
                rating += 20
            elif isinstance(dis, Slum):
                rating += -100
            elif isinstance(dis, Armory):
                rating += -10
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += 10
            elif isinstance(dis, Castle):
                rating += 10
            elif isinstance(dis, Openland):
                rating += -10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_city(city):
            rating += 30
        if region.in_walls(wall):
            rating += 50
        return rating


class HousingMid(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += 20
            elif isinstance(dis, HousingMid):
                rating += 20
            elif isinstance(dis, Industrial):
                rating += -10
            elif isinstance(dis, Shops):
                rating += 20
            elif isinstance(dis, Slum):
                rating += -50
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += 10
            elif isinstance(dis, Openland):
                rating += -10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_city(city):
            rating += 30
        if region.in_walls(wall):
            rating += 20
        return rating


class HousingLow(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += -10
            elif isinstance(dis, HousingLow):
                rating += 20
            elif isinstance(dis, Industrial):
                rating += 10
            elif isinstance(dis, Farmland):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += 10
            elif isinstance(dis, Castle):
                rating += -20
            elif isinstance(dis, Openland):
                rating += -20
            elif isinstance(dis, Precinct):
                rating += 10
        if region.in_city(city):
            rating += 30
        return rating


class Industrial(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += -20
            elif isinstance(dis, HousingMid):
                rating += -10
            elif isinstance(dis, HousingLow):
                rating += 10
            elif isinstance(dis, Slum):
                rating += 30
            elif isinstance(dis, Armory):
                rating += 20
            elif isinstance(dis, Farmland):
                rating += 10
            elif isinstance(dis, Market):
                rating += -10
            elif isinstance(dis, Cathedral):
                rating += -50
            elif isinstance(dis, Castle):
                rating += -100
            elif isinstance(dis, Precinct):
                rating += 10
            elif isinstance(dis, Courtyard):
                rating += -30
            elif isinstance(dis, Openland):
                rating += 20
            elif isinstance(dis, Park):
                rating += -30
        if region.in_walls(wall):
            rating += -30
        return rating


class Market(District):

    def generate_district(self, region):
        center = region.get_center()
        points = []
        for point in region.vertices:
            length = center.get_x() - point.get_x()
            if length > 0:
                new_x = center.get_x() - abs((length * 0.65))
            else:
                new_x = center.get_x() + abs((length * 0.65))
            length = center.get_y() - point.get_y()
            if length > 0:
                new_y = center.get_y() - abs((length * 0.65))
            else:
                new_y = center.get_y() + abs((length * 0.65))
            points.append(Point(new_x, new_y))

        new_poly = Polygon(points)
        self.generate_buildings(region, new_poly, 0.5, 0.05, 100)


    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += 10
            elif isinstance(dis, HousingLow):
                rating += 10
            elif isinstance(dis, Market):
                rating += 20
            elif isinstance(dis, Industrial):
                rating += -10
            elif isinstance(dis, Shops):
                rating += 20
            elif isinstance(dis, Farmland):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += 10
            elif isinstance(dis, Castle):
                rating += 10
            elif isinstance(dis, Precinct):
                rating += 10
            elif isinstance(dis, Openland):
                rating += 10
            elif isinstance(dis, Gate):
                rating += 10
        return rating


class Openland(District):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += -10
            elif isinstance(dis, HousingMid):
                rating += -10
            elif isinstance(dis, HousingLow):
                rating += -10
            elif isinstance(dis, Industrial):
                rating += 20
            elif isinstance(dis, Slum):
                rating += -40
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Openland):
                rating += 10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_city(city):
            rating += -40
        if region.in_walls(wall):
            rating += -100
        return rating


class Park(District):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += 10
            elif isinstance(dis, HousingMid):
                rating += 10
            elif isinstance(dis, Industrial):
                rating += -30
            elif isinstance(dis, Shops):
                rating += 10
            elif isinstance(dis, Slum):
                rating += -10
            elif isinstance(dis, Farmland):
                rating += 10
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += 10
            elif isinstance(dis, Castle):
                rating += 10
            elif isinstance(dis, Openland):
                rating += 10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_city(city):
            rating += 10
        if region.in_walls(wall):
            rating += -50
        return rating


class Precinct(District):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingLow):
                rating += 10
            elif isinstance(dis, Shops):
                rating += 10
            elif isinstance(dis, Slum):
                rating += 20
            elif isinstance(dis, Armory):
                rating += 10
            elif isinstance(dis, Market):
                rating += 10
            elif isinstance(dis, Castle):
                rating += 10
            elif isinstance(dis, Precinct):
                rating += -10
        if region.in_city(city):
            rating += 10
        if region.in_walls(wall):
            rating += 10
        return rating


class Shops(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += 20
            elif isinstance(dis, HousingMid):
                rating += 20
            elif isinstance(dis, Shops):
                rating += 20
            elif isinstance(dis, Slum):
                rating += -20
            elif isinstance(dis, Armory):
                rating += 10
            elif isinstance(dis, Market):
                rating += 20
            elif isinstance(dis, Cathedral):
                rating += 30
            elif isinstance(dis, Castle):
                rating += 20
            elif isinstance(dis, Courtyard):
                rating += 10
            elif isinstance(dis, Park):
                rating += 10
        if region.in_city(city):
            rating += 20
        if region.in_walls(wall):
            rating += 30
        return rating


class Slum(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall, city):
        """
        Determines the likely hood a given district will be in a region

        Parameters
        ----------
        region : Region
            The region that we are determining the likely hood the district will be in
        neighbor_regions : List of Regions
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
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += -100
            elif isinstance(dis, HousingMid):
                rating += -50
            elif isinstance(dis, Industrial):
                rating += 30
            elif isinstance(dis, Shops):
                rating += -20
            elif isinstance(dis, Slum):
                rating += 20
            elif isinstance(dis, Farmland):
                rating += 10
            elif isinstance(dis, Cathedral):
                rating += -10
            elif isinstance(dis, Castle):
                rating += -100
            elif isinstance(dis, Precinct):
                rating += 20
            elif isinstance(dis, Courtyard):
                rating += -30
            elif isinstance(dis, Openland):
                rating += -40
            elif isinstance(dis, Park):
                rating += -10
        if region.in_walls(wall):
            rating += -40
        return rating

