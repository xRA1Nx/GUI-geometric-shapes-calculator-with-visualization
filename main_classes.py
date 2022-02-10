from math import sin, pi, tan, radians

"""
_h параметр "высоты" , который используется формулах для расчета S тропеции, 
в остальных случаях используется dafault
значение, кроме некоторых фигур где используется как коэффициент, к примеру треугольник - 1/2
"""


class Flat:
    __type = "flat"
    grad = 90
    _h = 1
    a = 0
    b = 0

    @property
    def get_h(self):
        return self._h

    @property
    def get_type(self):
        return self.__type

    @property
    def area(self):
        return round(self.a * self.b * sin(self.grad * pi / 180) * self.get_h, 2)


class Volume(Flat):
    __type = "volume"

    @property
    def main_area(self):
        return round(self.a * self.b * sin(self.grad * pi / 180) * self.get_h, 2)
