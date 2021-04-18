import numpy as np

from src.Backend.Region import Region
from src.Backend.Polygon import Polygon
import random
import math
from src.Backend.Point import Point

_PI = math.pi


def d(p, v_start, v_end):
    """
    Takes in a vector defined by two points and a point and computes a version of the dot product whose sign can
    be used to determine which side of the vector it is on.

    Parameters
    ----------
    p : Point
        A point which we wish to determine which side of the line it is on
    v_start : Point
        Origin of the vector
    v_end : Point
        Destination of the vector

    Returns
    -------
    float
        The result of the formula
    """
    return (p.get_x() - v_start.get_x()) * (v_end.get_y() - v_start.get_y()) - \
           (p.get_y() - v_start.get_y()) * (v_end.get_x() - v_start.get_x())


def normalize_angle(angle):
    """
    Normalizes an angle in radians to be in the -pi to +pi range

    Parameters
    ----------
    angle : float
        The angle to normalize

    Returns
    -------
    float
        The normalized angle
    """
    angle = round(angle, 8)
    while round(angle, 8) > round(math.pi, 8):
        angle -= round(2 * math.pi, 8)
    angle = round(angle, 8)
    while round(angle, 8) < round(-math.pi, 8):
        angle += round(2 * math.pi, 8)
    return round(angle, 8)


