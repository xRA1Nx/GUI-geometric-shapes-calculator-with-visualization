#!/usr/bin/env python

from Classes.flat_classes import flat_figurs
from Classes.volume_classes import volume_figurs
from itertools import product, combinations

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainter, QPolygon

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np


# конфигуратор основного окна с шаблоном интерфейса
class AppConfig:
    args = []
    obj = None

    @classmethod
    def set_obj(cls, item):
        cls.obj = item

    @classmethod
    def get_result(cls):
        if form.combo_operations.currentText() == "S - площадь фигуры":
            return cls.obj.area
        elif form.combo_operations.currentText() == "V - обьем фигуры":
            return cls.obj.volume

    @classmethod
    def get_obj(cls):
        return cls.obj

    @staticmethod
    def radio_signal():

        figures = []
        form.combo_figurs.clear()
        form.combo_operations.clear()
        if form.radioButton_flat.isChecked():
            figures = flat_figurs.keys()
            form.combo_operations.addItem("S - площадь фигуры")

        elif form.radioButton_volume.isChecked():
            figures = volume_figurs.keys()
            form.combo_operations.addItem("S - площадь фигуры")
            form.combo_operations.addItem("V - обьем фигуры")

        for item in figures:
            form.combo_figurs.addItem(item)

    @staticmethod
    def button_signal():
        draw.close()
        draw_3d.close()
        d_x = window.width() + window.x() + 2
        d_y = window.y() + 30
        if form.combo_operations.currentText():
            args = []
            all_figurs = {**flat_figurs, **volume_figurs}
            for item in POLE_TUPLE:
                item.setStyleSheet("color: black")
                if item.text() and item.text().replace(".", "", 1).isdigit():  # валидация данных по типу float !!!
                    args.append(float(item.text()))
                elif item.text():
                    item.setStyleSheet("color: red")
                if not item.text():
                    item.setStyleSheet("border: 1px solid red")

            selected_figure = all_figurs[form.combo_figurs.currentText()](*args)
            AppConfig.set_obj(selected_figure)
            if selected_figure.param_len == len(args):  # валидация по заполннености полей
                form.output.setText(str(AppConfig.get_result()))
                if form.radioButton_flat.isChecked():
                    # делаем окно визуализации вспомогательным, теперь оно будет закрываться при закрытии главного окна!
                    draw.set_params()
                    draw.setGeometry(d_x, d_y, 500, 500)
                    if max(args) <= 360:
                        draw.show()
                elif form.radioButton_volume.isChecked():
                    draw_3d.set_params()
                    draw_3d.setGeometry(d_x, d_y, 500, 500)
                    draw_3d.set_draw_type()
                    draw_3d.start_draw()
                    draw_3d.show()

    @staticmethod
    def layout_cleared():
        for i in (POLE_TUPLE + LABLE_TUPLE):
            i.setHidden(True)
            i.setStyleSheet("color: black")
            i.clear()

    @staticmethod
    def combo_figures_signal():
        AppConfig.layout_cleared()
        form.output.setText("")
        if form.combo_figurs.currentText():
            all_figurs = {**flat_figurs, **volume_figurs}
            selected_figure = all_figurs[form.combo_figurs.currentText()]
            form.pole_a.setHidden(False)
            form.label_a.setHidden(False)
            form.label_a.setText(selected_figure.label_a)
            if selected_figure.label_b:
                form.pole_b.setHidden(False)
                form.label_b.setHidden(False)
                form.label_b.setText(selected_figure.label_b)
            if selected_figure.label_c:
                form.pole_c.setHidden(False)
                form.label_c.setHidden(False)
                form.label_c.setText(selected_figure.label_c)


# доп окно для рисования 2D моделей
class Draw(QDialog):
    a = 0
    b = 0
    c = 0
    figure = ""
    draw_type = 0

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.pen = QPen()
        self.setWindowTitle("Визуализация")
        self.pen.setColor(Qt.green)
        self.pen.setWidth(3)

    @property
    def get_a(self):
        return self.a

    @property
    def get_b(self):
        return self.b

    @property
    def get_c(self):
        return self.c

    def set_params(self):
        params = AppConfig.get_obj().get_params
        if len(params) >= 1:
            self.a = params[0]
            self.b = self.a
            if len(params) >= 2:
                self.b = params[1]
                if len(params) == 3:
                    self.c = params[2]

    def paintEvent(self, event):
        def_x = 130
        def_y = 70
        painter = QPainter(self)
        painter.setPen(self.pen)
        obj = AppConfig.get_obj()
        if obj.draw_type == 1:
            painter.drawRect(def_x, def_y, int(self.a * 10), int(self.b * 10))
        elif obj.draw_type == 2:
            points = obj.get_points
            poly = QPolygon(points)
            painter.drawPolygon(poly)
        elif obj.draw_type == 3:
            painter.drawEllipse(def_x, def_y, int(self.a * 10), int(self.a * 10))


# доп окно для рисования 3D моделей
class Draw3D(Draw):
    def __init__(self, parent=None):
        super().__init__()
        QtWidgets.QWidget.__init__(self, parent)

    def start_draw(self):
        Create3dFig(self, width=5, height=4).plot()

    def set_draw_type(self):
        self.draw_type = AppConfig.get_obj().get_draw_type


# генератор 3D модели
class Create3dFig(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='3d')
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        obj = AppConfig.get_obj()
        if obj.get_draw_type == 1:
            temp_x, temp_y, temp_z = obj.get_points
            x = temp_x * draw_3d.get_a
            y = temp_y * draw_3d.get_a
            if draw_3d.get_b:
                z = temp_z * draw_3d.get_b
            else:
                z = temp_z * draw_3d.get_a
            self.ax.plot_surface(x, y, z, cmap=plt.get_cmap('rainbow'))

        elif obj.get_draw_type == 2:
            points, verts = obj.get_points
            self.ax.scatter3D(points[:, 0], points[:, 1], points[:, 2])
            self.ax.add_collection3d(Poly3DCollection(verts,
                                                      facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
        elif obj.get_draw_type == 3:
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
    window.setFixedSize(400, 175)
    window.show()

    POLE_TUPLE = (form.pole_a,
                  form.pole_b,
                  form.pole_c)
    LABLE_TUPLE = (form.label_a,
                   form.label_b,
                   form.label_c)

    AppConfig.layout_cleared()
    draw_3d = Draw3D(window)
    draw = Draw(window)  # наследуем от Мейн окна

    form.radioButton_flat.toggled.connect(AppConfig.radio_signal)
    form.radioButton_volume.toggled.connect(AppConfig.radio_signal)
    form.pushButton.clicked.connect(AppConfig.button_signal)
    form.combo_figurs.currentTextChanged.connect(AppConfig.combo_figures_signal)

    app.exec()
