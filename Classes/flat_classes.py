from Classes.main_classes import Flat, pi


class Square(Flat):
    param_len = 1

    def __init__(self, a):
        self.a = a
        self.b = a

    @property
    def get_params(self):
        return self.a


class Rectangle(Square):
    param_len = 2

    def __init__(self, a, b):
        super().__init__(a)
        self.b = b

    @property
    def get_params(self):
        return self.a, self.b


class Rhomb(Square):
    param_len = 2

    def __init__(self, a, grad):
        super().__init__(a)
        self.grad = grad

    @property
    def get_params(self):
        return self.a, self.grad


class Trapese(Rectangle):
    param_len = 3

    def __init__(self, a, b, h):
        super().__init__(a, b)
        self.h = h

    @property
    def get_params(self):
        return self.a, self.b, self.h

    @property
    def area(self):
        return round((self.a + self.b) / 2 * self.h, 2)


class Triangle(Rectangle):
    param_len = 3

    def __init__(self, a, b, grad):
        super().__init__(a, b)
        self.grad = grad

    @property
    def get_h(self):
        return self._h / 2

    @property
    def get_params(self):
        return self.a, self.b, self.grad


class Circle(Flat):
    param_len = 1

    def __init__(self, r):
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
