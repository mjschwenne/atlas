import unittest
from src.Backend.Point import Point
from src.Backend.District import *
from src.Backend.Polygon import Polygon
from src.Backend.Wall import Wall


class DistrictTests(unittest.TestCase):
    # 12Sided
    # =======
    ver13 = [Point(0, 0), Point(-2, 1), Point(-4, 3), Point(-5, 5), Point(-4, 7), Point(-2, 9), Point(0, 10),
             Point(2, 9), Point(4, 7), Point(5, 5), Point(4, 3), Point(2, 1)]
    reg13 = Region(None, ver13, False, False)
    # is Water
    ver14 = [Point(0, 0), Point(-2, 1), Point(-4, 3), Point(-5, 5), Point(-4, 7), Point(-2, 9), Point(0, 10),
             Point(2, 9), Point(4, 7), Point(5, 5), Point(4, 3), Point(2, 1)]
    reg14 = Region(None, ver13, True, False)

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
    reg7 = Region(HousingMid(0, 0, 0), ver7, False, False)

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
    regList = [reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14]
    # No Castle
    regList2 = [reg1, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14]

    # wall
    verWall = [Point(3.5, -2), Point(6, 2), Point(6, 8), Point(3.5, 12), Point(-3.5, 12), Point(-6, 8), Point(-4, 7),
               Point(-5, 5), Point(-6, 5), Point(-6, 2), Point(-3.5, -2)]
    wall = Wall([reg13])
    wall.set_vertices(verWall)
    wall.set_gates([Point(-4.5, 6)])

    # wall no gate
    wall2 = Wall([reg13])
    wall2.set_vertices(verWall)
    wall2.set_gates([])

    # city
    verCity = [Point(3.5, -2), Point(6, 2), Point(6, 8), Point(3.5, 12), Point(-3.5, 12), Point(-6, 8),
               Point(-6, 2), Point(-3.5, -2)]
    polyCity = Polygon(verCity)

    def test_Armory(self):
        self.assertEqual(80, Armory.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Castle_with_Castle(self):
        self.assertEqual(-10000, Castle.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Castle_with_out_Castle(self):
        self.assertEqual(0, Castle.determine_rating(self.reg13, self.regList2, self.wall, self.polyCity))

    def test_Cathedral(self):
        self.assertEqual(30, Cathedral.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Dock_with_Water(self):
        self.assertEqual(50, Docks.determine_rating(self.reg14, self.regList, self.wall, self.polyCity))

    def test_Dock_with_out_Water(self):
        self.assertEqual(-1000, Docks.determine_rating(self.reg13, self.regList2, self.wall, self.polyCity))

    def test_Farmland(self):
        self.assertEqual(-1000, Farmland.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Gate_with_Gate(self):
        self.assertEqual(60, Gate.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Gate_with_out_Gate(self):
        self.assertEqual(-1000, Gate.determine_rating(self.reg13, self.regList, self.wall2, self.polyCity))

    def test_Housing(self):
        self.assertEqual(70, HousingMid.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Market(self):
        self.assertEqual(100, Market.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Precinct(self):
        self.assertEqual(60, Precinct.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Slum(self):
        self.assertEqual(-1010, Slum.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_Smithing(self):
        self.assertEqual(130, Smithing.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))

    def test_WarCamp(self):
        self.assertEqual(-1000, WarCamp.determine_rating(self.reg13, self.regList, self.wall, self.polyCity))


