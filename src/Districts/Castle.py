from src.Backend.District import District
from src.Districts.Cathedral import Cathedral
from src.Districts.Housing import Housing
from src.Districts.Gate import Gate
from src.Districts.Slum import Slum
from src.Districts.WarCamp import WarCamp
from src.Districts.Armory import Armory
from src.Backend.Region import Region


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
                    elif isinstance(dis, WarCamp):
                        rating += -100
        if region.in_walls(wall):
            rating += 1000
        return rating
