#!/usr/bin/env python

from Classes.generate_figure import *

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

# from PyQt5.QtGui import QPainter, QBrush, QPen
# from PyQt5.QtCore import Qt

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
        GenerateFigure.set_type("плоские фигуры")  # устанавливаем типа обьекта flat

    elif form.radioButton_volume.isChecked():
        figures = volume_figurs.keys()
        form.combo_operations.addItem("S - площадь фигуры")
        form.combo_operations.addItem("V - обьем фигуры")
        GenerateFigure.set_type("обьемные фигуры")

    for item in figures:
        form.combo_figurs.addItem(item)


def button_signal():
    args = []
    all_figurs = {**flat_figurs, **volume_figurs}
    selected_figure = all_figurs[form.combo_figurs.currentText()]

    GenerateFigure.set_figure(form.combo_figurs.currentText())
    GenerateFigure.set_operation(form.combo_operations.currentText())

    for item in POLE_TUPLE:
        item.setStyleSheet("color: black")
        if item.text() and item.text().replace(".", "", 1).isdigit():  # проверка на float
            args.append(float(item.text()))
        else:
            item.setStyleSheet("color: red")
        GenerateFigure.set_params(args)

    if selected_figure._param_len == len(args):
        form.output.setText(str(GenerateFigure.get_result()))


def combo_figures_signal():
    layout_cleared()
    form.output.setText("")
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
            form.label_c.setText("высота, мм:")


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
        i.setStyleSheet("color: black")
        i.setText("")


# painter = QPainter([])
# painter.setPen(QPen(Qt.green, 8, Qt.SolidLine))
# painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
# painter.drawEllipse(40, 40, 400, 400)

layout_cleared()

app.exec()
