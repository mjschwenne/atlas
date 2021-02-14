import unittest
from src.Polygon import Polygon
from src.Point import Point


class TestPolygon(unittest.TestCase):
    # Square 1
    # ========
    s1p1 = Point(0.0, 0.0)
    s1p2 = Point(0.0, 1.0)
    s1p3 = Point(1.0, 1.0)
    s1p4 = Point(1.0, 0.0)
    s1ver = [s1p1, s1p2, s1p3, s1p4]

    # Square 2
    # ========
    s2p1 = Point(0.0, 0.0)
    s2p2 = Point(0.0, 10.0)
    s2p3 = Point(10.0, 10.0)
    s2p4 = Point(10.0, 0.0)
    s2ver = [s2p1, s2p2, s2p3, s2p4]

    # Less than 3 points
    # ==================
    sh1p1 = Point(0.0, 0.0)
    sh1p2 = Point(0.0, 0.1)
    sh1ver = [sh1p1, sh1p2]

    # Repeated point
    # ==============
    sh2p1 = Point(0.0, 0.0)
    sh2p2 = Point(0.0, 0.0)
    sh2p3 = Point(0.0, 1.0)
    sh2p4 = Point(1.0, 1.0)
    sh2p5 = Point(1.0, 0.0)
    sh2ver = [sh2p1, sh2p2, sh2p3, sh2p4, sh2p5]

    # Pentagram (intersecting) Shape
    # ==============================
    sh3p1 = Point(0.0, 5.0)
    sh3p2 = Point(4.0, -5.0)
    sh3p3 = Point(-5.0, 2.0)
    sh3p4 = Point(5.0, 2.0)
    sh3p5 = Point(-4.0, -5.0)
    sh3ver = [sh3p1, sh3p2, sh3p3, sh3p4, sh3p5]

    # Square 1 Tests
    def test_perimeter_s1(self):
        """
        Test of the Polygon.py get_perimeter method for s1
        """
        poly = Polygon(self.s1ver)

        self.assertEqual(4, poly.get_perimeter())

    def test_is_convex_s1(self):
        poly = Polygon(self.s1ver)

        self.assertEqual(True, poly.is_convex())

    # Square 2 Tests
    def test_perimeter_s2(self):
        """
        Test of the Polygon.py get_perimeter method for s2
        """
        poly = Polygon(self.s2ver)

        self.assertEqual(40, poly.get_perimeter())

    def test_is_convex_s2(self):
        """
        Test of the Polygon.py is_convex method for s2
        """
        poly = Polygon(self.s2ver)

        self.assertEqual(True, poly.is_convex())

    # is_convex method tests
    def test_less_than_three_points_is_convex(self):
        """
        Test of a Polygon with less than 3 points (should return false for is_convex)
        """
        poly = Polygon(self.sh1ver)

        self.assertEqual(False, poly.is_convex())

    def test_repeated_point_is_convex(self):
        """
        Test of a Polygon with a repeated point (should return false for is_convex)
        """
        poly = Polygon(self.sh2ver)

        self.assertEqual(False, poly.is_convex())

    def test_pentagram_is_convex(self):
        """
        Test of a Polygon with intersecting lines, a pentagram (should return false for is_convex)
        """
        poly = Polygon(self.sh3ver)

        self.assertEqual(False, poly.is_convex())


if __name__ == '__main__':
    unittest.main()
