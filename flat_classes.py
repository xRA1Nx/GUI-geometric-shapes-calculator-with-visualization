from main_classes import Flat, pi


class Square(Flat):
    _param_len = 1
    def __init__(self, a):
        self.a = a
        self.b = a


class Rectangle(Square):
    _param_len = 2
    def __init__(self, a, b):
        super().__init__(a)
        self.b = b


class Rhomb(Square):
    _param_len = 2
    def __init__(self, a, grad):
        super().__init__(a)
        self.grad = grad


class Trapese(Rectangle):
    _param_len = 3
    def __init__(self, a, b, h):
        super().__init__(a, b)
        self._h = h


class Triangle(Rectangle):
    _param_len = 3
    def __init__(self, a, b, grad):
        super().__init__(a, b)
        self.grad = grad

    @property
    def get_h(self):
        return self._h / 2


class Circle(Flat):
    _param_len = 1
    def __init__(self, r):
        self.r = r

    @property
    def area(self):
        return round(pi * self.r ** 2, 2)
