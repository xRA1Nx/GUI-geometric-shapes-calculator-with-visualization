from Classes.main_classes import Volume, tan, pi, radians
import numpy as np


class Cube(Volume):
    name = "куб"
    param_len = 1
    label_a = "сторона a, мм:"
    draw_type = 3

    def __init__(self, a=0):
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
    name = "параллелипипед"
    param_len = 3
    label_a = "сторона a, мм:"
    label_b = "сторона b, мм:"
    label_c = "высота h, мм:"
    draw_type = 2

    def __init__(self, a=0, b=0, h=0):
        super().__init__(a)
        self.b = b
        self.h = h

    @property
    def area(self):
        return round(2 * (self.a * self.b + self.b * self.h + self.a * self.h), 2)

    @property
    def get_points(self):
        points = np.array([[-1, -1, -1],
                           [1, -1, -1],
                           [1, 1, -1],
                           [-1, 1, -1],
                           [-1, -1, 1],
                           [1, -1, 1],
                           [1, 1, 1],
                           [-1, 1, 1]])
        p = [[2.06498904e-01, -6.30755443e-07, 1.07477548e-03],
             [1.61535574e-06, 1.18897198e-01, 7.85307721e-06],
             [7.08353661e-02, 4.48415767e-06, 2.05395893e-01]]
        z = np.zeros((8, 3))
        for i in range(8):
            z[i, :] = np.dot(points[i, :], p)
        z = 10.0 * z
        verts = [[z[0], z[1], z[2], z[3]],
                 [z[4], z[5], z[6], z[7]],
                 [z[0], z[1], z[5], z[4]],
                 [z[2], z[3], z[7], z[6]],
                 [z[1], z[2], z[6], z[5]],
                 [z[4], z[7], z[3], z[0]]]
        return z, verts


class Pyramid(Volume):
    name = "пирамида"
    param_len = 3
    label_a = "сторона a, мм:"
    label_b = "кол-во граней, шт:"
    label_c = "высота, мм:"
    draw_type = 2

    def __init__(self, a=0, n=0, h=0):  # a - длина стороны, n - кол-во граней, h - высота пирамиды
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

    @property
    def get_points(self):
        v = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [0, 0, 1]])
        verts = [[v[0], v[1], v[4]], [v[0], v[3], v[4]],
                 [v[2], v[1], v[4]], [v[2], v[3], v[4]], [v[0], v[1], v[2], v[3]]]
        return v, verts


class Orb(Volume):
    name = "сфера"
    param_len = 1
    label_a = "радиус R, мм:"
    draw_type = 1

    def __init__(self, r=0):
        self.r = r

    @property
    def area(self):
        return round(4 * pi * self.r ** 2, 3)

    @property
    def volume(self):
        return round(4 / 3 * pi * self.r ** 3, 3)

    @property
    def get_points(self):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        return x, y, z


class Cylinder(Volume):
    name = "цилиндр"
    param_len = 2
    label_a = "радиус R, мм:"
    label_b = "высота h, мм:"
    draw_type = 1

    def __init__(self, r=0, h=0):
        self.r = r
        self.h = h

    @property
    def area(self):
        return round(2 * pi * self.r * (self.r + self.h), 3)

    @property
    def volume(self):
        return round(pi * self.r ** 2 * self.h * self._h, 3)

    @property
    def get_points(self):
        u = np.linspace(0, 2 * np.pi, 50)  # разделить круг на 50 углов
        h = np.linspace(0, 1, 20)  # Разделить высоту 1 на 20 равных частей
        x = np.outer(np.sin(u), np.ones(len(h)))  # значение x повторяется 20 раз
        y = np.outer(np.cos(u), np.ones(len(h)))  # значение y повторяется 20 раз
        z = np.outer(np.ones(len(u)), h)  # высота, соответствующая x, y
        return x, y, z


class Conus(Cylinder):
    name = "конус"
    _h = 1 / 3
    param_len = 2
    draw_type = 1

    def __init__(self, r=0, h=0):
        super().__init__(r, h)

    @property
    def area(self):
        return round(pi * self.r * (self.r + (self.r ** 2 + self.h ** 2) ** 0.5), 3)

    @property
    def get_points(self):
        theta = np.linspace(0, 2 * np.pi, 100)
        lin = np.linspace(-1, 0, 100)
        t, r = np.meshgrid(theta, lin)
        x = r * np.cos(t)
        y = r * np.sin(t)
        z = (1 + r)
        return x, y, z


volume_figurs = {"сфера": Orb,
                 "куб": Cube,
                 "параллелепипед": Parallelepiped,
                 "пирамида": Pyramid,
                 "цилиндр": Cylinder,
                 "конус": Conus,
                 }
