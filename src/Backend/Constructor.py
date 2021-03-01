import random

from src.Backend.District import *


class Constructor:

    def assign_districts(self, regions, wall, city):
        for reg in regions:
            reg.set_district(None)
        for reg in regions:
            self.assign_district(reg, regions, wall, city)
        change = True
        while change:
            change = False
            for reg in regions:
                rating = reg.get_district().determine_rating(reg, regions, wall, city)
                if rating < 0:
                    self.assign_district(reg, regions, wall, city)
                    change = True

    def assign_district(self, reg, regions, wall, city):
        armory_val = Armory.determine_rating(reg, regions, wall, city)
        castle_val = Castle.determine_rating(reg, regions, wall, city)
        cathedral_val = Cathedral.determine_rating(reg, regions, wall, city)
        docks_val = Docks.determine_rating(reg, regions, wall, city)
        farmland_val = Farmland.determine_rating(reg, regions, wall, city)
        gate_val = Gate.determine_rating(reg, regions, wall, city)
        housing_val = Housing.determine_rating(reg, regions, wall, city)
        market_val = Market.determine_rating(reg, regions, wall, city)
        precinct_val = Precinct.determine_rating(reg, regions, wall, city)
        slum_val = Slum.determine_rating(reg, regions, wall, city)
        smithing_val = Smithing.determine_rating(reg, regions, wall, city)
        warcamp_val = WarCamp.determine_rating(reg, regions, wall, city)
        values = []
        districts = []
        if armory_val >= 0:
            values.append(armory_val + 10)
            districts.append(Armory(0, 0, 0))
        if castle_val >= 0:
            values.append(castle_val + 10)
            districts.append(Castle(0, 0, 0))
        if cathedral_val >= 0:
            values.append(cathedral_val + 10)
            districts.append(Cathedral(0, 0, 0))
        if docks_val >= 0:
            values.append(docks_val + 10)
            districts.append(Docks(0, 0, 0))
        if farmland_val >= 0:
            values.append(farmland_val + 10)
            districts.append(Farmland(0, 0, 0))
        if gate_val >= 0:
            values.append(gate_val + 10)
            districts.append(Gate(0, 0, 0))
        if housing_val >= 0:
            values.append(housing_val + 10)
            districts.append(Housing(0, 0, 0))
        if market_val >= 0:
            values.append(market_val + 10)
            districts.append(Market(0, 0, 0))
        if precinct_val >= 0:
            values.append(precinct_val + 10)
            districts.append(Precinct(0, 0, 0))
        if slum_val >= 0:
            values.append(slum_val + 10)
            districts.append(Slum(0, 0, 0))
        if smithing_val >= 0:
            values.append(smithing_val + 10)
            districts.append(Smithing(0, 0, 0))
        if warcamp_val >= 0:
            values.append(warcamp_val + 10)
            districts.append(WarCamp(0, 0, 0))

        dist = random.choices(districts, k=1, weights=values)
        reg.set_district(dist[0])
