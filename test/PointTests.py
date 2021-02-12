import unittest
from src import Point


class TestPoint(unittest.TestCase):

    def test_constructor_x(self):
        point0 = Point.Point(0, 0)
        self.assertEqual(point0.get_x(), 0)

    def test_constructor_y(self):
        point0 = Point.Point(0, 0)
        self.assertEqual(point0.get_y(), 0)


if __name__ == '__main__':
    unittest.main()
