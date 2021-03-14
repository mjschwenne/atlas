import unittest

from src.Backend.Point import Point
from src.Backend.Region import Region
from src.Backend.District import Armory
import matplotlib.pyplot as plt


class DistrictGenerationTests(unittest.TestCase):

    def test_basic_district_Generation_1(self):
        a = Armory(0.1, 0, 10)
        r = Region(a, [Point(0.0, 0.0), Point(0.0, 10.0), Point(10.0, 10.0), Point(10.0, 0.0)], False, False)
        r.get_district().generate_district(r)
        buildings = r.buildings

        vx_list = []
        vy_list = []
        for v in r.vertices:
            vx_list.append(v.get_x())
            vy_list.append(v.get_y())
        vx_list.append(r.vertices[0].get_x())
        vy_list.append(r.vertices[0].get_y())
        plt.plot(vx_list, vy_list, 'b-')
        for b in buildings:
            x_list = []
            y_list = []
            for p in b.vertices:
                x_list.append(p.get_x())
                y_list.append(p.get_y())
            x_list.append(b.vertices[0].get_x())
            y_list.append(b.vertices[0].get_y())
            plt.plot(x_list, y_list, 'k-')
        plt.show()
        self.assertEqual(True, True)

    def test_basic_district_Generation_2(self):
        a = Armory(0.5, 0, 25)
        r = Region(a, [Point(0.0, 0.0), Point(0.0, 5.0), Point(10.0, 10.0), Point(7.0, 0.0)], False, False)
        r.get_district().generate_district(r)
        buildings = r.buildings

        vx_list = []
        vy_list = []
        for v in r.vertices:
            vx_list.append(v.get_x())
            vy_list.append(v.get_y())
        vx_list.append(r.vertices[0].get_x())
        vy_list.append(r.vertices[0].get_y())
        plt.plot(vx_list, vy_list, 'b-')
        for b in buildings:
            x_list = []
            y_list = []
            for p in b.vertices:
                x_list.append(p.get_x())
                y_list.append(p.get_y())
            x_list.append(b.vertices[0].get_x())
            y_list.append(b.vertices[0].get_y())
            plt.plot(x_list, y_list, 'k-')
        plt.show()
        self.assertEqual(True, True)

    def test_basic_district_Generation_3(self):
        a = Armory(0.5, 0, 25)
        r = Region(a, [Point(0.0, 0.0), Point(0.0, 100.0), Point(100.0, 100.0), Point(100.0, 0.0)], False, False)
        r.get_district().generate_district(r)
        buildings = r.buildings

        vx_list = []
        vy_list = []
        for v in r.vertices:
            vx_list.append(v.get_x())
            vy_list.append(v.get_y())
        vx_list.append(r.vertices[0].get_x())
        vy_list.append(r.vertices[0].get_y())
        plt.plot(vx_list, vy_list, 'b-')
        for b in buildings:
            x_list = []
            y_list = []
            for p in b.vertices:
                x_list.append(p.get_x())
                y_list.append(p.get_y())
            x_list.append(b.vertices[0].get_x())
            y_list.append(b.vertices[0].get_y())
            plt.plot(x_list, y_list, 'k-')
        plt.show()
        self.assertEqual(True, True)

    def test_basic_district_Generation_4(self):
        a = Armory(0.5, 0.1, 1000)
        r = Region(a, [Point(100.0, 700.0), Point(600.0, 500.0), Point(600.0, 100.0), Point(500.0, -200.0),
                       Point(200.0, -300.0), Point(-200.0, -200.0), Point(-400.0, 200.0)], False, False)
        r.get_district().generate_district(r)
        buildings = r.buildings

        vx_list = []
        vy_list = []
        for v in r.vertices:
            vx_list.append(v.get_x())
            vy_list.append(v.get_y())
        vx_list.append(r.vertices[0].get_x())
        vy_list.append(r.vertices[0].get_y())
        plt.plot(vx_list, vy_list, 'b-')
        for b in buildings:
            x_list = []
            y_list = []
            for p in b.vertices:
                x_list.append(p.get_x())
                y_list.append(p.get_y())
            x_list.append(b.vertices[0].get_x())
            y_list.append(b.vertices[0].get_y())
            plt.plot(x_list, y_list, 'k-')
        plt.show()
        self.assertEqual(True, True)