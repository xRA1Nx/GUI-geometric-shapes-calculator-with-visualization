#!/usr/bin/env python
from flat_classes import *
from volume_classes import *

flat_figurs = {"круг": Circle,
               "квадрат": Square,
               "прямоугольник": Rectangle,
               "треугольник": Triangle,
               "трапеция": Trapese,
               "ромб": Rhomb,
               }

volume_figurs = {"сфера": Orb,
                 "куб": Cube,
                 "параллелепипед": Parallelepiped,
                 "пирамида": Pyramid,
                 "цилиндр": Cylinder,
                 "конус": Conus,
                 }

figurs_types = {"плоские фигуры": "flat",
                "обьемные фигуры": 'volume',
                }


class ChoiseFigure:
    object = None
    type = "плоские фигуры"
    name = "квадрат"
    args = [2]

    @staticmethod
    def get_type(t=type):
        return figurs_types[t]

    @classmethod
    def get_area(cls):
        if cls.get_type() == "flat":
            cls.object = flat_figurs[cls.name](*cls.args)
        else:
            cls.object = volume_figurs[cls.name](*cls.args)
        return cls.object.area


print(ChoiseFigure.get_area())

print(ChoiseFigure.get_type())

# arg = [5]
# y = Circle(*arg)
# print(y.area)
