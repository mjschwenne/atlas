from src.Backend.District import District
from src.Districts.Housing import Housing
from src.Districts.Castle import Castle
from src.Districts.Market import Market
from src.Districts.WarCamp import WarCamp
from src.Backend.Region import Region


class Gate(District):

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
        bool
        on_gate = False
        for ver in wall.get_gates():
            if region.is_contained(ver):
                on_gate = True
                rating += 200
                break
        if not on_gate:
            return -1000
        for reg in other_regions:
            if region != reg:
                if region.is_bordering(reg):
                    dis = reg.get_district()
                    if isinstance(dis, Housing):
                        rating += 20
                    elif isinstance(dis, Market):
                        rating += 10
                    elif isinstance(dis, Castle):
                        rating += 10
                    elif isinstance(dis, WarCamp):
                        rating += 20
        return rating
