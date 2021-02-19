import unittest
from src.Backend.Point import Point


class TestPoint(unittest.TestCase):

    def test_constructor_0(self):
        """
        Test of the Point.py constructor for initial values of 0
        """
        point = Point(0, 0)
        values = (point.get_x(), point.get_y())
        self.assertEqual((0, 0), values)

    def test_constructor_positive(self):
        """
        Tests the Point.py constructor for initial values that are positive
        """
        point = Point(1, 2)
        values = (point.get_x(), point.get_y())
        self.assertEqual((1, 2), values)

    def test_constructor_negative(self):
        """
        Tests the Point.py constructor for negative values
        """
        point = Point(-1, -2)
        values = (point.get_x(), point.get_y())
        self.assertEqual((-1, -2), values)

    def test_constructor_positive_decimal(self):
        """
        Tests the constructor with positive values 0<x<1
        """
        point = Point(0.1, 0.2)
        values = (point.get_x(), point.get_y())
        self.assertEqual((0.1, 0.2), values)

    def test_constructor_negative_decimal(self):
        """
        Test constructor with negative values 0<x<1
        """
        point = Point(-0.1, -0.2)
        values = (point.get_x(), point.get_y())
        self.assertEqual((-0.1, -0.2), values)

    def test_set_x(self):
        """
        Tests the set_x method
        """
        point = Point(0, 0)
        point.set_x(1.0)
        self.assertEqual(1, point.get_x())

    def test_set_y(self):
        """
        Tests the set_y method
        """
        point = Point(0, 0)
        point.set_y(1.0)
        self.assertEqual(1, point.get_y())

    def test_simple_distance_same_point(self):
        """
        Test the simple_distance method for distance between a point and itself
        """
        point = Point(0, 0)
        self.assertEqual(0, point.simple_distance(point))

    def test_simple_distance_neg_pos(self):
        """
        Test the simple_distance method form a negative point to a positive point
        """
        point1 = Point(-1, -2)
        point2 = Point(1, 2)
        self.assertEqual(4.47214, round(point1.simple_distance(point2), 5))

    def test_simple_distance_pos_pos(self):
        """
        Tests the simple_distance method for two positive points
        """
        point1 = Point(1, 2)
        point2 = Point(3, 4)
        self.assertEqual(2.82843, round(point1.simple_distance(point2), 5))

    def test_simple_distance_neg_neg(self):
        """
        Test the simple_distance method for two negative points
        """
        point1 = Point(-1, -2)
        point2 = Point(-3, -4)
        self.assertEqual(2.82843, round(point1.simple_distance(point2), 5))

    def test_simple_distance_pos_neg(self):
        """
        Test the simple_distance method from a positive point to a negative point
        """
        point1 = Point(1, 2)
        point2 = Point(-1, -2)
        self.assertEqual(4.47214, round(point1.simple_distance(point2), 5))

    def test_manhattan_distance_same_point(self):
        """
        Test manhattan_distance method for a point to itself
        """
        point = Point(0, 0)
        self.assertEqual(0, point.manhattan_distance(point))

    def test_manhattan_distance_neg_pos(self):
        """
        Tests manhattan_distance method from a negative point to a positive point
        """
        point1 = Point(-1, -2)
        point2 = Point(1, 2)
        self.assertEqual(6, point1.manhattan_distance(point2))

    def test_manhattan_distance_pos_pos(self):
        """
        Test manhattan_distance method for two positive points
        """
        point1 = Point(1, 2)
        point2 = Point(3, 4)
        self.assertEqual(4, point1.manhattan_distance(point2))

    def test_manhattan_distance_neg_neg(self):
        """
        Test the manhattan_distance method for two negative points
        """
        point1 = Point(-1, -2)
        point2 = Point(-3, -4)
        self.assertEqual(4, point1.manhattan_distance(point2))

    def test_manhattan_distance_pos_neg(self):
        """
        Tests manhattan_distance method from a positive point to a negative point
        """
        point1 = Point(1, 2)
        point2 = Point(-1, -2)
        self.assertEqual(6, point1.manhattan_distance(point2))
    
    def test_points_equal(self):
        """
        Tests the __eq__ magic function
        """
        self.assertEqual(True, Point(1, 1) == Point(1, 1))

    def test_points_equal2(self):
        """
        Tests the __eq__ magic function
        """
        self.assertEqual(False, Point(0, 0) == Point(1, 1))

    def test_points_not_equal(self):
        """
        Tests the __ne__ magic function
        """
        self.assertEqual(False, Point(1, 1) != Point(1, 1))

    def test_points_not_equal2(self):
        """
        Tests the __ne__ magic function
        """
        self.assertEqual(True, Point(0, 0) != Point(1, 1))

    def test_points_lt(self):
        """
        Tests the __lt__ magic function for a smaller y coordinate
        """
        self.assertEqual(True, Point(2, -1) < Point(0, 0))

    def test_points_lt2(self):
        """
        Tests the __lt__ magic function for an equal y but smaller x
        """
        self.assertEqual(True, Point(-2, 0) < Point(0, 0))

    def test_points_lt3(self):
        """
        Tests the __lt__ magic function for an equal y but larger x
        """
        self.assertEqual(False, Point(2, 0) < Point(0, 0))

    def test_points_lt4(self):
        """
        Tests the __lt__ magic function for a larger y
        """
        self.assertEqual(False, Point(2, 1) < Point(0, 0))

    def test_points_lt5(self):
        """
        Tests the __lt__ magic function for an equal point
        """
        self.assertEqual(False, Point(1, 1) < Point(1, 1))

    def test_points_le(self):
        """
        Tests the __le__ magic function for a smaller point
        """
        self.assertEqual(True, Point(-1, -1) <= Point(0, 0))

    def test_points_le2(self):
        """
        Tests the __le__ magic function for an equal point
        """
        self.assertEqual(True, Point(0, 0) <= Point(0, 0))

    def test_points_le3(self):
        """
        Tests the __e__ magic function for a larger point
        """
        self.assertEqual(False, Point(-1, 1) <= Point(0, 0))

    def test_points_gt(self):
        """
        Tests the __gt__ magic function for a smaller y coordinate
        """
        self.assertEqual(False, Point(2, -1) > Point(0, 0))

    def test_points_gt2(self):
        """
        Tests the __gt__ magic function for an equal y but smaller x
        """
        self.assertEqual(False, Point(-2, 0) > Point(0, 0))

    def test_points_gt3(self):
        """
        Tests the __gt__ magic function for an equal y but larger x
        """
        self.assertEqual(True, Point(2, 0) > Point(0, 0))

    def test_points_gt4(self):
        """
        Tests the __gt__ magic function for a larger y
        """
        self.assertEqual(True, Point(2, 1) > Point(0, 0))

    def test_points_gt5(self):
        """
        Tests the __gt__ magic function for an equal point
        """
        self.assertEqual(False, Point(1, 1) > Point(1, 1))

    def test_points_ge(self):
        """
        Tests the __ge__ magic function for a smaller point
        """
        self.assertEqual(False, Point(-1, -1) >= Point(0, 0))

    def test_points_ge2(self):
        """
        Tests the __ge__ magic function for an equal point
        """
        self.assertEqual(True, Point(0, 0) >= Point(0, 0))

    def test_points_ge3(self):
        """
        Tests the __ge__ magic function for a larger point
        """
        self.assertEqual(True, Point(-1, 1) >= Point(0, 0))


if __name__ == '__main__':
    unittest.main()
