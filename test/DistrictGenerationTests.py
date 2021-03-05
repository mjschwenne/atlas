import unittest

from src.Backend.Point import Point
from src.Backend.Region import Region
from src.Backend.District import Armory
import matplotlib.pyplot as plt

class DistrictGenerationTests(unittest.TestCase):

    def test_basic_district_Generation(self):
        a = Armory(0.1, 0.8, 25)
        r = Region(a, [Point(0.0, 0.0), Point(0.0, 10.0), Point(10.0, 10.0), Point(10.0, 0.0)], False, False)
        r.get_district().generate_district(r)
        buildings = r.buildings

        vx_list = []
        vy_list = []
        for v in r.vertices:
            vx_list.append(v.get_x())
            vy_list.append(v.get_y())
        for b in buildings:
            x_list = []
            y_list = []
            for p in b.vertices:
                x_list.append(p.get_x())
                y_list.append(p.get_y())
            x_list.append(b.vertices[0].get_x())
            y_list.append(b.vertices[0].get_y())
            plt.plot(x_list, y_list, 'k-')

        vx_list.append(r.vertices[0].get_x())
        vy_list.append(r.vertices[0].get_y())
        plt.plot(vx_list, vy_list, 'b-')
        plt.show()
        self.assertEqual(True, True)
