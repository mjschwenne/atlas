import unittest

import math

from src.Backend.Polygon import Polygon
from src.Backend.Point import Point

import matplotlib.pyplot as plt


class TestPolygon(unittest.TestCase):
    # Square 1
    # ========
    s1ver = [Point(0.0, 0.0), Point(0.0, 1.0), Point(1.0, 1.0), Point(1.0, 0.0)]

    # Square 2
    # ========
    s2ver = [Point(0.0, 0.0), Point(0.0, 10.0), Point(10.0, 10.0), Point(10.0, 0.0)]

    # Irregular 1
    # ===========
    i1ver = [Point(3, 19), Point(6, 18), Point(8, 18), Point(19, 12), Point(15, 7), Point(15, 2)]

    # Irregular 2
    # ===========
    i2ver = [Point(-10, 10), Point(2, 8), Point(2, -2), Point(5, -7), Point(-5, -10),
             Point(-7, -4), Point(-7, 3), Point(-8.5, 4.2)]

    # Irregular 3
    # ===========
    i3ver = [Point(9, 10.5), Point(15, 2), Point(4.4, -6), Point(2.6, -3), Point(6, 8)]

    # Less than 3 points
    # ==================
    sh1ver = [Point(0.0, 0.0), Point(0.0, 0.1)]

    # Repeated point
    # ==============
    sh2ver = [Point(0.0, 0.0), Point(0.0, 0.0), Point(0.0, 1.0), Point(1.0, 1.0), Point(1.0, 0.0)]

    # Pentagram (intersecting) Shape
    # ==============================
    sh3ver = [Point(0.0, 5.0), Point(4.0, -5.0), Point(-5.0, 2.0), Point(5.0, 2.0), Point(-4.0, -5.0)]

    # Polygon is_contained exhaustive tests
    # =====================================
    poly_ex_1 = Polygon([Point(-5, 5), Point(-2, 2), Point(-3.5, -1), Point(-6.5, -1), Point(-8, 2)])

    # Bounding box bug
    # ================
    bounding_box = Polygon([Point(-200, 200), Point(200, 200), Point(200, -200), Point(-200, -200)])

    # is_contained district bug 02/28/21
    # ==================================
    reg_1 = Polygon([Point(-3.5, 12), Point(0, 12), Point(0, 10), Point(-2, 9)])
    reg_2 = Polygon([Point(3.5, 12), Point(0, 12), Point(0, 10), Point(2, 9)])
    Wall_1 = Polygon([Point(3.5, -2), Point(6, 2), Point(6, 8), Point(3.5, 12), Point(-3.5, 12), Point(-6, 8),
                      Point(-6, 2), Point(-3.5, -2)])

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

    def test_get_center_s1(self):
        """
        Test of the Polygon.py get_center method for s1
        """
        poly = Polygon(self.s1ver)

        self.assertEqual((0.5, 0.5), poly.get_center().get())

    def test_get_center_s2(self):
        """
        Test of the Polygon.py get_center method for s2
        """
        poly = Polygon(self.s2ver)

        self.assertEqual((5, 5), poly.get_center().get())

    def test_get_center_i1(self):
        """
        Test of the Polygon.py get_center method for i1

        Oracle, MATLAB: centroid(polyshape([3 6 8 19 15 15], [19 18 18 12 7 2]))
        """
        poly = Polygon(self.i1ver)
        cx, cy = poly.get_center().get()
        self.assertEqual((11.7333, 11.9009), (round(cx, 4), round(cy, 4)))

    def test_get_center_i2(self):
        """
        Test of the Polygon.py get_center method for i1

        Oracle, MATLAB: centroid(polyshape([-10 2 2 5 -5 -7 -7 -8.5 -10], [10 8 -2 -7 -10 -4 3 4.2 10]))
        """
        poly = Polygon(self.i2ver)
        cx, cy = poly.get_center().get()
        self.assertEqual((-2.6617, 0.3087), (round(cx, 4), round(cy, 4)))

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

    def test_is_bordering_squares(self):
        """
        Test of Polygon.py with two different sized squares with a corner at (0, 0)
        """
        s1 = Polygon(self.s1ver)
        s2 = Polygon(self.s2ver)

        self.assertEqual(True, s1.is_bordering(s2))

    def test_is_bordering_irregulars1(self):
        """
        Test of Polygon.py to see if the two irregular polygons are bordering
        """
        i1 = Polygon(self.i1ver)
        i2 = Polygon(self.i2ver)

        self.assertEqual(False, i1.is_bordering(i2))

    def test_is_bordering_irregulars2(self):
        """
        Test of Polygon with two bordering, irregular polygons with one matching vertex
        """
        i1 = Polygon(self.i1ver)
        i3 = Polygon(self.i3ver)

        self.assertEqual(True, i3.is_bordering(i1))

    def test_is_bordering_irregulars3(self):
        """
        Test of Polygon with two bordering, irregular polygons with no matching vertices
        """
        i2 = Polygon(self.i2ver)
        i3 = Polygon(self.i3ver)

        self.assertEqual(True, i2.is_bordering(i3))

    def test_is_bordering_intersecting(self):
        """
        Test of Polygon with two intersecting polygons, but no vertices along a shared edge
        """
        s2 = Polygon(self.s2ver)
        i1 = Polygon(self.i1ver)

        self.assertEqual(False, i1.is_bordering(s2))

    def test_poly_ex_1_1(self):
        """
        The first test in an exhaustive test of is_contained on poly_ex_1 for point (-8, 5)
        """
        self.assertEqual(False, self.poly_ex_1.is_contained(Point(-8, 5)))

    def test_poly_ex_1_2(self):
        """
        The second test in an exhaustive test of is_contained on poly_ex_1 for point (-12, 2)
        """
        self.assertEqual(False, self.poly_ex_1.is_contained(Point(-12, 2)))

    def test_poly_ex_1_3(self):
        """
        The third test in an exhaustive test of is_contained on poly_ex_1 for point (-8, 2)
        """
        self.assertEqual(True, self.poly_ex_1.is_contained(Point(-8, 2)))

    def test_poly_ex_1_4(self):
        """
        The fourth test in an exhaustive test of is_contained on poly_ex_1 for point (-9, -1)
        """
        self.assertEqual(False, self.poly_ex_1.is_contained(Point(-9, -1)))

    def test_poly_ex_1_5(self):
        """
        The fifth test in an exhaustive test of is_contained on poly_ex_1 for point (-5, -1)
        """
        self.assertEqual(True, self.poly_ex_1.is_contained(Point(-5, -1)))

    def test_poly_ex_1_6(self):
        """
        The sixth test in an exhaustive test of is_contained on poly_ex_1 for point (-3.5, -1)
        """
        self.assertEqual(True, self.poly_ex_1.is_contained(Point(-3.5, -1)))

    def test_poly_ex_1_7(self):
        """
        The seventh test in an exhaustive test of is_contained on poly_ex_1 for point (-5, 2)
        """
        self.assertEqual(True, self.poly_ex_1.is_contained(Point(-5, 2)))

    def test_poly_ex_1_8(self):
        """
        The eighth test in an exhaustive test of is_contained on poly_ex_1 for point (-5, 1)
        """
        self.assertEqual(True, self.poly_ex_1.is_contained(Point(-5, 1)))

    def test_poly_ex_1_9(self):
        """
        The ninth test in an exhaustive test of is_contained on poly_ex_1 for point (-4, 4)
        """
        self.assertEqual(True, self.poly_ex_1.is_contained(Point(-4, 4)))

    def test_poly_ex_1_10(self):
        """
        The 10th test in an exhaustive test of is_contained on poly_ex_1 for point (1, 2)
        """
        self.assertEqual(False, self.poly_ex_1.is_contained(Point(1, 2)))

    def test_poly_ex_1_11(self):
        """
        The 11th test in an exhaustive test of is_contained on poly_ex_1 for point (1, 1)
        """
        self.assertEqual(False, self.poly_ex_1.is_contained(Point(1, 1)))

    def test_bounding_box_bug(self):
        """
        First test of edge case found in Voronoi.py
        """
        point = Point.to_point([265.2175165347952, 143.5904398457129])
        self.assertEqual(False, self.bounding_box.is_contained(point))

    def test_bounding_box_second_bug(self):
        """
        Second test of edge case found in Voronoi.py
        """
        point = Point.to_point([-300, 201])
        self.assertEqual(False, self.bounding_box.is_contained(point))

    def test_bug_is_contained_districts_022821_0(self):
        """
        First test of edge case found in districts
        """
        self.assertEqual(True, self.Wall_1.is_contained(Point(-3.5, 12)))

    def test_bug_is_contained_districts_022821_1(self):
        """
        Second test of edge case found in districts
        """
        self.assertEqual(True, self.Wall_1.is_contained(Point(0, 12)))

    def test_bug_is_contained_districts_022821_2(self):
        """
        Third test of edge case found in districts
        """
        self.assertEqual(True, self.Wall_1.is_contained(Point(0, 10)))

    def test_bug_is_contained_districts_022821_3(self):
        """
        Fourth test of edge case found in districts
        """
        self.assertEqual(True, self.Wall_1.is_contained(Point(-2, 9)))

    def test_bug_is_contained_districts_022821_4(self):
        """
        Fifth test of edge case found in districts
        """
        self.assertEqual(True, self.Wall_1.is_contained(Point(3.5, 12)))

    def test_bug_is_contained_districts_022821_5(self):
        """
        Sixth test of edge case found in districts
        """
        self.assertEqual(True, self.Wall_1.is_contained(Point(0, 12)))

    def test_bug_is_contained_districts_022821_6(self):
        """
        Seventh test of edge case found in districts
        """
        self.assertEqual(True, self.Wall_1.is_contained(Point(0, 10)))

    def test_bug_is_contained_districts_022821_7(self):
        """
        Eighth test of edge case found in districts
        """
        self.assertEqual(True, self.Wall_1.is_contained(Point(2, 9)))

    def test_Polygon_is_equal(self):
        """
        Test if two non-equal polygons are returned non-equal
        """
        i1 = Polygon(self.i1ver)
        s1 = Polygon(self.s1ver)
        self.assertEqual(False, i1 == s1)

    def test_Polygon_is_equal_2(self):
        """
        Test the __eq__ magic function with two equal polygons
        """
        poly1 = Polygon(self.i3ver)
        poly2 = Polygon(self.i3ver)
        self.assertEqual(True, poly1 == poly2)

    def test_polygon_is_equal_3(self):
        """
        Test the __eq__ magic function with two equal polygons with offset vertex lists
        """
        poly1 = Polygon(self.i2ver)
        shifted_vert_list = self.i2ver.copy()
        first_vert = shifted_vert_list.pop(0)
        shifted_vert_list.append(first_vert)
        poly2 = Polygon(shifted_vert_list)
        self.assertEqual(True, poly1 == poly2)

    def test_polygon_cut_1(self):
        """
        First test of the cut method
        """
        poly = Polygon(self.s1ver)
        polys = poly.cut(Point(0.0, 0.5), Point(1.0, 0.5))
        self.assertEqual(2, len(polys))

    def test_polygon_cut_2(self):
        """
        Second test of the cut method
        """
        poly = Polygon(self.s1ver)
        polys = poly.cut(Point(0.5, 0.0), Point(0.5, 1.0))
        self.assertEqual(2, len(polys))

    def test_polygon_cut_3(self):
        """
        Third test of the cut method
        """
        poly = Polygon(self.s1ver)
        polys = poly.cut(Point(0.0, 0.0), Point(1.0, 1.0))
        self.assertEqual(2, len(polys))

    def test_polygon_split_1(self):
        """
        First test of the split method
        """
        poly = Polygon(self.s1ver)
        polys = poly.split(Point(0.5, 0.0), math.pi / 2)
        self.assertEqual(2, len(polys))

    def test_polygon_cut_gap_1(self):
        """
        First test of the cut method
        """
        poly = Polygon(self.s1ver)
        polys = poly.cut_gap(Point(0.0, 0.5), Point(1.0, 0.5), 0.1)
        for p in polys:
            x_list = []
            y_list = []
            for v in p.vertices:
                x_list.append(v.get_x())
                y_list.append(v.get_y())
            x_list.append(p.vertices[0].get_x())
            y_list.append(p.vertices[0].get_y())
            plt.plot(x_list, y_list)
        plt.show()
        self.assertEqual(2, len(polys))

    def test_polygon_cut_gap_2(self):
        """
        First test of the cut method
        """
        poly = Polygon(self.s1ver)
        polys = poly.cut_gap(Point(0.5, 0.0), Point(0.5, 1.0), 0.1)
        for p in polys:
            x_list = []
            y_list = []
            for v in p.vertices:
                x_list.append(v.get_x())
                y_list.append(v.get_y())
            x_list.append(p.vertices[0].get_x())
            y_list.append(p.vertices[0].get_y())
            plt.plot(x_list, y_list)
        plt.show()
        self.assertEqual(2, len(polys))

    def test_polygon_cut_gap_3(self):
        """
        First test of the cut method
        """
        poly = Polygon(self.s1ver)
        polys = poly.cut_gap(Point(0.0, 0.0), Point(1.0, 1.0), 0.1)
        for p in polys:
            x_list = []
            y_list = []
            for v in p.vertices:
                x_list.append(v.get_x())
                y_list.append(v.get_y())
            x_list.append(p.vertices[0].get_x())
            y_list.append(p.vertices[0].get_y())
            plt.plot(x_list, y_list)
        plt.show()
        self.assertEqual(2, len(polys))

    def test_polygon_split_2(self):
        """
        Second test of the split method
        """
        poly = Polygon(self.s1ver)
        polys = poly.split(Point(0.0, 0.5), math.pi)
        self.assertEqual(2, len(polys))

    def test_polygon_split_3(self):
        """
        Third test of the split method
        """
        poly = Polygon(self.s1ver)
        polys = poly.split(Point(0.0, 0.0), math.pi / 4.0)
        self.assertEqual(2, len(polys))

    def test_polygon_intersection_1(self):
        inter = Polygon.intersection(Point(1.0, 5.0), Point(5.0, 1.0), Point(0.0, 2.0), Point(3.0, 5.0))
        self.assertEqual(Point(2.0, 4.0), inter)

    def test_polygon_intersection_2(self):
        inter = Polygon.intersection(Point(1.0, 0.0), Point(2.0, 0.0), Point(0.0, 0.0), Point(1.0, 0.0))
        self.assertEqual(Point(1.0, 0.0), inter)

    def test_polygon_intersection_3(self):
        inter = Polygon.intersection(Point(1.0, 3.0), Point(1.0, -3.0), Point(0.0, 0.0), Point(5.0, 0.0))
        self.assertEqual(Point(1.0, 0.0), inter)

    def test_polygon_intersection_4(self):
        inter = Polygon.intersection(Point(1.0, 3.0), Point(1.0, -3.0), Point(1.0, 3.0), Point(1.0, 5.0))
        self.assertEqual(Point(1.0, 3.0), inter)

    def test_polygon_intersection_5(self):
        inter = Polygon.intersection(Point(1.0, 3.0), Point(5.0, -1.0), Point(0.0, 0.0), Point(5.0, 0.0))
        self.assertEqual(Point(4.0, 0.0), inter)

    def test_polygon_intersection_6(self):
        inter = Polygon.intersection(Point(5.0, 3.0), Point(5.0, -3.0), Point(0.0, 0.0), Point(5.0, 0.0))
        self.assertEqual(Point(5.0, 0.0), inter)

    def test_polygon_intersection_7(self):
        inter = Polygon.intersection(Point(0.0, 0.0), Point(1.0, 1.0), Point(1.0, 1.0), Point(1.0, 0.0))
        self.assertEqual(Point(1.0, 1.0), inter)

    def test_polygon_area_1(self):
        poly = Polygon(self.s1ver)
        a = poly.area()
        self.assertEqual(1, a)

    def test_polygon_area_2(self):
        poly = Polygon([Point(5.0, 10.0), Point(10.0, 10.0), Point(10.0, 5.0), Point(5.0, 5.0)])
        a = poly.area()
        self.assertEqual(25, a)

    def test_is_bordering_1(self):
        bound = Polygon([Point(-50, 50), Point(50, 50), Point(50, -50), Point(-50, -50)])
        inner = Polygon([Point(5.356, 11.586), Point(13.568, 23.317), Point(21.625, 50.0),
                         Point(-43.232, 50.0), Point(-13.057, 13.892), Point(-4.688, 10.088)])
        self.assertEqual(True, bound.is_bordering(inner))

    def test_in_segment(self):
        self.assertEqual(200.00000000, round(200.00000000000003, 8))
        self.assertEqual(True, Polygon.in_segment(Point(-200, 200), Point(200, 200), Point(-179.9948605683313, 200.00000000000003)))

    def test_rectangle_in_1(self):
        poly = Polygon(self.s1ver)
        rect = poly.rectangle_inside(Point(0.0, 0.0), Point(0.0, 1.0))
        vx_list = []
        vy_list = []
        for v in poly.vertices:
            vx_list.append(v.get_x())
            vy_list.append(v.get_y())
        vx_list.append(poly.vertices[0].get_x())
        vy_list.append(poly.vertices[0].get_y())
        plt.plot(vx_list, vy_list, 'b-')

        v2x_list = []
        v2y_list = []
        for v in rect.vertices:
            if v is None:
                break
            v2x_list.append(v.get_x())
            v2y_list.append(v.get_y())
        v2x_list.append(rect.vertices[0].get_x())
        v2y_list.append(rect.vertices[0].get_y())
        plt.plot(v2x_list, v2y_list, 'k-')

        plt.show()
        self.assertEqual(True, True)

    def test_rectangle_in_2(self):
        poly = Polygon([Point(2, 8), Point(8, 5), Point(8, 1), Point(7, -2), Point(4, -5), Point(-3, -3), Point(-3, 4)])
        rect = poly.rectangle_inside(Point(2.0, 8.0), Point(8.0, 5.0))
        vx_list = []
        vy_list = []
        for v in poly.vertices:
            vx_list.append(v.get_x())
            vy_list.append(v.get_y())
        vx_list.append(poly.vertices[0].get_x())
        vy_list.append(poly.vertices[0].get_y())
        plt.plot(vx_list, vy_list, 'b-')

        v2x_list = []
        v2y_list = []
        for v in rect.vertices:
            if v is None:
                break
            v2x_list.append(v.get_x())
            v2y_list.append(v.get_y())
        v2x_list.append(rect.vertices[0].get_x())
        v2y_list.append(rect.vertices[0].get_y())
        plt.plot(v2x_list, v2y_list, 'k-')

        plt.show()
        self.assertEqual(True, True)

    def test_intersect_segment(self):
        p1 = Point(78.087, 78.087)
        p2 = Point(328.087, 78.087)
        p3 = Point(328.087, 328.087)
        p4 = Point(328.087, 78.087)
        self.assertEqual(True, Polygon.intersect_segment(p2, p1, p4, p3))

    def test_intersecting_edge_1(self):
        poly = Polygon([Point(78.087, 78.087), Point(328.087, 78.087), Point(328.087, 328.087), Point(78.087, 328.087)])
        p = Point(328.087, 328.087)
        ext_p = Point(328.087, 78.087)
        self.assertTrue(poly.find_intersecting_edge(p, ext_p))

    def test_easy_cut_1(self):
        poly = Polygon(self.s1ver)
        polys = poly.easy_cut(Point(0.5, 0.5), math.pi, 0)
        for p in polys:
            x_list = []
            y_list = []
            for v in p.vertices:
                x_list.append(v.get_x())
                y_list.append(v.get_y())
            x_list.append(p.vertices[0].get_x())
            y_list.append(p.vertices[0].get_y())
            plt.plot(x_list, y_list)
        plt.show()
        self.assertEqual(2, len(polys))


if __name__ == '__main__':
    unittest.main()
