import math
import unittest
import numpy as np
from src.Backend.Point import Point

"""
Unlike most of the other test files, this one does not test a certain backend or frontend file, but rather helps
us understand the process of generating a angle which will bisect a polygon
"""


def d(p, v_start, v_end):
    """
    Takes in a vector defined by two points and a point and computes a version of the dot product whose sign can
    be used to determine which side of the vector it is on.

    Parameters
    ----------
    p : Point
        A point which we wish to determine which side of the line it is on
    v_start : Point
        Origin of the vector
    v_end : Point
        Destination of the vector

    Returns
    -------
    float
        The result of the formula
    """
    return (p.get_x() - v_start.get_x()) * (v_end.get_y() - v_start.get_y()) - \
           (p.get_y() - v_start.get_y()) * (v_end.get_x() - v_start.get_x())


def normalize_angle(angle):
    """
    Normalizes an angle in radians to be in the -pi to +pi range

    Parameters
    ----------
    angle : float
        The angle to normalize

    Returns
    -------
    float
        The normalized angle
    """
    angle = round(angle, 8)
    while round(angle, 8) > round(math.pi, 8):
        angle -= round(2 * math.pi, 8)
    angle = round(angle, 8)
    while round(angle, 8) < round(-math.pi, 8):
        angle += round(2 * math.pi, 8)
    return round(angle, 8)


def test(c, v_start, v_end):
    """
    Simulates one case the process of finding the bisection angle in district generation
    """
    # Midpoint of the vector
    p = Point((v_start.get_x() + v_end.get_x()) / 2, (v_start.get_y() + v_end.get_y()) / 2)
    # Angle of the vector
    ang = math.atan2(v_end.get_y() - v_start.get_y(), v_end.get_x() - v_start.get_x())
    # Calculate for c
    d_c = d(c, v_start, v_end)
    if ang != 0 and round(ang, 8) != round(math.pi, 8):
        d_p = d(Point(p.get_x() - 1, p.get_y()), v_start, v_end)
    else:
        d_p = d(Point(p.get_x(), p.get_y() + 1), v_start, v_end)
    # Compare the signs
    # if np.sign(d_c) == np.sign(d_p):
    #     ang -= np.sign(d_c) * math.pi / 2
    # else:
    ang -= np.sign(d_c) * math.pi / 2

    return d_c, d_p, ang


class MyTestCase(unittest.TestCase):

    def test_center_left(self):
        v_start = Point(0, 0)
        v_end = Point(2, 2)
        c = Point(0, 2)
        expected_ang = round(3 * math.pi / 4, 8)
        d_c, d_p, ang = test(c, v_start, v_end)
        actual_ang = normalize_angle(ang)
        self.assertEqual(expected_ang, actual_ang)

    def test_center_right(self):
        v_start = Point(0, 0)
        v_end = Point(2, 2)
        c = Point(2, 0)
        expected_ang = round(-math.pi / 4, 8)
        d_c, d_p, ang = test(c, v_start, v_end)
        actual_ang = normalize_angle(ang)
        self.assertEqual(expected_ang, actual_ang)

    def test_center_left_backwards_vector(self):
        v_start = Point(2, 2)
        v_end = Point(0, 0)
        c = Point(0, 2)
        expected_ang = round(3 * math.pi / 4, 8)
        d_c, d_p, ang = test(c, v_start, v_end)
        actual_ang = normalize_angle(ang)
        self.assertEqual(expected_ang, round(actual_ang, 8))

    def test_center_right_backwards_vector(self):
        v_start = Point(2, 2)
        v_end = Point(0, 0)
        c = Point(2, 0)
        expected_ang = round(-math.pi / 4, 8)
        d_c, d_p, ang = test(c, v_start, v_end)
        actual_ang = actual_ang = normalize_angle(ang)
        self.assertEqual(expected_ang, round(actual_ang, 8))

    def test_center_left_horizontal_vector(self):
        v_start = Point(0, 0)
        v_end = Point(2, 0)
        c = Point(1, 1)
        expected_ang = round(math.pi / 2, 8)
        d_c, d_p, ang = test(c, v_start, v_end)
        actual_ang = normalize_angle(ang)
        self.assertEqual(expected_ang, actual_ang)

    def test_center_right_horizontal_vector(self):
        v_start = Point(0, 0)
        v_end = Point(2, 0)
        c = Point(1, -1)
        expected_ang = round(-math.pi / 2, 8)
        d_c, d_p, ang = test(c, v_start, v_end)
        actual_ang = normalize_angle(ang)
        self.assertEqual(expected_ang, actual_ang)

    def test_center_left_horizontal_backwards_vector(self):
        v_start = Point(2, 0)
        v_end = Point(0, 0)
        c = Point(1, 1)
        expected_ang = round(math.pi / 2, 8)
        d_c, d_p, ang = test(c, v_start, v_end)
        actual_ang = normalize_angle(ang)
        self.assertEqual(expected_ang, actual_ang)

    def test_center_right_horizontal_backwards_vector(self):
        v_start = Point(2, 0)
        v_end = Point(0, 0)
        c = Point(1, -1)
        expected_ang = round(-math.pi / 2, 8)
        d_c, d_p, ang = test(c, v_start, v_end)
        actual_ang = normalize_angle(ang)
        self.assertEqual(expected_ang, actual_ang)


if __name__ == '__main__':
    unittest.main()
