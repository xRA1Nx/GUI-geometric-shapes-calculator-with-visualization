#!/usr/bin/env python
from Classes.generate_figure import *
from math import cos, sin, radians
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QCoreApplication, QPoint
from PyQt5.QtGui import QPen, QPainter, QPolygon

Form, Window = uic.loadUiType("template.ui")

app = QApplication([])
window = Window()
window.setGeometry(100, 100, 600, 400)
window.setFixedSize(420, 250)

form = Form()
form.setupUi(window)
# window.setWindowFlags(Qt.FramelessWindowHint)  # убираем верхнее поле окна
window.setWindowFlags(Qt.SubWindow

                      )
window.show()

POLE_TUPLE = (form.pole_a,
              form.pole_b,
              form.pole_c)
LABLE_TUPLE = (form.label_a,
               form.label_b,
               form.label_c)


class AppConfig:

    @staticmethod
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

    @staticmethod
    def button_signal():
        args = []
        #draw.close()
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

        if selected_figure.param_len == len(args):
            form.output.setText(str(GenerateFigure.get_result()))
            draw.setGeometry(510, 130, 300, 200)
            draw.set_params()
            draw.set_figure()
            draw.show()

    @staticmethod
    def layout_cleared():
        for i in (POLE_TUPLE + LABLE_TUPLE):
            i.setHidden(True)
            i.setStyleSheet("color: black")
            i.setText("")

    @staticmethod
    def combo_figures_signal():
        AppConfig.layout_cleared()
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


class Draw(QWidget):
    a = 0
    b = 0
    c = 0
    figure = ""

    def __init__(self):
        super(Draw, self).__init__()
        self.pen = QPen()
        self.setWindowTitle("Визуализация")
        self.pen.setColor(Qt.green)
        self.pen.setWidth(3)

        # base_layer = QVBoxLayout(self)

    def set_params(self):
        params = GenerateFigure.get_params()
        if len(params) >= 1:
            self.a = params[0]
            if len(params) >= 2:
                self.b = params[1]
                if len(params) == 3:
                    self.c = params[2]

    def set_figure(self):
        self.figure = GenerateFigure.get_figure()

    def paintEvent(self, event):
        def_x = 130
        def_y = 70
        painter = QPainter(self)
        painter.setPen(self.pen)
        if self.figure == "прямоугольник":
            painter.drawRect(def_x, def_y, int(self.a * 10), int(self.b * 10))
        if self.figure == "квадрат":
            painter.drawRect(def_x, def_y, int(self.a * 10), int(self.a * 10))
        if self.figure == "круг":
            painter.drawEllipse(def_x, def_y, int(self.a * 10), int(self.a * 10))
        if self.figure == "треугольник":
            gr = self.c
            point_b_x = int(def_x + self.b * sin(radians(gr)) * 10)
            point_b_y = int(def_y + self.b * cos(radians(gr)) * 10)
            points = [QPoint(def_x, def_y),
                      QPoint(def_x, def_y + int(self.a * 10)),
                      QPoint(point_b_x, point_b_y)]
            poly = QPolygon(points)
            painter.drawPolygon(poly)
        if self.figure == "трапеция":
            def_x = 80
            def_y = 30
            points = [QPoint(def_x, def_y),
                      QPoint(def_x + int(self.a * 10), def_y),
                      QPoint(def_x + int(self.b * 10), def_y + int(self.c * 10)),
                      QPoint(def_x - 50, def_y + int(self.c * 10))]
            poly = QPolygon(points)
            painter.drawPolygon(poly)
        if self.figure == "ромб":
            def_x = 80
            def_y = 30
            gr = self.b
            point_a_x = int(def_x + self.a * sin(radians(90 - gr)) * 10)
            point_a_y = int(def_y + self.a * cos(radians(90 - gr)) * 10)
            points = [QPoint(def_x, def_y),
                      QPoint(def_x + int(self.a * 10), def_y),
                      QPoint(point_a_x + int(self.a * 10), point_a_y),
                      QPoint(point_a_x, point_a_y),
                      # QPoint(def_x + int(self.b * 10), def_y + int(self.c * 10)),
                      # QPoint(def_x - 50, def_y + int(self.c * 10))
                      ]
            poly = QPolygon(points)
            painter.drawPolygon(poly)


# form.gridLayout_2.addWidget(Painter)


if __name__ == "__main__":
    AppConfig.layout_cleared()
    draw = Draw()
    form.radioButton_flat.toggled.connect(AppConfig.radio_signal)
    form.radioButton_volume.toggled.connect(AppConfig.radio_signal)
    form.Button_exit.clicked.connect(QCoreApplication.instance().quit)  # закрываем приложение
    form.pushButton.clicked.connect(AppConfig.button_signal)
    form.combo_figurs.currentTextChanged.connect(AppConfig.combo_figures_signal)

    app.exec()
