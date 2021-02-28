from src.Backend.Constructor import Constructor
from src.Backend.Point import Point
from src.Backend.Polygon import Polygon
from src.Backend.Region import Region
from src.Backend.Wall import Wall


class DemoStuff:
    # 12Sided
    # =======
    ver0 = [Point(0, 0), Point(-2, 1), Point(-4, 3), Point(-5, 5), Point(-4, 7), Point(-2, 9), Point(0, 10),
            Point(2, 9), Point(4, 7), Point(5, 5), Point(4, 3), Point(2, 1)]
    reg0 = Region(None, ver0, False, False)

    # others
    # ======
    ver1 = [Point(-3.5, 12), Point(0, 12), Point(0, 10), Point(-2, 9)]
    reg1 = Region(None, ver1, False, False)

    ver2 = [Point(3.5, 12), Point(0, 12), Point(0, 10), Point(2, 9)]
    reg2 = Region(None, ver2, False, False)

    ver3 = [Point(-3.5, 12), Point(-6, 8), Point(-4, 7), Point(-2, 9)]
    reg3 = Region(None, ver3, False, False)

    ver4 = [Point(3.5, 12), Point(6, 8), Point(4, 7), Point(2, 9)]
    reg4 = Region(None, ver4, True, False)

    ver5 = [Point(-6, 5), Point(-6, 8), Point(-4, 7), Point(-5, 5)]
    reg5 = Region(None, ver5, False, False)

    ver6 = [Point(6, 5), Point(6, 8), Point(4, 7), Point(5, 5)]
    reg6 = Region(None, ver6, False, False)

    ver7 = [Point(-6, 5), Point(-6, 2), Point(-4, 3), Point(-5, 5)]
    reg7 = Region(None, ver7, False, False)

    ver8 = [Point(6, 5), Point(6, 2), Point(4, 3), Point(5, 5)]
    reg8 = Region(None, ver8, False, False)

    ver9 = [Point(-3.5, -2), Point(-6, 2), Point(-4, 3), Point(-2, 1)]
    reg9 = Region(None, ver9, False, False)

    ver10 = [Point(3.5, -2), Point(6, 2), Point(4, 3), Point(2, 1)]
    reg10 = Region(None, ver9, False, False)

    ver11 = [Point(-3.5, -2), Point(0, -2), Point(0, 0), Point(-2, 1)]
    reg11 = Region(None, ver11, False, False)

    ver12 = [Point(3.5, -2), Point(0, -2), Point(0, 0), Point(2, 1)]
    reg12 = Region(None, ver11, False, False)

    ver13 = [Point(-6, 8), Point(-6, 12), Point(-3.5, 12)]
    reg13 = Region(None, ver13, False, False)

    ver14 = [Point(6, 8), Point(6, 12), Point(3.5, 12)]
    reg14 = Region(None, ver14, False, False)

    ver15 = [Point(-6, -2), Point(-6, 2), Point(-3.5, -2)]
    reg15 = Region(None, ver15, False, False)

    ver16 = [Point(6, -2), Point(6, 2), Point(3.5, -2)]
    reg16 = Region(None, ver16, False, False)

    ver17 = [Point(-6, -2), Point(-6, 2), Point(-8, 2)]
    reg17 = Region(None, ver17, False, False)

    ver18 = [Point(6, -2), Point(6, 2), Point(8, 2)]
    reg18 = Region(None, ver18, False, False)

    ver19 = [Point(-6, -2), Point(0, -2), Point(0, -4)]
    reg19 = Region(None, ver19, False, False)

    ver20 = [Point(6, -2), Point(0, -2), Point(0, -4)]
    reg20 = Region(None, ver20, False, False)

    ver21 = [Point(6, 12), Point(0, 12), Point(0, 14)]
    reg21 = Region(None, ver21, False, False)

    ver22 = [Point(-6, 12), Point(0, 12), Point(0, 14)]
    reg22 = Region(None, ver22, False, False)

    ver23 = [Point(-6, 8), Point(-6, 12), Point(-8, 8)]
    reg23 = Region(None, ver23, False, False)

    ver24 = [Point(6, 8), Point(6, 12), Point(8, 8)]
    reg24 = Region(None, ver24, False, False)

    ver25 = [Point(-6, 2), Point(-6, 5), Point(-9, 5), Point(-8, 2)]
    reg25 = Region(None, ver25, False, False)

    ver26 = [Point(6, 2), Point(6, 5), Point(9, 5), Point(8, 2)]
    reg26 = Region(None, ver26, False, False)

    ver27 = [Point(-6, 8), Point(-6, 5), Point(-9, 5), Point(-8, 8)]
    reg27 = Region(None, ver27, False, False)

    ver28 = [Point(6, 8), Point(6, 5), Point(9, 5), Point(8, 8)]
    reg28 = Region(None, ver28, False, False)

    # List of Regions
    regList = [reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg0, reg13, reg14, reg15,
               reg16, reg17, reg18, reg19, reg20, reg21, reg22, reg23, reg24, reg25, reg26, reg27, reg28]

    # wall
    verWall = [Point(3.5, -2), Point(6, 2), Point(6, 8), Point(3.5, 12), Point(-3.5, 12), Point(-6, 8),
               Point(-6, 2), Point(-3.5, -2)]
    wall = Wall([reg0])
    wall.set_vertices(verWall)
    wall.set_gates([Point(-6, 4), Point(6, 4), Point(-2, -2)])

    # city
    verCity = [Point(-6, 12), Point(-6, -2), Point(6, -2), Point(6, 12)]
    polyCity = Polygon(verCity)

    def assign_districts(self):
        Constructor().assign_districts(self.regList, self.wall, self.polyCity)
        return self.regList

