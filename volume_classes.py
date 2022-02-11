from main_classes import Volume, tan, pi, radians


class Cube(Volume):
    _param_len = 1
    def __init__(self, a):
        self.a = a
        self.b = a
        self.h = a

    @property
    def area(self):
        return round(6 * self.a * self.b, 2)

    @property
    def volume(self):
        return round(self.main_area * self.h, 2)


class Parallelepiped(Cube):
    _param_len = 3
    def __init__(self, a, b, h):
        super().__init__(a)
        self.b = b
        self.h = h

    @property
    def area(self):
        return round(2 * (self.a * self.b + self.b * self.h + self.a * self.h), 2)


class Pyramid(Volume):
    _param_len = 3
    def __init__(self, a, n, h):  # a - длина стороны, n - кол-во граней, h - высота пирамиды
        self.a = a
        self.n = n
        self.h = h

    @property
    def area(self):
        tg = tan(radians(180 / self.n))
        arg1 = self.a / 2 / tg
        arg2 = self.h ** 2 + (self.a / (2 * tg)) ** 2
        area = self.n * self.a / 2 * (arg1 + arg2 ** 0.5)
        return round(area, 3)

    @property
    def volume(self):
        tg = tan(radians(180 / self.n))
        volume = self.n * self.a ** 2 * self.h / (12 * tg)
        return round(volume, 3)


class Orb(Volume):
    _param_len = 1
    def __init__(self, r):
        self.r = r

    @property
    def area(self):
        return round(4 * pi * self.r ** 2, 3)

    @property
    def volume(self):
        return round(4 / 3 * pi * self.r ** 3, 3)


class Cylinder(Volume):
    _param_len = 2
    def __init__(self, r, h):
        self.r = r
        self.h = h

    @property
    def area(self):
        return round(2 * pi * self.r * (self.r + self.h), 3)

    @property
    def volume(self):
        return round(pi * self.r ** 2 * self.h * self._h, 3)


class Conus(Cylinder):
    _h = 1 / 3
    _param_len = 2

    def __init__(self, r, h):
        super().__init__(r, h)

    @property
    def area(self):
        return round(pi * self.r * (self.r + (self.r ** 2 + self.h ** 2) ** 0.5), 3)
