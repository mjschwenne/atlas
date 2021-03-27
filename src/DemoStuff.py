from src.Backend.Constructor import Constructor
from src.Backend.District import Armory, BasicDistrict, HousingMid, Slum
from src.Backend.Point import Point
from src.Backend.Polygon import Polygon
from src.Backend.Region import Region
from src.Backend.Infrastructure import Infrastructure


class DemoStuff:
    # 12Sided
    # =======
    ver0 = [Point(0, 0), Point(-200, 100), Point(-400, 300), Point(-500, 500), Point(-400, 700), Point(-200, 900), Point(0, 1000),
            Point(200, 900), Point(400, 700), Point(500, 500), Point(400, 300), Point(200, 100)]
    reg0 = Region(None, ver0, False, False)

    # others
    # ======
    ver1 = [Point(-350, 1200), Point(0, 1200), Point(0, 1000), Point(-200, 900)]
    reg1 = Region(None, ver1, False, False)

    ver2 = [Point(350, 1200), Point(0, 1200), Point(0, 1000), Point(200, 900)]
    reg2 = Region(None, ver2, False, False)

    ver3 = [Point(-350, 1200), Point(-600, 800), Point(-400, 700), Point(-200, 900)]
    reg3 = Region(None, ver3, False, False)

    ver4 = [Point(350, 1200), Point(600, 800), Point(400, 700), Point(200, 900)]
    reg4 = Region(None, ver4, True, False)

    ver5 = [Point(-600, 500), Point(-600, 800), Point(-400, 700), Point(-500, 500)]
    reg5 = Region(None, ver5, False, False)

    ver6 = [Point(600, 500), Point(600, 800), Point(400, 700), Point(500, 500)]
    reg6 = Region(None, ver6, False, False)

    ver7 = [Point(-600, 500), Point(-600, 200), Point(-400, 300), Point(-500, 500)]
    reg7 = Region(None, ver7, False, False)

    ver8 = [Point(600, 500), Point(600, 200), Point(400, 300), Point(500, 500)]
    reg8 = Region(None, ver8, False, False)

    ver9 = [Point(-350, -200), Point(-600, 200), Point(-400, 300), Point(-200, 100)]
    reg9 = Region(None, ver9, False, False)

    ver10 = [Point(350, -200), Point(600, 200), Point(400, 300), Point(200, 100)]
    reg10 = Region(None, ver10, False, False)

    ver11 = [Point(-350, -200), Point(0, -200), Point(0, 0), Point(-200, 100)]
    reg11 = Region(None, ver11, False, False)

    ver12 = [Point(350, -200), Point(0, -200), Point(0, 0), Point(200, 100)]
    reg12 = Region(None, ver12, False, False)

    ver13 = [Point(-600, 800), Point(-600, 1200), Point(-350, 1200)]
    reg13 = Region(None, ver13, False, False)

    ver14 = [Point(600, 800), Point(600, 1200), Point(350, 1200)]
    reg14 = Region(None, ver14, False, False)

    ver15 = [Point(-600, -200), Point(-600, 200), Point(-350, -200)]
    reg15 = Region(None, ver15, False, False)

    ver16 = [Point(600, -200), Point(600, 200), Point(350, -200)]
    reg16 = Region(None, ver16, False, False)

    ver17 = [Point(-600, -200), Point(-600, 200), Point(-800, 200)]
    reg17 = Region(None, ver17, False, False)

    ver18 = [Point(600, -200), Point(600, 200), Point(800, 200)]
    reg18 = Region(None, ver18, False, False)

    ver19 = [Point(-600, -200), Point(0, -200), Point(0, -400)]
    reg19 = Region(None, ver19, False, False)

    ver20 = [Point(600, -200), Point(0, -200), Point(0, -400)]
    reg20 = Region(None, ver20, False, False)

    ver21 = [Point(600, 1200), Point(0, 1200), Point(0, 1400)]
    reg21 = Region(None, ver21, False, False)

    ver22 = [Point(-600, 1200), Point(0, 1200), Point(0, 1400)]
    reg22 = Region(None, ver22, False, False)

    ver23 = [Point(-600, 800), Point(-600, 1200), Point(-800, 800)]
    reg23 = Region(None, ver23, False, False)

    ver24 = [Point(600, 800), Point(600, 1200), Point(800, 800)]
    reg24 = Region(None, ver24, False, False)

    ver25 = [Point(-600, 200), Point(-600, 500), Point(-900, 500), Point(-800, 200)]
    reg25 = Region(None, ver25, False, False)

    ver26 = [Point(600, 200), Point(600, 500), Point(900, 500), Point(800, 200)]
    reg26 = Region(None, ver26, False, False)

    ver27 = [Point(-600, 800), Point(-600, 500), Point(-900, 500), Point(-800, 800)]
    reg27 = Region(None, ver27, False, False)

    ver28 = [Point(600, 800), Point(600, 500), Point(900, 500), Point(800, 800)]
    reg28 = Region(None, ver28, False, False)

    # List of Regions
    regList = [reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg0, reg13, reg14, reg15,
               reg16, reg17, reg18, reg19, reg20, reg21, reg22, reg23, reg24, reg25, reg26, reg27, reg28]

    # wall
    verWall = [Point(350, -200), Point(600, 200), Point(600, 800), Point(350, 1200), Point(-350, 1200), Point(-600, 800),
               Point(-600, 200), Point(-350, -200)]
    wall = Infrastructure([reg0])
    wall.set_vertices(verWall)
    wall.set_gates([Point(-600, 400), Point(600, 400), Point(-200, -200)])

    # city
    ver_city = [Point(-600, 1200), Point(-600, -200), Point(600, -200), Point(600, 1200)]
    poly_city = Polygon(ver_city)

    def assign_districts(self):
        for reg in self.regList:
            reg.buildings = []
        Constructor.assign_districts(self.regList, self.wall, self.poly_city)
        for reg in self.regList:
            if isinstance(reg.get_district(), BasicDistrict):
                reg.get_district().generate_district(reg)
        return self.regList

