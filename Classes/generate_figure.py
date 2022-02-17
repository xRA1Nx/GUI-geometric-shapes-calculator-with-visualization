from Classes.flat_classes import flat_figurs
from Classes.volume_classes import volume_figurs

figurs_types = {"плоские фигуры": "flat",
                "обьемные фигуры": 'volume',
                }


class GenerateFigure:
    object = None
    fig_type = ""
    figure = ""
    params = []
    operation = ""
    draw_type = ""


    @staticmethod
    def convert_type(t):
        return figurs_types[t]

    @classmethod
    def set_figure(cls, item):
        cls.figure = item

    @classmethod
    def get_figure(cls):
        return cls.figure

    @classmethod
    def set_type(cls, item):
        cls.fig_type = item

    @classmethod
    def set_draw_type(cls, item):
        cls.draw_type = item

    @classmethod
    def get_draw_type(cls):
        return cls.draw_type

    @classmethod
    def set_operation(cls, item):
        cls.operation = item

    @classmethod
    def set_params(cls, arg_list):
        cls.params = arg_list

    @classmethod
    def get_params(cls):
        return cls.params

    @classmethod
    def get_result(cls):
        if cls.convert_type(cls.fig_type) == "flat":
            cls.object = flat_figurs[cls.figure](*cls.params)
        elif cls.convert_type(cls.fig_type) == "volume":
            cls.object = volume_figurs[cls.figure](*cls.params)
        if cls.operation == "S - площадь фигуры":
            return cls.object.area
        elif cls.operation == "V - обьем фигуры":
            return cls.object.volume
