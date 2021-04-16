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
    def __init__(self, wall):
        self.wall = wall

    def generate_map(self, options):
        """
        Generates a random map, with the provided options.

        Parameters
        ----------
        options : list of ints
            The user options that control what districts are allowed, and if buildings are made
        Returns
        -------

        """
        # creates a fixed bounding polygon size
        # bounding_polygon = Polygon([Point(100, 100), Point(100, -100), Point(-100, -100), Point(-100, 100)])
        bounding_polygon = Polygon([Point(250, 250), Point(250, -250), Point(-250, -250), Point(-250, 250)])
        # decides how many districts are generated
        num_district = 10
        var1 = options[0]
        if var1 == 2:
            num_district = 25
            # bounding_polygon = Polygon([Point(250, 250), Point(250, -250), Point(-250, -250), Point(-250, 250)])
        elif var1 == 3:
            num_district = 50
            # bounding_polygon = Polygon([Point(500, 500), Point(500, -500), Point(-500, -500), Point(-500, 500)])
        elif var1 == 4:
            num_district = 75
            # bounding_polygon = Polygon([Point(750, 750), Point(750, -750), Point(-750, -750), Point(-750, 750)])
        elif var1 == 5:
            num_district = 100
            # bounding_polygon = Polygon([Point(1000, 1000), Point(1000, -250), Point(-1000, -1000), Point(-1000, 1000)])

        # creates the Voronoi diagram with the required dimensions and then relaxes it twice
        vor = Voronoi(num_district, bounding_polygon)
        vor.relax()
        vor.relax()

        # gets the polygons and makes them into regions
        polygons = vor.polygons
        regions = []
        for poly in polygons:
            regions.append(Region(None, poly.get_vertices()))

        # finds each regions neighboring regions
        for reg in regions:
             reg.find_neighbors(regions)

        # creates a wall and city, which modifies the graph to have the wall be a convex hull of points and shifts
        # the graph so the wall does not intersect any regions
        wall = Infrastructure(regions, vor.graph, bounding_polygon)
        self.wall
        
        self.assign_districts(regions, wall, options)

        # generates buildings if enabled
        if options[2] == 1:
            for reg in regions:
                if isinstance(reg.get_district(), BasicDistrict):
                    reg.get_district().generate_district(reg)
                elif isinstance(reg.get_district(), Courtyard):
                    reg.get_district().generate_district(reg)
                elif isinstance(reg.get_district(), Market):
                    reg.get_district().generate_district(reg)
                elif isinstance(reg.get_district(), Castle):
                    reg.get_district().generate_district(reg)
                elif isinstance(reg.get_district(), Cathedral):
                    reg.get_district().generate_district(reg)
                elif isinstance(reg.get_district(), Precinct):
                    reg.get_district().generate_district(reg)
        return regions

    @staticmethod
    def assign_districts(regions, wall, options):
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
        """

        # Clears out the previously stored regions if any
        for reg in regions:
            reg.set_district(None)

        # Assigns a district to each Region
        for reg in regions:
            Constructor.assign_district(reg, regions, wall, options)

        # Loops over the districts to do an initial placement of districts, and sees if a district must be forced placed
        # due to a lack of an any districts being valid
        change = False
        forced = 0
        for reg in regions:
            neighbors = reg.get_neighbors()
            if isinstance(reg.get_district(), Castle):
                rating = reg.get_district().determine_rating(reg, neighbors, regions, wall)
            else:
                rating = reg.get_district().determine_rating(reg, neighbors, wall)
            if rating < 0:
                force = Constructor.assign_district(reg, regions, wall, options)
                change = True
                if force:
                    forced += 1

        # checks to make sure all placements are either valid or were forced into its spot, if there were any changes
        # it will keep checking and making changes til none are forced or no changes are made
        while change and forced == 0:
            change = False
            for reg in regions:
                neighbors = reg.get_neighbors()
                if isinstance(reg.get_district(), Castle):
                    rating = reg.get_district().determine_rating(reg, neighbors, regions, wall)
                else:
                    rating = reg.get_district().determine_rating(reg, neighbors, wall)
                if rating < 0:
                    force = Constructor.assign_district(reg, regions, wall, options)
                    change = True
                    if force:
                        forced += 1

    @staticmethod
    def assign_district(reg, regions, wall, options):
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
        """

        # Gets the rating for every District
        neighbors = reg.neighbors
        values = []
        districts = []

        # if a district is a valid option, it gets its score, and adds it to the list
        if options[1] == 1:
            armory_val = Armory.determine_rating(reg, neighbors, wall)
            if armory_val >= 0:
                values.append(armory_val + 10)
                districts.append(Armory(0.6, 0.1, 100))
        if options[3] == 1:
            castle_val = Castle.determine_rating(reg, neighbors, regions, wall)  # special case, needs all
            # regions not just neighbors
            if castle_val >= 0:
                values.append(castle_val + 10)
                districts.append(Castle())
        if options[4] == 1:
            cathedral_val = Cathedral.determine_rating(reg, neighbors, wall)
            if cathedral_val >= 0:
                values.append(cathedral_val + 10)
                districts.append(Cathedral())
        if options[6] == 1:
            farmland_val = Farmland.determine_rating(reg, neighbors, wall)
            if farmland_val >= 0:
                values.append(farmland_val + 10)
                districts.append(Farmland())
        if options[7] == 1:
            gate_val = Gate.determine_rating(reg, neighbors, wall)
            if gate_val >= 0:
                values.append(gate_val + 10)
                districts.append(Gate(0.7, 0.04, 20))
        if options[8] == 1:
            housinghigh_val = HousingHigh.determine_rating(reg, neighbors, wall)
            if housinghigh_val >= 0:
                values.append(housinghigh_val + 10)
                districts.append(HousingHigh(0.4, 0.4, 120))
        if options[10] == 1:
            housingmid_val = HousingMid.determine_rating(reg, neighbors, wall)
            if housingmid_val >= 0:
                values.append(housingmid_val + 10)
                districts.append(HousingMid(0.5, 0.2, 80))
        if options[9] == 1:
            housinglow_val = HousingLow.determine_rating(reg, neighbors, wall)
            if housinglow_val >= 0:
                values.append(housinglow_val + 10)
                districts.append(HousingLow(0.6, 0.1, 50))
        if options[12] == 1:
            market_val = Market.determine_rating(reg, neighbors, wall)
            if market_val >= 0:
                values.append(market_val + 10)
                districts.append(Market())
        if options[15] == 1:
            precinct_val = Precinct.determine_rating(reg, neighbors, wall)
            if precinct_val >= 0:
                values.append(precinct_val + 10)
                districts.append(Precinct())
        if options[17] == 1:
            slum_val = Slum.determine_rating(reg, neighbors, wall)
            if slum_val >= 0:
                values.append(slum_val + 10)
                districts.append(Slum(0.8, 0.01, 15))
        if options[11] == 1:
            industrial_val = Industrial.determine_rating(reg, neighbors, wall)
            if industrial_val >= 0:
                values.append(industrial_val + 10)
                districts.append(Industrial(0.3, 0.1, 90))
        if options[16] == 1:
            shops_val = Shops.determine_rating(reg, neighbors, wall)
            if shops_val >= 0:
                values.append(shops_val + 10)
                districts.append(Shops(0.4, 0.2, 40))
        if options[5] == 1:
            courtyard_val = Courtyard.determine_rating(reg, neighbors, wall)
            if courtyard_val >= 0:
                values.append(courtyard_val + 10)
                districts.append(Courtyard())
        if options[13] == 1:
            openland_val = Openland.determine_rating(reg, neighbors, wall)
            if openland_val >= 0:
                values.append(openland_val + 10)
                districts.append(Openland())
        if options[14] == 1:
            park_val = Park.determine_rating(reg, neighbors, wall)
            if park_val >= 0:
                values.append(park_val + 10)
                districts.append(Park())

        # if no valid districts makes it OpenLand
        if len(values) == 0:
            if reg.in_walls(wall):
                reg.set_district(HousingLow(0.6, 0.1, 50))
            else:
                reg.set_district(Openland())
            return True
        else:
            # randomly selects a district based on the weights/ratings of the districts
            dist = random.choices(districts, k=1, weights=values)
            reg.set_district(dist[0])
            return False
