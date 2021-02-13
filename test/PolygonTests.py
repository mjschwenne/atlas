import unittest
from src import Polygon
from src import Point


class TestPolygonSquares(unittest.TestCase):
    # Square 1
    # ========
    s1p1 = Point.Point(0.0, 0.0)
    s1p2 = Point.Point(0.0, 1.0)
    s1p3 = Point.Point(1.0, 1.0)
    s1p4 = Point.Point(1.0, 0.0)
    s1ver = [s1p1, s1p2, s1p3, s1p4]

    # Square 2
    # ========
    s2p1 = Point.Point(0.0, 0.0)
    s2p2 = Point.Point(0.0, 10.0)
    s2p3 = Point.Point(10.0, 10.0)
    s2p4 = Point.Point(10.0, 0.0)
    s2ver = [s2p1, s2p2, s2p3, s2p4]

    # Square 1 Tests
    def test_perimeter_s1(self):
        """
        Test of the Polygon.py get_perimeter method for s1
        """
        poly = Polygon.Polygon(self.s1ver)

        self.assertEqual(4, poly.get_perimeter())

    def test_is_convex_s1(self):
        poly = Polygon.Polygon(self.s1ver)

        self.assertEqual(True, poly.is_convex())

    # Square 2 Tests
    def test_perimeter_s2(self):
        """
        Test of the Polygon.py get_perimeter method for s2
        """
        poly = Polygon.Polygon(self.s2ver)

        self.assertEqual(40, poly.get_perimeter())

    def test_is_convex_s2(self):
        """
        Test of the Polygon.py is_convex method for s2
        """
        poly = Polygon.Polygon(self.s2ver)

        self.assertEqual(True, poly.is_convex())

if __name__ == '__main__':
    unittest.main()
