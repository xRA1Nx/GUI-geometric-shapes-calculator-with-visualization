from math import sin, pi, tan, radians, cos

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
    c = 0
    param_len = 0
    label_a = ""
    label_b = ""
    label_c = ""
    name = ""
    draw_type = 0
    draw_type_3d = 0
    points = []

    def __str__(self):
        labels = [self.label_a, self.label_b, self.label_c]
        text = f"{self.name.upper()}-"
        for i in range(len(self.get_params)):
            text += f" {labels[i]} {self.get_params[i]}"
        return text

    @property
    def get_params(self):
        return self.a, self.b, self.c

    @property
    def get_points(self):
        return None

    @property
    def get_h(self):
        return self._h

    @property
    def get_type(self):
        return self.__type

    @property
    def get_draw_type(self):
        return self.draw_type

    @property
    def area(self):
        return round(self.a * self.b * sin(self.grad * pi / 180) * self.get_h, 2)

    @property
    def get_param_len(self):
        return self.param_len


class Volume(Flat):
    __type = "volume"

    @property
    def main_area(self):
        return round(self.a * self.b * sin(self.grad * pi / 180) * self.get_h, 2)

    @property
    def get_draw_type(self):
        return self.draw_type_3d
