import random
import math
from src.Backend.Point import Point
from src.Backend.Polygon import Polygon

_PI = math.pi


class DistrictGeneration:
    @staticmethod
    def create_buildings(region, chaos_level, probability_of_empty_space, min_building_size):
        """
        Splits a given region into buildings randomly

        Parameters
        ----------
        region : Region
            The Region to split into buildings
        chaos_level : float
            A float from 0 to 1 that indicates how random/chaotic the region will be (0 is the most normal, 1 is the
            most chaotic)
        probability_of_empty_space : float
            A float from 0 to 1 that indicates how likely there is to be empty space in the region (0 is impossible and
            1 is 100% clear space)
        min_building_size : float
            The area around which the smallest building will be.
        """
        max_p1 = region.vertices[0]
        max_p2 = region.vertices[1]
        max_distance = max_p1.simple_distance(max_p2)

        # finds the longest length on an edge of the region
        for i in range(0, (len(region.vertices) - 1)):
            p1 = region.vertices[i]
            p2 = region.vertices[i + 1]
            distance = p1.simple_distance(p2)
            if max_distance < distance:
                max_distance = distance
                max_p1 = p1
                max_p2 = p2

        # find the angle of the edge
        if max_p1.get_y() > max_p2.get_y():
            help_p = Point(max_p1.get_x(), max_p2.get_y())
            c = max_p2.simple_distance(max_p1)
            a = max_p1.simple_distance(help_p)
            edge_angle = math.sin(a / c)
        elif max_p1.get_y() < max_p2.get_y():
            help_p = Point(max_p2.get_x(), max_p1.get_y())
            c = max_p1.simple_distance(max_p2)
            a = max_p2.simple_distance(help_p)
            edge_angle = math.sin(a / c)
        elif max_p1.get_x == max_p2.get_x():
            edge_angle = _PI / 2
        else:
            edge_angle = _PI

        random.seed()
        ran_p = Point(0, 0)

        # Finds a random value informed by chaos_level
        cut_rand = random.uniform((1 - chaos_level), (0.5 * chaos_level + 0.5))

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
        ran_ang = random.uniform(-((_PI / 2) + ((chaos_level / 36) * _PI)),
                                 ((_PI / 2) + ((chaos_level / 36) * _PI))) + edge_angle

        # Slit the region into two parts
        parts = region.cut(ran_p, ran_ang)

        # For each part
        for part in parts:
            if part.area() < min_building_size + (random.uniform(0, chaos_level) * min_building_size):
                if random.random() < probability_of_empty_space:
                    region.buildings.append(part)
            else:
                DistrictGeneration.create_buildings(part, chaos_level, probability_of_empty_space, min_building_size)
