import sys
from math import cos, pi, sin
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow, QInputDialog
from first_widget import First
from graphs import Graphs
from error import Error

scx = 500
scy = 500

class FirstWidget(QMainWindow, First):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.start)


    def start(self):
        self.second_form = DrawStar()
        self.second_form.show()
        self.hide()


class DrawStar(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.mas = 1



    def initUI(self):
        self.setGeometry(100, 100, scx, scy)
        self.setWindowTitle('Graph')

        self.button_1 = QPushButton(self)
        self.button_1.move(20, 40)
        self.button_1.setText("-")
        self.button_1.clicked.connect(self.masmin)

        self.button_2 = QPushButton(self)
        self.button_2.move(100, 40)
        self.button_2.setText("+")
        self.button_2.clicked.connect(self.masplus)

        self.button_back = QPushButton(self)
        self.button_back.move(scx - 100, scy - 100)
        self.button_back.setText("SETTINGS")
        self.button_back.clicked.connect(self.settings)

    def settings(self):
        self.graphs = GraphsSettings()
        self.graphs.show()




    def masmin(self):
        self.mas *= 1.2
        self.repaint()

    def masplus(self):
        self.mas /= 1.2
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.graph(qp)
        qp.end()

    def graph(self, qp):
        # рисуем оси

        pen = QPen(Qt.black, 2)
        qp.setPen(pen)

        qp.drawLine(0, scy // 2, scx, scy // 2)
        qp.drawLine(scx // 2, 0, scx // 2, scy)

        for i in np.linspace(-5 * self.mas, 5 * self.mas, 11):  # делаем единичные отрезки на Ox + сетку
            qp.drawText(scx // 2 + (i * (scx / 10)) / self.mas, scy // 2, str(round(i, 2)))
            pen = QPen(Qt.gray, 1)
            qp.setPen(pen)
            qp.drawLine(scx // 2 + (i * (scx / 10)) / self.mas, 0, scx // 2 + (i * (scx / 10)) / self.mas, scy)

        for i in np.linspace(-5 * self.mas, 5 * self.mas, 11):  # делаем единичные отрезки на Oy + сетку
            qp.drawText(scx // 2, scy // 2 + (i * (scy / 10)) / self.mas, str(round(-i, 2)))
            pen = QPen(Qt.gray, 1)
            qp.setPen(pen)
            qp.drawLine(0, scy // 2 + (i * (scy / 10)) / self.mas, scx, scy // 2 + (i * (scy / 10)) / self.mas)

        # Изменяем цвет линии для графика
        pen = QPen(Qt.red, 2)
        qp.setPen(pen)

        dotsx = np.zeros(scx, dtype=float)
        dotsy = np.zeros(scy, dtype=float)
        pos = 0
        func = 'sin(x)'

        for x in np.linspace(-5 * self.mas, 5 * self.mas, scx):  # задаём точки для графика
            dotsy[pos] = eval(func)
            dotsx[pos] = x
            pos += 1

        dotsx *= (scx / 10) / self.mas
        dotsy *= (scy / 10) / self.mas

        for i in range(len(dotsx)):  # рисуем график
            qp.drawPoint(dotsx[i] + scx // 2, scy // 2 - dotsy[i])

        # ещё раз намечаем оси, так как при прорисовке сетки они стали серыми
        pen = QPen(Qt.black, 2)
        qp.setPen(pen)
        qp.drawLine(0, scy // 2, scx, scy // 2)
        qp.drawLine(scx // 2, 0, scx // 2, scy)


class GraphsSettings(QWidget, Graphs):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.lineEdit_2.hide()
        self.lineEdit_3.hide()
        self.lineEdit_4.hide()
        self.lineEdit_5.hide()
        self.COUNT = {2: self.lineEdit_2, 3: self.lineEdit_3, 4: self.lineEdit_4, 5: self.lineEdit_5}
        self.step = 2

        self.pushButton.clicked.connect(self.add_function)

    def add_function(self):
        if self.step > 5:
            self.error = Error()
            self.error.show()

        else:
            self.COUNT[self.step].show()
            self.step += 1

class Error(QWidget, Error):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.close)

    def close(self):
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWidget()
    ex.show()
    sys.exit(app.exec())
