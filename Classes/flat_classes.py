from PyQt5.QtCore import QPoint

from Classes.main_classes import Flat, pi, sin, cos, radians


class Square(Flat):
    name = "квадрат"
    param_len = 1
    label_a = "сторона a, мм:"
    draw_type = 1

    def __init__(self, a=0):
        self.a = a
        self.b = a

    @property
    def get_params(self):
        return self.a

    @property
    def draw_now(self):
        return


class Rectangle(Square):
    name = "прямоугольник"
    param_len = 2
    label_a = "сторона a, мм:"
    label_b = "сторона b, мм:"
    draw_type = 1

    def __init__(self, a=0, b=0):
        super().__init__(a)
        self.b = b

    @property
    def get_params(self):
        return self.a, self.b

    @property
    def get_points(self):
        gr = self.grad
        def_x = 130
        def_y = 70
        point_b_x = int(def_x + self.b * sin(radians(gr)) * 10)
        point_b_y = int(def_y + self.b * cos(radians(gr)) * 10)
        points = [QPoint(def_x, def_y),
                  QPoint(def_x, def_y + int(self.a * 10)),
                  QPoint(point_b_x, point_b_y)]
        return points


class Rhomb(Square):
    name = "ромб"
    param_len = 2
    label_a = "сторона a, мм:"
    label_b = "угол, º:"
    draw_type = 2

    def __init__(self, a=0, grad=0):
        super().__init__(a)
        self.grad = grad

    @property
    def get_params(self):
        return self.a, self.grad

    @property
    def get_points(self):
        gr = self.grad
        def_x = 80
        def_y = 30
        point_a_x = int(def_x + self.a * sin(radians(90 - gr)) * 10)
        point_a_y = int(def_y + self.a * cos(radians(90 - gr)) * 10)
        points = [QPoint(def_x, def_y),
                  QPoint(def_x + int(self.a * 10), def_y),
                  QPoint(point_a_x + int(self.a * 10), point_a_y),
                  QPoint(point_a_x, point_a_y),
                  ]
        return points


class Trapese(Rectangle):
    name = "трапеция"
    param_len = 3
    label_a = "сторона a, мм:"
    label_b = "сторона b, мм:"
    label_c = "высота h, мм:"
    draw_type = 2

    def __init__(self, a=0, b=0, h=0):
        super().__init__(a, b)
        self.h = h

    @property
    def get_params(self):
        return self.a, self.b, self.h

    @property
    def area(self):
        return round((self.a + self.b) / 2 * self.h, 2)

    @property
    def get_points(self):
        def_x = 80
        def_y = 30
        points = [QPoint(def_x, def_y),
                  QPoint(def_x + int(self.a * 10), def_y),
                  QPoint(def_x + int(self.b * 10), def_y + int(self.h * 10)),
                  QPoint(def_x - 50, def_y + int(self.h * 10))]
        return points


class Triangle(Rectangle):
    name = "треугольник"
    param_len = 3
    label_a = "сторона a, мм:"
    label_b = "сторона b, мм:"
    label_c = "угол, º:"
    draw_type = 2

    def __init__(self, a=0, b=0, grad=0):
        super().__init__(a, b)
        self.grad = grad

    @property
    def get_h(self):
        return self._h / 2

    @property
    def get_params(self):
        return self.a, self.b, self.grad


class Circle(Flat):
    name = "круг"
    param_len = 1
    label_a = "радиус R, мм:"
    draw_type = 3

    def __init__(self, r=0):
        self.r = r

    @property
    def get_params(self):
        return self.r

    @property
    def area(self):
        return round(pi * self.r ** 2, 2)


flat_figurs = {"круг": Circle,
               "квадрат": Square,
               "прямоугольник": Rectangle,
               "треугольник": Triangle,
               "трапеция": Trapese,
               "ромб": Rhomb,
               }
