# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Error(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(251, 129)
        Form.setStyleSheet("background-color: rgb(47, 27, 0);")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 231, 31))
        self.label.setStyleSheet("background-color: rgb(248, 202, 255);")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(70, 80, 101, 31))
        self.pushButton.setStyleSheet("background-color: rgb(246, 210, 255);")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Ooops, too much functions"))
        self.pushButton.setText(_translate("Form", "OK"))
