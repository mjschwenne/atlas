from src.Backend.District import District
from src.Backend.Region import Region
from src.Districts.Housing import Housing
from src.Districts.Castle import Castle
from src.Districts.Market import Market
from src.Districts.Precinct import Precinct
from src.Districts.Slum import Slum
from src.Districts.Smithing import Smithing
from src.Districts.WarCamp import WarCamp
from src.Districts.Armory import Armory


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
        for reg in other_regions:
            if region != reg:
                if not (reg.is_water() or reg.has_river()):
                    return -1000
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
                    elif isinstance(dis, Castle):
                        rating += 30
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
