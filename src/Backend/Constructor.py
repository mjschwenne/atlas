import random
from datetime import datetime

from src.Backend.District import *
from src.Backend.Voronoi import Voronoi
from src.Backend.Infrastructure import Infrastructure


class Constructor:
    """
    The constructor handles the compilation and processing of information from the backend and the transition of that
    information into something that the front end can handle

    Methods
    -------
    generate_map(options)
        Generates a map
    assign_districts(regions, wall, city)
        Assigns the provided regions a district
    assign_district(reg, regions, wall, city)
        Assigns the region a district

    """

    def generate_map(self, options):
        print(datetime.now())
        bounding_polygon = Polygon([Point(250, 250), Point(250, -250), Point(-250, -250), Point(-250, 250)])
        num_district = 10
        var1 = options[0]
        if var1 == 2:
            num_district = 25
        elif var1 == 3:
            num_district = 50
        elif var1 == 4:
            num_district = 75
        elif var1 == 5:
            num_district = 100
        vor = Voronoi(num_district, bounding_polygon)
        vor.relax()
        vor.relax()

        polygons = vor.polygons
        regions = []
        for poly in polygons:
            regions.append(Region(None, poly.get_vertices(), False, False))
        for reg in regions:
            reg.find_neighbors(regions)
        wall = Infrastructure(regions, vor.graph, bounding_polygon)
        wall2 = Infrastructure(regions, vor.graph, bounding_polygon)
        city = Polygon(wall2.get_vertices())
        self.assign_districts(regions, wall, city, options)
        if options[2] == 1:
            for reg in regions:
                if isinstance(reg.get_district(), BasicDistrict):
                    reg.get_district().generate_district(reg)
                elif isinstance(reg.get_district(), Courtyard):
                    reg.get_district().generate_district(reg)
                elif isinstance(reg.get_district(), Market):
                    reg.get_district().generate_district(reg)
                # elif isinstance(reg.get_district(), Cathedral):
                #    reg.get_district().generate_district(reg)
        print(datetime.now())
        return regions

    @staticmethod
    def assign_districts(regions, wall, city, options):
        """
        Assigns the provided regions a district at sudo-random order, taking into account the wall and city bounds

        Parameters
        ----------
        options : List of ints
            Option input from user
        regions : List of regions
            Regions to have districts assigned
        wall : Infrastructure
            The wall of the city
        city : Polygon
            The polygon representing the city bounds
        """

        # Clears out the previously stored regions if any
        for reg in regions:
            reg.set_district(None)

        # Assigns a district to each Region
        for reg in regions:
            Constructor.assign_district(reg, regions, wall, city, options)

        # Loops over the districts to ensure valid placement at every location until all assignments are valid
        change = True
        while change:
            change = False
            for reg in regions:
                neighbors = reg.get_neighbors()
                if isinstance(reg.get_district(), Castle):
                    rating = reg.get_district().determine_rating(reg, neighbors, regions, wall, city)
                else:
                    rating = reg.get_district().determine_rating(reg, neighbors, wall, city)
                if rating < 0:
                    Constructor.assign_district(reg, regions, wall, city, options)
                    change = True

    @staticmethod
    def assign_district(reg, regions, wall, city, options):
        """
        Assigns a district to a region based on Ratings

        Parameters
        ----------
        options : List of ints
            User options
        reg : Region
            Region to have a district assigned to it
        regions : List of Regions
            All of the Regions on the map
        wall : Infrastructure
            The City wall
        city : Polygon
            The polygon representing the city limits
        """

        # Gets the rating for every District
        neighbors = reg.neighbors
        values = []
        districts = []

        if options[1] == 1:
            armory_val = Armory.determine_rating(reg, neighbors, wall, city)
            if armory_val >= 0:
                values.append(armory_val + 10)
                districts.append(Armory(0.8, 0.8, 14000))
        if options[3] == 1:
            castle_val = Castle.determine_rating(reg, neighbors, regions, wall, city)  # special case, needs all regions not
            # just neighbors
            if castle_val >= 0:
                values.append(castle_val + 10)
                districts.append(Castle())
        if options[4] == 1:
            cathedral_val = Cathedral.determine_rating(reg, neighbors, wall, city)
            if cathedral_val >= 0:
                values.append(cathedral_val + 10)
                districts.append(Cathedral())
        if options[6] == 1:
            farmland_val = Farmland.determine_rating(reg, neighbors, wall, city)
            if farmland_val >= 0:
                values.append(farmland_val + 10)
                districts.append(Farmland())
        if options[7] == 1:
            gate_val = Gate.determine_rating(reg, neighbors, wall, city)
            if gate_val >= 0:
                values.append(gate_val + 10)
                districts.append(Gate())
        if options[8] == 1:
            housinghigh_val = HousingHigh.determine_rating(reg, neighbors, wall, city)
            if housinghigh_val >= 0:
                values.append(housinghigh_val + 10)
                districts.append(HousingHigh(0.2, 0.5, 12000))
        if options[10] == 1:
            housingmid_val = HousingMid.determine_rating(reg, neighbors, wall, city)
            if housingmid_val >= 0:
                values.append(housingmid_val + 10)
                districts.append(HousingMid(0.5, 0.4, 8000))
        if options[9] == 1:
            housinglow_val = HousingLow.determine_rating(reg, neighbors, wall, city)
            if housinglow_val >= 0:
                values.append(housinglow_val + 10)
                districts.append(HousingLow(0.5, 0.3, 400))
        if options[12] == 1:
            market_val = Market.determine_rating(reg, neighbors, wall, city)
            if market_val >= 0:
                values.append(market_val + 10)
                districts.append(Market())
        if options[15] == 1:
            precinct_val = Precinct.determine_rating(reg, neighbors, wall, city)
            if precinct_val >= 0:
                values.append(precinct_val + 10)
                districts.append(Precinct())
        if options[17] == 1:
            slum_val = Slum.determine_rating(reg, neighbors, wall, city)
            if slum_val >= 0:
                values.append(slum_val + 10)
                districts.append(Slum(0.8, 0.01, 1000))
        if options[11] == 1:
            industrial_val = Industrial.determine_rating(reg, neighbors, wall, city)
            if industrial_val >= 0:
                values.append(industrial_val + 10)
                districts.append(Industrial(0.1, 0.1, 16000))
        if options[16] == 1:
            shops_val = Shops.determine_rating(reg, neighbors, wall, city)
            if shops_val >= 0:
                values.append(shops_val + 10)
                districts.append(Shops(0.2, 0.2, 10000))
        if options[5] == 1:
            courtyard_val = Courtyard.determine_rating(reg, neighbors, wall, city)
            if courtyard_val >= 0:
                values.append(courtyard_val + 10)
                districts.append(Courtyard())
        if options[13] == 1:
            openland_val = Openland.determine_rating(reg, neighbors, wall, city)
            if openland_val >= 0:
                values.append(openland_val + 10)
                districts.append(Openland())
        if options[14] == 1:
            park_val = Park.determine_rating(reg, neighbors, wall, city)
            if park_val >= 0:
                values.append(park_val + 10)
                districts.append(Park())

        # if no valid districts makes it OpenLand
        if len(values) == 0:
            reg.set_district(Openland())
        else:
            # randomly selects a district based on the weights/ratings of the districts
            dist = random.choices(districts, k=1, weights=values)
            reg.set_district(dist[0])
