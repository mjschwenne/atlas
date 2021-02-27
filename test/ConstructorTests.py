import unittest

from src.Backend.Constructor import Constructor
from src.Backend.District import *
from src.Backend.Point import Point
from src.Backend.Polygon import Polygon
from src.Backend.Region import Region
from src.Backend.Wall import Wall


class ConstructorTests(unittest.TestCase):
    # 12Sided
    # =======
    ver0 = [Point(0, 0), Point(-2, 1), Point(-4, 3), Point(-5, 5), Point(-4, 7), Point(-2, 9), Point(0, 10),
            Point(2, 9), Point(4, 7), Point(5, 5), Point(4, 3), Point(2, 1)]
    reg0 = Region(None, ver0, False, False)

    # others
    # ======
    ver1 = [Point(-3.5, 12), Point(0, 12), Point(0, 10), Point(-2, 9)]
    reg1 = Region(Armory(0, 0, 0), ver1, False, False)

    ver2 = [Point(3.5, 12), Point(0, 12), Point(0, 10), Point(2, 9)]
    reg2 = Region(Castle(0, 0, 0), ver2, False, False)

    ver3 = [Point(-3.5, 12), Point(-6, 8), Point(-4, 7), Point(-2, 9)]
    reg3 = Region(Cathedral(0, 0, 0), ver3, False, False)

    ver4 = [Point(3.5, 12), Point(6, 8), Point(4, 7), Point(2, 9)]
    reg4 = Region(Docks(0, 0, 0), ver4, True, False)

    ver5 = [Point(-6, 5), Point(-6, 8), Point(-4, 7), Point(-5, 5)]
    reg5 = Region(Farmland(0, 0, 0), ver5, False, False)

    ver6 = [Point(6, 5), Point(6, 8), Point(4, 7), Point(5, 5)]
    reg6 = Region(Gate(0, 0, 0), ver6, False, False)

    ver7 = [Point(-6, 5), Point(-6, 2), Point(-4, 3), Point(-5, 5)]
    reg7 = Region(Housing(0, 0, 0), ver7, False, False)

    ver8 = [Point(6, 5), Point(6, 2), Point(4, 3), Point(5, 5)]
    reg8 = Region(Market(0, 0, 0), ver8, False, False)

    ver9 = [Point(-3.5, -2), Point(-6, 2), Point(-4, 3), Point(-2, 1)]
    reg9 = Region(Precinct(0, 0, 0), ver9, False, False)

    ver10 = [Point(3.5, -2), Point(6, 2), Point(4, 3), Point(2, 1)]
    reg10 = Region(Slum(0, 0, 0), ver9, False, False)

    ver11 = [Point(-3.5, -2), Point(0, -2), Point(0, 0), Point(-2, 1)]
    reg11 = Region(Smithing(0, 0, 0), ver11, False, False)

    ver12 = [Point(3.5, -2), Point(0, -2), Point(0, 0), Point(2, 1)]
    reg12 = Region(WarCamp(0, 0, 0), ver11, False, False)

    # Castle
    regList = [reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg0]

    # wall
    verWall = [Point(3.5, -2), Point(6, 2), Point(6, 8), Point(3.5, 12), Point(-3.5, 12), Point(-6, 8), Point(-4, 7),
               Point(-5, 5), Point(-6, 5), Point(-6, 2), Point(-3.5, -2)]
    wall = Wall([reg0])
    wall.set_vertices(verWall)
    wall.set_gates([Point(-4.5, 6)])

    # city
    verCity = [Point(3.5, -2), Point(6, 2), Point(6, 8), Point(3.5, 12), Point(-3.5, 12), Point(-6, 8),
               Point(-6, 2), Point(-3.5, -2)]
    polyCity = Polygon(verCity)

    def test_assign_districts(self):
        Constructor().assign_districts(self.regList, self.wall, self.polyCity)
        for reg in self.regList:
            print(reg.get_district())
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
