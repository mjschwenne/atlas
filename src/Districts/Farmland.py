from src.Backend.District import District
from src.Districts.Precinct import Precinct
from src.Districts.Housing import Housing
from src.Backend.Region import Region


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
                    elif isinstance(dis, Precinct):
                        rating -= 10
        if region.in_city(city):
            rating -= 100
        if region.in_walls(wall):
            rating -= 1000
        return rating
