#!/usr/bin/env python
from Classes.generate_figure import *
from math import cos, sin, radians

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen, QPainter, QPolygon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from itertools import product, combinations
import numpy as np


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
        draw.close()
        draw_3d.close()
        if form.combo_operations.currentText():
            args = []

            all_figurs = {**flat_figurs, **volume_figurs}
            selected_figure = all_figurs[form.combo_figurs.currentText()]

            GenerateFigure.set_figure(form.combo_figurs.currentText())
            GenerateFigure.set_operation(form.combo_operations.currentText())

            for item in POLE_TUPLE:
                item.setStyleSheet("color: black")
                if item.text() and item.text().replace(".", "", 1).isdigit():  # проверка на float
                    args.append(float(item.text()))
                elif item.text():
                    item.setStyleSheet("color: red")
                GenerateFigure.set_params(args)

            if selected_figure.param_len == len(args):
                form.output.setText(str(GenerateFigure.get_result()))
                d_x = window.width() + window.x() + 2
                d_y = window.y() + 30
                if form.radioButton_flat.isChecked():
                    # делаем окно визуализации вспомогательным, теперь оно будет закрываться при закрытии главного окна!
                    draw.setGeometry(d_x, d_y, 500, 500)
                    draw.set_params()
                    draw.set_figure()
                    if max(args) <= 360:
                        draw.show()
                elif form.radioButton_volume.isChecked():
                    draw_3d.set_figure()
                    draw_3d.set_params()
                    print(draw_3d.figure)
                    draw_3d.setGeometry(d_x, d_y, 500, 500)
                    draw_3d.start_draw()
                    draw_3d.show()

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


class Draw(QDialog):
    a = 0
    b = 0
    c = 0
    figure = ""

    @property
    def get_a(self):
        return self.a

    @property
    def get_b(self):
        return self.b

    @property
    def get_c(self):
        return self.c

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.pen = QPen()
        self.setWindowTitle("Визуализация")
        self.pen.setColor(Qt.green)
        self.pen.setWidth(3)
        # self.setWindowFlags(Qt.Window)

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


class Draw3D(Draw):
    def __init__(self, parent=None):
        super().__init__()
        QtWidgets.QWidget.__init__(self, parent)

    def start_draw(self):
        Create3dFig(self, width=5, height=4).plot()


class Create3dFig(FigureCanvas):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='3d')
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        if draw_3d.figure == "сфера":
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = draw_3d.get_a * np.outer(np.cos(u), np.sin(v))
            y = draw_3d.get_a * np.outer(np.sin(u), np.sin(v))
            z = draw_3d.get_a * np.outer(np.ones(np.size(u)), np.cos(v))
            self.ax.plot_surface(x, y, z, rstride=5, cstride=5, color='b')
        if draw_3d.figure == "цилиндр":
            u = np.linspace(0, 2 * np.pi, 50)  # разделить круг на 50 углов
            h = draw_3d.get_b * np.linspace(0, 1, 20)  # Разделить высоту 1 на 20 равных частей
            x = draw_3d.get_a * np.outer(np.sin(u), np.ones(len(h)))  # значение x повторяется 20 раз
            y = draw_3d.get_a * np.outer(np.cos(u), np.ones(len(h)))  # значение y повторяется 20 раз
            z = np.outer(np.ones(len(u)), h)  # высота, соответствующая x, y
            self.ax.plot_surface(x, y, z, cmap=plt.get_cmap('rainbow'))
        if draw_3d.figure == "куб":
            r = [-1 * draw_3d.get_a, draw_3d.get_a]
            for s, e in combinations(np.array(list(product(r, r, r))), 2):
                if np.sum(np.abs(s - e)) == r[1] - r[0]:
                    self.ax.plot3D(*zip(s, e), color="b")


if __name__ == "__main__":
    Form, Window = uic.loadUiType("template.ui")
    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    window.setGeometry(100, 100, 600, 400)
    # window.setWindowFlags(Qt.CoverWindow)
    # window.showMaximized()
    window.setFixedSize(400, 175)
    window.show()

    POLE_TUPLE = (form.pole_a,
                  form.pole_b,
                  form.pole_c)
    LABLE_TUPLE = (form.label_a,
                   form.label_b,
                   form.label_c)

    AppConfig.layout_cleared()
    draw = Draw(window)  # наследуем от Мейн окна
    draw_3d = Draw3D(window)
    form.radioButton_flat.toggled.connect(AppConfig.radio_signal)
    form.radioButton_volume.toggled.connect(AppConfig.radio_signal)
    form.pushButton.clicked.connect(AppConfig.button_signal)
    form.combo_figurs.currentTextChanged.connect(AppConfig.combo_figures_signal)

    app.exec()

    # form.Button_exit.clicked.connect(QCoreApplication.instance().quit)  # закрываем приложение
