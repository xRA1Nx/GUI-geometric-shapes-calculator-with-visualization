#!/usr/bin/env python
from flat_classes import *
from volume_classes import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

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
# res = {**flat_figurs, **volume_figurs}
# print(res)
#
# for k, v in sorted(res.items(), key=lambda x: x[1]._param_len):
#     print(k, v._param_len)

figurs_types = {"плоские фигуры": "flat",
                "обьемные фигуры": 'volume',
                }


class ChoiseFigure:
    object = None
    fig_type = "1"
    figure = "квадрат"
    params = [2]

    @staticmethod
    def convert_type(t):
        return figurs_types[t]

    @classmethod
    def set_figure(cls, item):
        cls.figure = item

    @classmethod
    def set_type(cls, item):
        cls.fig_type = item

    @classmethod
    def set_params(cls, arg_list):
        cls.params = arg_list

    @classmethod
    def get_area(cls):
        if cls.convert_type(cls.fig_type) == "flat":
            cls.object = flat_figurs[cls.figure](*cls.params)
        elif cls.convert_type(cls.fig_type) == "volume":
            cls.object = volume_figurs[cls.figure](*cls.params)
        return cls.object.area


Form, Window = uic.loadUiType("template.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def radio_signal():
    figures = []
    form.combo_figurs.clear()
    form.combo_operations.clear()
    if form.radioButton_flat.isChecked():
        figures = flat_figurs.keys()
        form.combo_operations.addItem("S - площадь фигуры")
        ChoiseFigure.set_type("плоские фигуры")  # устанавливаем типа обьекта flat

    elif form.radioButton_volume.isChecked():
        figures = volume_figurs.keys()
        form.combo_operations.addItem("S - площадь фигуры")
        form.combo_operations.addItem("V - обьем фигуры")
        ChoiseFigure.set_type("обьемные фигуры")

    for item in figures:
        form.combo_figurs.addItem(item)


def button_signal():
    args = []

    ChoiseFigure.set_figure(form.combo_figurs.currentText())

    for item in POLE_TUPLE:
        if item.text():
            args.append(int(item.text()))
    ChoiseFigure.set_params(args)
    form.output.setText(str(ChoiseFigure.get_area()))


def combo_figures_signal():
    layout_cleared()
    if form.combo_figurs.currentText() in {"круг", "сфера", "квадрат", "куб"}:
        form.pole_a.setHidden(False)
        form.label_a.setHidden(False)
        if form.combo_figurs.currentText() in {"круг", "сфера"}:
            form.label_a.setText("радиус R, мм:")
        else:
            form.label_a.setText("сторона a, мм:")
    elif form.combo_figurs.currentText() in {"прямоугольник", "ромб", "цилиндр", "конус"}:
        form.pole_a.setHidden(False)
        form.label_a.setHidden(False)
        form.pole_b.setHidden(False)
        form.label_b.setHidden(False)
        if form.combo_figurs.currentText() in {"цилиндр", "конус"}:
            form.label_a.setText("радиус R, мм:")
            form.label_b.setText("высота h, мм:")
        elif form.combo_figurs.currentText() in {"прямоугольник"}:
            form.label_a.setText("сторона a, мм:")
            form.label_b.setText("сторона b, мм:")
        elif form.combo_figurs.currentText() in {"ромб"}:
            form.label_a.setText("сторона a, мм:")
            form.label_b.setText("угол, º:")
    elif form.combo_figurs.currentText() in {"треугольник", "трапеция", "параллелепипед", "пирамида"}:
        form.pole_a.setHidden(False)
        form.label_a.setHidden(False)
        form.pole_b.setHidden(False)
        form.label_b.setHidden(False)
        form.pole_c.setHidden(False)
        form.label_c.setHidden(False)
        if form.combo_figurs.currentText() in {"параллелепипед", "трапеция"}:
            form.label_a.setText("сторона a, мм:")
            form.label_b.setText("сторона b, мм:")
            form.label_c.setText("высота h,  мм:")
        elif form.combo_figurs.currentText() == "треугольник":
            form.label_a.setText("сторона a, мм:")
            form.label_b.setText("сторона b, мм:")
            form.label_c.setText("угол, º:")
        elif form.combo_figurs.currentText() == "пирамида":
            form.label_a.setText("сторона a, мм:")
            form.label_b.setText("кол-во граней, шт:")
            form.label_c.setText("высота, º:")


form.radioButton_flat.toggled.connect(radio_signal)
form.radioButton_volume.toggled.connect(radio_signal)
form.pushButton.clicked.connect(button_signal)
form.combo_figurs.currentTextChanged.connect(combo_figures_signal)

POLE_TUPLE = (form.pole_a,
              form.pole_b,
              form.pole_c)
LABLE_TUPLE = (form.label_a,
               form.label_b,
               form.label_c)


def layout_cleared(pol=POLE_TUPLE, lab=LABLE_TUPLE):
    for i in (pol + lab):
        i.setHidden(True)


layout_cleared()

app.exec()

# arg = [5]
# y = Circle(*arg)
# print(y.area)
# print(ChoiseFigure.get_area())
#
# print(ChoiseFigure.get_type())
