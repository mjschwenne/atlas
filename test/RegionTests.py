import unittest
from src.Backend.Polygon import Polygon
from src.Backend.Point import Point
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
    i3ver = [Point(-5, -5), Point(10, 15), Point(11, 15), Point(11, 14)]
    i3Poly = Polygon(i3ver)

    # Square 1
    # ========
    s1ver = [Point(10, 15), Point(11, 15), Point(11, 14), Point(10, 14)]
    s1Poly = Polygon(s1ver)

    # in_city Tests
    def test_in_city_s1_i1(self):
        """
        Test of the Region.py in_city method with s1 being the Region and i1 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(True, reg.in_city(self.i1Poly))

    def test_in_city_i1_s1(self):
        """
        Test of the Region.py in_city method with i1 being the Region and s1 being the City
        """
        reg = Region(self.district, self.i1ver)
        self.assertEqual(False, reg.in_city(self.s1Poly))

    def test_in_city_s1_i2(self):
        """
        Test of the Region.py in_city method with s1 being the Region and i2 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(False, reg.in_city(self.i2Poly))

    def test_in_city_i2_s1(self):
        """
        Test of the Region.py in_city method with i2 being the Region and s1 being the City
        """
        reg = Region(self.district, self.i2ver)
        self.assertEqual(False, reg.in_city(self.s1Poly))

    def test_in_city_s1_s1(self):
        """
        Test of the Region.py in_city method with s1 being the Region and s1 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(True, reg.in_city(self.s1Poly))

    def test_in_city_i3_i2(self):
        """
        Test of the Region.py in_city method with i3 being the Region and i2 being the City
        """
        reg = Region(self.district, self.i3ver)
        self.assertEqual(False, reg.in_city(self.i2Poly))

    def test_in_city_i3_i1(self):
        """
        Test of the Region.py in_city method with i3 being the Region and i1 being the City
        """
        reg = Region(self.district, self.i3ver)
        self.assertEqual(False, reg.in_city(self.i1Poly))

    def test_in_city_s1_i3(self):
        """
        Test of the Region.py in_city method with s1 being the Region and i3 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(True, reg.in_city(self.i3Poly))

    # in_walls Tests
    def test_in_walls_s1_i1(self):
        """
        Test of the Region.py in_city method with s1 being the Region and i1 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(True, reg.in_walls(self.i1Poly))

    def test_in_walls_i1_s1(self):
        """
        Test of the Region.py in_city method with i1 being the Region and s1 being the City
        """
        reg = Region(self.district, self.i1ver)
        self.assertEqual(False, reg.in_walls(self.s1Poly))

    def test_in_walls_s1_i2(self):
        """
        Test of the Region.py in_city method with s1 being the Region and i2 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(False, reg.in_walls(self.i2Poly))

    def test_in_walls_i2_s1(self):
        """
        Test of the Region.py in_city method with i2 being the Region and s1 being the City
        """
        reg = Region(self.district, self.i2ver)
        self.assertEqual(False, reg.in_walls(self.s1Poly))

    def test_in_walls_s1_s1(self):
        """
        Test of the Region.py in_city method with s1 being the Region and s1 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(True, reg.in_walls(self.s1Poly))

    def test_in_walls_i3_i2(self):
        """
        Test of the Region.py in_city method with i3 being the Region and i2 being the City
        """
        reg = Region(self.district, self.i3ver)
        self.assertEqual(False, reg.in_walls(self.i2Poly))

    def test_in_walls_i3_i1(self):
        """
        Test of the Region.py in_city method with i3 being the Region and i1 being the City
        """
        reg = Region(self.district, self.i3ver)
        self.assertEqual(False, reg.in_walls(self.i1Poly))

    def test_in_walls_s1_i3(self):
        """
        Test of the Region.py in_city method with s1 being the Region and i3 being the City
        """
        reg = Region(self.district, self.s1ver)
        self.assertEqual(True, reg.in_walls(self.i3Poly))

if __name__ == '__main__':
    unittest.main()
