import unittest
from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
from src.Backend.Wall import Wall
from src.Backend.Region import Region
from src.Backend.District import District


class TestRegion(unittest.TestCase):
    # District
    # =========
    district = District(0, 0, 0)

    # Irregular 1
    # ===========
    i1ver = [Point(3, 19), Point(6, 18), Point(8, 18), Point(19, 12), Point(15, 7), Point(15, 2)]
    i1Poly = Polygon(i1ver)

    # Irregular 2
    # ===========
    i2ver = [Point(-10, 10), Point(2, 8), Point(2, -2), Point(5, -7), Point(-5, -10),
             Point(-7, -4), Point(-7, 3), Point(-8.5, 4.2)]
    i2Poly = Polygon(i2ver)

    # Irregular 3
    # ===========
    i3ver = [Point(9, 10.5), Point(15, 2), Point(4.4, -6), Point(2.6, -3), Point(6, 8)]
    i3Poly = Polygon(i3ver)

    # Square 1
    # ========
    s1ver = [Point(10, 15), Point(11, 15), Point(11, 14), Point(10, 14)]
    s1Poly = Polygon(s1ver)

    def test_in_city_s1_i1(self):
        """
        Test of the Region.py in_city method with s1 being the Region and i1 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(True, reg.in_city(self.i1Poly))


if __name__ == '__main__':
    unittest.main()
