import sys
from math import cos, pi, sin
import numpy as np
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow, QInputDialog
from first_widget import First
from graph5 import Graph
from error import Error
import datetime as dt
from history import History

scx = 650
scy = 650


class FirstWidget(QMainWindow, First):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.start)
        self.username = self.lineEdit.text()
        self.pushButton_4.clicked.connect(self.history)

    def start(self):
        self.second_form = DrawGraph()
        self.second_form.show()
        self.hide()

    def history(self):
        self.open = History()
        self.open.show()



class DrawGraph(QWidget, Graph):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_1 = QPushButton(self)
        self.button_1.move(20, 40)
        self.button_1.setText("-")
        self.button_1.clicked.connect(self.masmin) # уменьшнние масшатаба

        self.button_2 = QPushButton(self)
        self.button_2.move(100, 40)
        self.button_2.setText("+")
        self.button_2.clicked.connect(self.masplus) # увеличесние масштаба

        self.pushButton.clicked.connect(self.add_function)
        self.buttonBox_1.accepted.connect(self.create_function)
        self.buttonBox_2.accepted.connect(self.create_function)
        self.buttonBox_3.accepted.connect(self.create_function)
        self.buttonBox_4.accepted.connect(self.create_function)
        self.buttonBox_5.accepted.connect(self.create_function)

        self.buttonBox_1.rejected.connect(self.delete)
        self.buttonBox_2.rejected.connect(self.delete)
        self.buttonBox_3.rejected.connect(self.delete)
        self.buttonBox_4.rejected.connect(self.delete)
        self.buttonBox_5.rejected.connect(self.delete)

        self.pushButton_2.clicked.connect(self.show_parameter)
        self.pushButton_3.clicked.connect(self.show_parameter)
        self.pushButton_4.clicked.connect(self.show_parameter)
        self.pushButton_5.clicked.connect(self.show_parameter)
        self.pushButton_6.clicked.connect(self.show_parameter)

        self.label_21.hide()

        self.mas = 1
        self.func = 'x ** 2'
        self.check = [0, 1, -1]

        self.COUNT = {1: [self.horizontalSlider, self.label_2, self.lineEdit_4,
                          self.label_3, self.lineEdit_2, self.label_4, self.lineEdit_3],
                      2: [self.label_8, self.lineEdit_8, self.buttonBox_2, self.pushButton_3,
                          self.horizontalSlider_2, self.label_5, self.lineEdit_7,
                          self.label_6, self.lineEdit_6, self.label_7, self.lineEdit_5],
                      3: [self.label_12, self.lineEdit_12, self.buttonBox_3, self.pushButton_4,  # here
                          self.horizontalSlider_3, self.label_9, self.lineEdit_11,
                          self.label_10, self.lineEdit_10, self.label_11, self.lineEdit_9],
                      4: [self.label_16, self.lineEdit_16, self.buttonBox_4, self.pushButton_5,
                          self.horizontalSlider_4, self.label_13, self.lineEdit_15,
                          self.label_14, self.lineEdit_14, self.label_15, self.lineEdit_13],
                      5: [self.label_20, self.lineEdit_20, self.buttonBox_5, self.pushButton_6,
                          self.horizontalSlider_5, self.label_17, self.lineEdit_19,
                          self.label_18, self.lineEdit_18, self.label_19, self.lineEdit_17]}

        self.BUTTON_BOXES = {self.buttonBox_1: self.lineEdit,
                             self.buttonBox_2: self.lineEdit_8,
                             self.buttonBox_3: self.lineEdit_12,
                             self.buttonBox_4: self.lineEdit_16,
                             self.buttonBox_5: self.lineEdit_20}

        self.SLIDERS = {self.pushButton_2: [self.horizontalSlider, self.label_2, self.lineEdit_4, self.label_3,
                                            self.lineEdit_2, self.label_4, self.lineEdit_3],
                        self.pushButton_3: [self.horizontalSlider_2, self.label_5, self.lineEdit_7, self.label_6,
                                            self.lineEdit_6, self.label_7, self.lineEdit_5],
                        self.pushButton_4: [self.horizontalSlider_3, self.label_9, self.lineEdit_11, self.label_10,
                                            self.lineEdit_10, self.label_11, self.lineEdit_9],
                        self.pushButton_5: [self.horizontalSlider_4, self.label_13, self.lineEdit_15, self.label_14,
                                            self.lineEdit_14, self.label_15, self.lineEdit_13],
                        self.pushButton_6: [self.horizontalSlider_5, self.label_17, self.lineEdit_19, self.label_18,
                                            self.lineEdit_18, self.label_19, self.lineEdit_17]}

        for i in range(1, len(self.COUNT) + 1):
            new = [j.hide() for j in self.COUNT[i]]

        self.step = 2

    def add_function(self):
        if self.step > 5:
            self.error = Error()
            self.error.show()

        else:
            for i in self.COUNT[self.step][:4]:
                i.show()
            self.step += 1

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

        self.dotsx = np.zeros(scx, dtype=float)
        self.dotsy = np.zeros(scy, dtype=float)
        self.pos = 0

        # проверка, существует ли вводимая функция
        check = [0, -1, 1]
        right = False
        for x in check:
            try:
                new = eval(self.func)
                right = True
            except:
                pass

        if right:

            for x in np.linspace(-5 * self.mas, 5 * self.mas, scx):  # задаём точки для графика
                self.dotsy[self.pos] = eval(self.func)
                self.dotsx[self.pos] = x
                self.pos += 1

            self.dotsx *= (scx / 10) / self.mas
            self.dotsy *= (scy / 10) / self.mas

            for i in range(len(self.dotsx)):  # рисуем график
                qp.drawPoint(self.dotsx[i] + scx // 2, scy // 2 - self.dotsy[i])


            # подключаемся к базе данных
            new = 'history_db.sqlite'
            con = sqlite3.connect(new)
            cur = con.cursor()
            time = str(dt.datetime.now())[:-7]
            print(time)
            save = f'''INSERT INTO history(name,time) VALUES('{self.func}','{time}');'''
            print(save)
            cur.execute(save)
            con.commit()

        else:
            self.label_21.show()
        # ещё раз намечаем оси, так как при прорисовке сетки они стали серыми
        pen = QPen(Qt.black, 2)
        qp.setPen(pen)
        qp.drawLine(0, scy // 2, scx, scy // 2)
        qp.drawLine(scx // 2, 0, scx // 2, scy)

    def create_function(self):
        '''for i in self.SLIDERS:
            if i.'''
        self.func = self.BUTTON_BOXES[self.sender()].text()
        print(self.func)
        # self.graph()
        self.repaint()

    def delete(self):
        self.label_21.hide()
        self.BUTTON_BOXES[self.sender()].setText('')

    def show_parameter(self):
        for i in self.SLIDERS[self.sender()]:
            i.show()
        # self.SLIDERS[self.sender()][0].setMinimum()


class Error(QWidget, Error):  # лимит на колическтво вводимых функций
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.close)

    def close(self):
        self.hide()

class History(QWidget, History):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.new = 'history_db.sqlite'
        self.con = sqlite3.connect(self.new)
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""SELECT * FROM history""").fetchall()
        all = []
        for i in self.result:
            data = '\t'.join(list(map(str, i)))
            all.append(data)

        all = '\n'.join(all)
        self.textEdit.setText(all)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWidget()
    ex.show()
    sys.exit(app.exec())
