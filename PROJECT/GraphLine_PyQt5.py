import sys
from math import cos, pi, sin
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton

scx = 1000
scy = 1000


class DrawStar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mas = 1

    def initUI(self):
        self.setGeometry(300, 300, scx, scy)
        self.setWindowTitle('Graph')

        self.button_1 = QPushButton(self)
        self.button_1.move(20, 40)
        self.button_1.setText("-")
        self.button_1.clicked.connect(self.masmin)

        self.button_2 = QPushButton(self)
        self.button_2.move(100, 40)
        self.button_2.setText("+")
        self.button_2.clicked.connect(self.masplus)

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

        for x in np.linspace(-5 * self.mas, 5 * self.mas, scx):  # задаём точки для графика
            dotsy[pos] = sin(x)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DrawStar()
    ex.show()
    sys.exit(app.exec())