class District:
    """
    Region storing a list of Vertices and a District with functions to determine what the Region is in

    Attributes
    ----------
    chaos_level : float
        The amount of 'chaos' or randomness in the generation of the districts, is a value 0-1
    probability_of_empty_space : float
        The amount of empty space in a district, is a value 0-1
    max_building_size:
        The minimum building size

    Methods
    -------
    generate(region, chaos_level, probability_of_empty_space, max_building_size)
        Generates the district
    generate_buildings(region, section, chaos_level, probability_of_empty_space, max_building_size)
        Generates the buildings for a given region and section of region
    set_chaos_level(new_chaos_level)
        Sets the Districts chaos level
    get_chaos_level()
        Returns the districts chaos_level
    set_probability_of_empty_space(new_probability_of_empty_space)
        Sets the Districts probability_of_empty_space
    get_probability_of_empty_space()
        Returns the Districts probability_of_empty_space
    set_max_building_size(new_max_building_size)
        Sets the Districts max_building_size
    get_max_building_size()
        Returns the Districts max_building_size
    """
    def __init__(self):
        """
        District constructor

        """
        self.chaos_level = 0
        self.probability_of_empty_space = 0
        self.max_building_size = 0

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

    def set_max_building_size(self, new_max_building_size):
        """
        Sets the value of 'max_building_size' for a district

        Parameters
        ----------
        new_max_building_size : float
            The new value of 'max_building_size' of the district
        """
        self.max_building_size = new_max_building_size

    def get_max_building_size(self):
        """
        Gets the 'max_building_size' of the district

        Returns
        -------
        float
            The 'max_building_size' of the district
        """
        return self.max_building_size

    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = 0
        for reg in neighbor_regions:
            if isinstance(reg.get_district(), District):
                rating += 1
        if region.in_walls(wall):
            rating -= 100
        return rating

    def generate(self, region, chaos_level, probability_of_empty_space, max_building_size):
        """
        Splits a given region into buildings randomly

        Parameters
        ----------
        chaos_level : float
            The chaos_value for how chaotic the buildings are
        probability_of_empty_space : float
            The amount of empty space to be made
        max_building_size : float
            The minimum building size
        region : Region
            The Region to split into buildings that stores the buildings list
        """
        self.generate_buildings(region, region, chaos_level, probability_of_empty_space, max_building_size)

    def generate_buildings(self, region, section, chaos_level, probability_of_empty_space, max_building_size):
        """
        Splits a given region into buildings randomly

        Parameters
        ----------
        chaos_level : float
            The chaos_value for how chaotic the buildings are
        probability_of_empty_space : float
            The amount of empty space to be made
        max_building_size : float
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

        # Find the random angle of the division from the angle of the edge Ensure the we choose an angle which points
        # into the region and NOT away from it. We will use a formula which is essentially the dot product of the
        # edge vector with a vector from the edge start to the center of the polygon. We then test this value with a
        # point on a known side of the line to see if they match
        center = section.get_center()
        d_c = d(center, max_p1, max_p2)
        # if edge_angle != 0 and round(edge_angle, 8) != round(_PI, 8):
        #     # If the line is not horizontal than (ran_p.get_x() - 1, ran_p.get_y()) is to the left of the line
        #     d_p = d(Point(ran_p.get_x() - 1, ran_p.get_y()), max_p1, max_p2)
        # else:
        #     # If the line is horizontal than (ran_p.get_x(), ran_p.get_y() + 1) is to the left of the line
        #     d_p = d(Point(ran_p.get_x(), ran_p.get_y() + 1), max_p1, max_p2)
        cut_ang = edge_angle - (np.sign(d_c) * math.pi / 2)
        ran_ang = (random.uniform(-self.chaos_level, self.chaos_level) * (math.pi / 12)) + cut_ang

        # Find the random gap width
        gap = max_distance * 0.01 + random.uniform(0, chaos_level) * (max_distance * 0.01)

        # Slit the region into two parts
        parts = section.split(ran_p, normalize_angle(ran_ang), gap)

        for part in parts:
            if round(part.area(), 8) <= max_building_size + \
                    (random.uniform(0, chaos_level) * max_building_size):
                if random.uniform(0, 1) >= probability_of_empty_space and len(part.vertices) > 2:
                    if part.area() > max_building_size * 0.2:
                        region.buildings.append(part)
            else:
                self.generate_buildings(region, part, chaos_level, probability_of_empty_space, max_building_size)


class BasicDistrict(District):
    """
    Region storing a list of Vertices and a District with functions to determine what the Region is in

    Attributes
    ----------
    chaos_level : float
        The amount of 'chaos' or randomness in the generation of the districts, is a value 0-1
    probability_of_empty_space : float
        The amount of empty space in a district, is a value 0-1
    max_building_size:
        The minimum building size

    Methods
    -------
    generate_district(region)
        Generates the district
    generate_buildings(region, section)
        Generates the buildings for a given region and section of region

    """
    def __init__(self, chaos_level, probability_of_empty_space, max_building_size):
        """
        Basic District constructor

        Parameters
        ----------
        chaos_level : float
            The initial value of chaos_level for this district
        probability_of_empty_space : float
            The initial value of chaos_level for this district
        max_building_size : float
            The initial value of max_building_size for this district
        """
        super().__init__()
        self.chaos_level = chaos_level
        self.probability_of_empty_space = probability_of_empty_space
        self.max_building_size = max_building_size

    def generate_district(self, region):
        """
        Generates the buildings for the district within the middle 95% of the area

        Parameters
        ----------
        region : Region
            The region to assign buildings to
        """
        self.generate_buildings(region, region.scale_of_polygon(0.95))

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

        # Find the random angle of the division from the angle of the edge Ensure the we choose an angle which points
        # into the region and NOT away from it. We will use a formula which is essentially the dot product of the
        # edge vector with a vector from the edge start to the center of the polygon. We then test this value with a
        # point on a known side of the line to see if they match
        center = section.get_center()
        d_c = d(center, max_p1, max_p2)
        # if edge_angle != 0 and round(edge_angle, 8) != round(_PI, 8):
        #     # If the line is not horizontal than (ran_p.get_x() - 1, ran_p.get_y()) is to the left of the line
        #     d_p = d(Point(ran_p.get_x() - 1, ran_p.get_y()), max_p1, max_p2)
        # else:
        #     # If the line is horizontal than (ran_p.get_x(), ran_p.get_y() + 1) is to the left of the line
        #     d_p = d(Point(ran_p.get_x(), ran_p.get_y() + 1), max_p1, max_p2)
        cut_ang = edge_angle - (np.sign(d_c) * math.pi / 2)
        ran_ang = (random.uniform(-self.chaos_level, self.chaos_level) * (math.pi / 12)) + cut_ang

        # Find the random gap width
        gap = max_distance * 0.01 + random.uniform(0, self.chaos_level) * (max_distance * 0.01)

        # Slit the region into two parts
        parts = section.split(ran_p, normalize_angle(ran_ang), gap)

        for part in parts:
            if round(part.area(), 8) <= self.max_building_size + \
                    (random.uniform(0, self.chaos_level) * self.max_building_size):
                if random.uniform(0, 1) >= self.probability_of_empty_space and len(part.vertices) > 2:
                    if part.area() > self.max_building_size * 0.2:
                        region.buildings.append(part)
            else:
                self.generate_buildings(region, part)


class Armory(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        if not region.in_walls(wall):
            return -10

        return rating


class Castle(District):
    def generate_district(self, region):
        """
        Generates the buildings for the district

        Parameters
        ----------
        region : Region
            The region to assign buildings to
        """
        # Generate interior polygon used to generate castle structure (is castle walls)
        random.seed()

        wall_polygon = region.scale_of_polygon(1.0 / 2.0)
        move_scale = region.get_perimeter() * 0.03
        wall_polygon.move_polygon_by_center(random.uniform(-move_scale, move_scale),
                                            random.uniform(-move_scale, move_scale))
        region.buildings.append(wall_polygon)

        max_area_poly = wall_polygon.rectangle_inside(wall_polygon.vertices[0], wall_polygon.vertices[1])
        max_area = max_area_poly.area()
        for i in range(1, len(wall_polygon.vertices)):
            v1 = wall_polygon.vertices[i]
            v2 = wall_polygon.vertices[(i + 1) % len(wall_polygon.vertices)]
            new_poly = wall_polygon.rectangle_inside(v1, v2)
            new_area = new_poly.area()
            if new_area > max_area:
                max_area = new_area
                max_area_poly = new_poly

        castle = max_area_poly.scale_of_polygon(2.0 / 3.0)
        castle.move_center_to(wall_polygon.get_center())
        region.buildings.append(castle)

        # Break up exterior buildings
        exterior_polys = region.cut_out_gap_2(wall_polygon, 1.2)
        for p in exterior_polys:
            self.generate_buildings(region, p.scale_of_polygon(0.9), 0.6, 0.2, 50)

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbors, other_regions, wall):
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
        if not region.in_walls(wall):
            return -10
        rating += 100
        return rating


class Cathedral(District):

    def generate_district(self, region):
        """
        Generates the buildings for the district

        Parameters
        ----------
        region : Region
            The region to assign buildings to
        """
        center = region.scale_of_polygon(random.uniform(0.2, 0.3))
        region.buildings.append(center)
        polys = region.cut_out_2(center)
        for e in polys:
            self.generate_buildings(region, e.scale_of_polygon(0.85), 0.5, 0.1, 70)

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        if not region.in_walls(wall):
            return -10

        return rating


class Courtyard(District):

    def generate_district(self, region):
        """
        Generates the buildings for the district

        Parameters
        ----------
        region : Region
            The region to assign buildings to
        """
        center = region.scale_of_polygon(random.uniform(0.04, 0.01))
        region.buildings.append(center)

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        if not region.in_walls(wall):
            return -10
        return rating


class Farmland(District):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = 0

        if region.in_walls(wall):
            return -100

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

        return rating


class Gate(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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
        if not region.in_walls(wall):
            return -10
        return 100


class HousingHigh(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = 0

        if not region.in_walls(wall):
            return -10

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

        return rating


class HousingMid(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = 0

        if not region.in_walls(wall):
            return -10

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

        return rating


class HousingLow(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = 0

        if not region.in_walls(wall):
            return -10

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

        return rating


class Industrial(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = 0

        if not region.in_walls(wall):
            return -10

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

        return rating


class Market(District):

    def generate_district(self, region):
        """
        Generates the buildings for the district

        Parameters
        ----------
        region : Region
            The region to assign buildings to
        """
        random.seed()
        interior_poly = region.scale_of_polygon(random.uniform(0.4, 0.7))
        center_poly = region.scale_of_polygon(random.uniform(0.01, 0.04))
        region.buildings.append(center_poly)
        exterior_parts = region.cut_out_2(interior_poly)
        for e in exterior_parts:
            self.generate_buildings(region, e.scale_of_polygon(0.95), 0.5, 0.1, 30)

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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


        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = 0

        if not region.in_walls(wall):
            return -10

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
    def determine_rating(region, neighbor_regions, wall):
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
        if region.in_walls(wall):
            return -10
        return rating


class Park(District):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        Returns
        -------
        integer
            The rating of the region for the district

        """
        rating = -10
        for reg in neighbor_regions:
            dis = reg.get_district()
            if isinstance(dis, HousingHigh):
                rating += 10
            elif isinstance(dis, HousingLow):
                rating -= 10
            elif isinstance(dis, Slum):
                rating -= 10
            elif isinstance(dis, Industrial):
                rating -= 10

        return rating


class Precinct(District):

    def generate_district(self, region):
        """
        Generates the buildings for the district

        Parameters
        ----------
        region : Region
            The region to assign buildings to
        """
        center = region.scale_of_polygon(random.uniform(0.2, 0.3))
        move_scale = region.get_perimeter() * 0.03
        center.move_polygon_by_center(random.uniform(-move_scale, move_scale),
                                      random.uniform(-move_scale, move_scale))
        region.buildings.append(center)
        polys = region.cut_out_2(center)
        for e in polys:
            self.generate_buildings(region, e.scale_of_polygon(0.8), 0.4, 0.2, 50)

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, other_regions, wall):
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

        Returns
        -------
        integer
            The rating of the region for the district
        """
        precincts = 0
        for reg in other_regions:
            if region != reg:
                if isinstance(reg.get_district(), Precinct):
                    precincts += 1

        if precincts >= 2:
            return -10

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
                rating += -50
        if not region.in_walls(wall):
            return -10
        return rating


class Shops(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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

        if not region.in_walls(wall):
            return -10

        return rating


class Slum(BasicDistrict):

    # Overrides District's determine Rating
    @staticmethod
    def determine_rating(region, neighbor_regions, wall):
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
