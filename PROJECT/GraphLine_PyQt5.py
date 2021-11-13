import sys
from math import cos, pi, sin, sqrt
import numpy as np
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow, QInputDialog, QLabel
from first_widget import First
from graph import Graph
from error import Error
import datetime as dt
from history import History
from colors import Colors
from history2 import History2
from help import Help

scx = 650
scy = 650


class FirstWidget(QMainWindow, First):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.start)

        self.pushButton_4.clicked.connect(self.history)

        self.pushButton_3.clicked.connect(self.help)

    def start(self):
        username = self.lineEdit.text()
        # print(USERNAME)
        self.second_form = DrawGraph(username)
        self.second_form.show()
        self.hide()

    def history(self):
        self.open = History()
        self.open.show()

    def help(self):
        self.open2 = Help()
        self.open2.show()


class DrawGraph(QWidget, Graph):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setupUi(self)
        self.button_1 = QPushButton(self)
        self.button_1.move(20, 40)
        self.button_1.setText("-")
        self.button_1.clicked.connect(self.masmin)  # уменьшнние масшатаба

        self.button_2 = QPushButton(self)
        self.button_2.move(100, 40)
        self.button_2.setText("+")
        self.button_2.clicked.connect(self.masplus)  # увеличесние масштаба

        self.pushButton_7.clicked.connect(self.save)

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

        self.pushButton_10.clicked.connect(self.show_saved)

        self.func_list = []
        self.colors = [Qt.red, Qt.green, Qt.yellow, Qt.cyan, Qt.darkMagenta]
        self.parametres = ['None', 'None', 'None', 'None', 'None']

        self.label_21.hide()
        self.label_22.hide()
        self.label_23.hide()

        self.mas = 1
        # self.func = 'x ** 2'
        self.check = [0, 1, -1]

        self.horizontalSlider.valueChanged.connect(self.par_change)
        self.horizontalSlider_2.valueChanged.connect(self.par_change)
        self.horizontalSlider_3.valueChanged.connect(self.par_change)
        self.horizontalSlider_4.valueChanged.connect(self.par_change)
        self.horizontalSlider_5.valueChanged.connect(self.par_change)

        self.sliders = [self.horizontalSlider, self.horizontalSlider_2, self.horizontalSlider_3,
                        self.horizontalSlider_4, self.horizontalSlider_5]

        self.coords = QLabel(self)
        self.coords.setText("Координаты: None, None")
        self.coords.move(650, 650)
        self.coords.resize(500, 40)

        for i in self.sliders:
            i.setMinimum(0)
            i.setMaximum(10)
            i.setSingleStep(1)

        self.box_buttons = [self.buttonBox_1, self.buttonBox_2, self.buttonBox_3,
                            self.buttonBox_4, self.buttonBox_5]

        self.labels = [self.label, self.label_8, self.label_12, self.label_16, self.label_20]

        self.line_edits = [self.lineEdit, self.lineEdit_8, self.lineEdit_12, self.lineEdit_16, self.lineEdit_20]

        self.add_functions_buttons = [self.pushButton_2, self.pushButton_3, self.pushButton_4,
                                      self.pushButton_5, self.pushButton_6]

        self.par_widgets = [
            [self.label_2, self.lineEdit_4, self.label_3, self.lineEdit_2, self.label_4, self.lineEdit_3],
            [self.label_5, self.lineEdit_7, self.label_6, self.lineEdit_6, self.label_7, self.lineEdit_5],
            [self.label_9, self.lineEdit_11, self.label_10, self.lineEdit_10, self.label_11, self.lineEdit_9],
            [self.label_13, self.lineEdit_15, self.label_14, self.lineEdit_14, self.label_15, self.lineEdit_13],
            [self.label_17, self.lineEdit_19, self.label_18, self.lineEdit_18, self.label_19, self.lineEdit_17]]

        for i in range(5):
            hide_w = [j.hide() for j in self.par_widgets[i]]
            self.sliders[i].hide()

        self.step = 1

        for i in range(1, 5):
            self.box_buttons[self.step].hide()
            self.labels[self.step].hide()
            self.line_edits[self.step].hide()
            self.step += 1

        self.step = 1

    def mouseMoveEvent(self, event):
        distance_from_center = round(((event.y() - 250) ** 2 + (event.x() - 500) ** 2) ** 0.5, 2)
        x = round((round(event.x(), 2) - 325) * self.mas / 65, 2)
        y = round(-(round(event.y(), 2) - 325) * self.mas / 65, 2)
        self.coords.setText(f'Coordinates: ({x}, {y})')

        '''q = QPainter()  #Painting the line
        q.begin(self)
        q.drawLine(event.x(), event.y(), 250, 500)
        q.end()'''

    def add_function(self):
        if self.step > 4:
            self.error = Error()
            self.error.show()

        else:
            self.box_buttons[self.step].show()
            self.labels[self.step].show()
            self.line_edits[self.step].show()
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

        for func in self.func_list:
            '''if self.par_a != "None":
                a = self.par_a'''

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

            a = self.parametres[0]
            b = self.parametres[1]
            c = self.parametres[2]
            d = self.parametres[3]
            e = self.parametres[4]

            # проверка, существует ли вводимая функция
            check = [0, -1, 1]
            right = False
            for x in check:
                try:
                    new = eval(func)
                    right = True
                except:
                    pass

            if right:

                for x in np.linspace(-5 * self.mas, 5 * self.mas, scx):  # задаём точки для графика
                    try:
                        self.dotsy[self.pos] = eval(func)
                        self.dotsx[self.pos] = x
                        self.pos += 1
                    except:
                        pass

                self.dotsx *= (scx / 10) / self.mas
                self.dotsy *= (scy / 10) / self.mas

                '''pen = QPen(self.colors[self.func.index(func)], 1)
                qp.setPen(pen)'''

                for i in range(len(self.dotsx)):  # рисуем график
                    try:
                        pen = QPen(self.colors[self.func_list.index(func)], 1.5)
                        qp.setPen(pen)

                        qp.drawPoint(self.dotsx[i] + scx // 2, scy // 2 - self.dotsy[i])
                    except:
                        pass

                # подключаемся к базе данных

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

        ind = self.box_buttons.index(self.sender())
        self.func = self.line_edits[ind].text()
        self.func_list.append(self.func)
        new = 'history_db.sqlite'
        con = sqlite3.connect(new)
        cur = con.cursor()
        time = str(dt.datetime.now())[:-7]

        save = f'''INSERT INTO history(name,time,username) VALUES('{self.func}','{time}','{self.username}');'''

        cur.execute(save)
        con.commit()

        print(self.func)
        # self.graph()
        self.repaint()

    def delete(self):
        self.label_21.hide()
        ind = self.box_buttons.index(self.sender())

        try:
            print(self.func_list)
            del self.func_list[self.func_list.index(self.line_edits[ind].text())]
        except:
            pass

        self.line_edits[ind].setText('')
        # self.BUTTON_BOXES[self.sender()].setText('')
        self.repaint()

    def show_parameter(self):
        ind = self.add_functions_buttons.index(self.sender())
        for i in self.par_widgets[ind]:
            i.show()
        self.sliders[ind].show()
        # self.SLIDERS[self.sender()][0].setMinimum()

    def par_change(self):
        for i in self.sliders:
            ind = self.sliders.index(i)
            mn = self.par_widgets[ind][1].text()
            print(mn)
            mx = self.par_widgets[ind][3].text()
            print(mx)
            st = self.par_widgets[ind][5].text()
            if mn != '' and mx != '' and int(mn) > int(mx):
                self.label_22.show()
            elif mn != '' and mx != '' and st != '':
                self.label_22.hide()
                self.label_23.hide()
                i.setMinimum(int(mn))
                i.setMaximum(int(mx))
                i.setSingleStep(int(st))
            else:
                self.label_23.show()

        self.parametres[self.sliders.index(self.sender())] = self.sender().value()
        self.repaint()

    def save(self):
        name, ok_pressed = QInputDialog.getText(self, "Function", 'Function:')

        if ok_pressed:
            new = 'history_db.sqlite'
            con = sqlite3.connect(new)
            cur = con.cursor()
            time2 = str(dt.datetime.now())[:-7]

            save = f'''INSERT INTO saved(function, username, time) VALUES('{name}','{self.username}','{time2}');'''

            cur.execute(save)
            con.commit()

    def show_saved(self):
        self.open = History2()
        self.open.show()


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


class History2(QWidget, History2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.new = 'history_db.sqlite'
        self.con = sqlite3.connect(self.new)
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""SELECT * FROM saved""").fetchall()
        all = []
        for i in self.result:
            data = '\t'.join(list(map(str, i)))
            all.append(data)

        all = '\n'.join(all)
        self.textEdit.setText(all)


class Colors(QWidget, Colors):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Help(QWidget, Help):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.help = open('help.txt', 'r', encoding='utf-8')
        self.text = self.help.readlines()
        self.textEdit.setText('\n'.join(self.text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWidget()
    ex.show()
    sys.exit(app.exec())
