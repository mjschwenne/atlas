import random

from src.Backend.District import *


class Constructor:
    """
    The constructor handles the compilation and processing of information from the backend and the transition of that
    information into something that the front end can handle

    Methods
    -------
    assign_districts(regions, wall, city)
        Assigns the provided regions a district
    assign_district(reg, regions, wall, city)
        Assigns the region a district

    """

    @staticmethod
    def assign_districts(regions, wall, city):
        """
        Assigns the provided regions a district at sudo-random order, taking into account the wall and city bounds

        Parameters
        ----------
        regions : List of regions
            Regions to have districts assigned
        wall : Wall
            The wall of the city
        city : Polygon
            The polygon representing the city bounds
        """

        # Clears out the previously stored regions if any
        for reg in regions:
            reg.set_district(None)

        # Assigns a district to each Region
        for reg in regions:
            Constructor.assign_district(reg, regions, wall, city)

        # Loops over the districts to ensure valid placement at every location until all assignments are valid
        change = True
        while change:
            change = False
            for reg in regions:
                rating = reg.get_district().determine_rating(reg, regions, wall, city)
                if rating < 0:
                    Constructor.assign_district(reg, regions, wall, city)
                    change = True

    @staticmethod
    def assign_district(reg, regions, wall, city):
        """
        Assigns a district to a region based on Ratings

        Parameters
        ----------
        reg : Region
            Region to have a district assigned to it
        regions : List of Regions
            All of the Regions on the map
        wall : Wall
            The City wall
        city : Polygon
            The polygon representing the city limits
        """

        # Gets the rating for every District
        armory_val = Armory.determine_rating(reg, regions, wall, city)
        castle_val = Castle.determine_rating(reg, regions, wall, city)
        cathedral_val = Cathedral.determine_rating(reg, regions, wall, city)
        farmland_val = Farmland.determine_rating(reg, regions, wall, city)
        gate_val = Gate.determine_rating(reg, regions, wall, city)
        housinghigh_val = HousingHigh.determine_rating(reg, regions, wall, city)
        housingmid_val = HousingMid.determine_rating(reg, regions, wall, city)
        housinglow_val = HousingLow.determine_rating(reg, regions, wall, city)
        market_val = Market.determine_rating(reg, regions, wall, city)
        precinct_val = Precinct.determine_rating(reg, regions, wall, city)
        slum_val = Slum.determine_rating(reg, regions, wall, city)
        industrial_val = Industrial.determine_rating(reg, regions, wall, city)
        shops_val = Shops.determine_rating(reg, regions, wall, city)
        courtyard_val = Courtyard.determine_rating(reg, regions, wall, city)
        openland_val = Openland.determine_rating(reg, regions, wall, city)
        park_val = Park.determine_rating(reg, regions, wall, city)

        # creates lists of valid Districts and Weights
        values = []
        districts = []

        # checks to see if a district is valid, if so adds it to the lists
        if armory_val >= 0:
            values.append(armory_val + 10)
            districts.append(Armory(0.8, 0.8, 14000))
        if castle_val >= 0:
            values.append(castle_val + 10)
            districts.append(Castle())
        if cathedral_val >= 0:
            values.append(cathedral_val + 10)
            districts.append(Cathedral())
        if farmland_val >= 0:
            values.append(farmland_val + 10)
            districts.append(Farmland())
        if gate_val >= 0:
            values.append(gate_val + 10)
            districts.append(Gate())
        if housinghigh_val >= 0:
            values.append(housinghigh_val + 10)
            districts.append(HousingHigh(0.2, 0.5, 12000))
        if housingmid_val >= 0:
            values.append(housingmid_val + 10)
            districts.append(HousingMid(0.5, 0.4, 8000))
        if housinglow_val >= 0:
            values.append(housinglow_val + 10)
            districts.append(HousingLow(0.5, 0.3, 400))
        if market_val >= 0:
            values.append(market_val + 10)
            districts.append(Market())
        if precinct_val >= 0:
            values.append(precinct_val + 10)
            districts.append(Precinct())
        if slum_val >= 0:
            values.append(slum_val + 10)
            districts.append(Slum(0.8, 0.01, 1000))
        if industrial_val >= 0:
            values.append(industrial_val + 10)
            districts.append(Industrial(0, 0, 0))
        if shops_val >= 0:
            values.append(shops_val + 10)
            districts.append(Shops(0, 0, 0))
        if courtyard_val >= 0:
            values.append(courtyard_val + 10)
            districts.append(Courtyard())
        if openland_val >= 0:
            values.append(openland_val + 10)
            districts.append(Openland())
        if park_val >= 0:
            values.append(park_val + 10)
            districts.append(Park())


        # randomly selects a district based on the weights/ratings of the districts
        dist = random.choices(districts, k=1, weights=values)
        reg.set_district(dist[0])
