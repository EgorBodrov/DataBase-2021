# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Python\database\welcome.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WelcomeWindow(object):
    def setupUi(self, WelcomeWindow):
        WelcomeWindow.setObjectName("WelcomeWindow")
        WelcomeWindow.resize(840, 250)
        WelcomeWindow.setMinimumSize(QtCore.QSize(840, 250))
        WelcomeWindow.setMaximumSize(QtCore.QSize(840, 250))
        self.centralwidget = QtWidgets.QWidget(WelcomeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.push_connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.push_connect_button.setGeometry(QtCore.QRect(350, 170, 131, 41))
        self.push_connect_button.setObjectName("push_connect_button")
        self.enter_database_line = QtWidgets.QLineEdit(self.centralwidget)
        self.enter_database_line.setGeometry(QtCore.QRect(210, 130, 411, 31))
        self.enter_database_line.setStyleSheet("font: 75 12pt \"Arial\";")
        self.enter_database_line.setText("")
        self.enter_database_line.setAlignment(QtCore.Qt.AlignCenter)
        self.enter_database_line.setObjectName("enter_database_line")
        self.enter_database_label = QtWidgets.QLabel(self.centralwidget)
        self.enter_database_label.setGeometry(QtCore.QRect(280, 80, 271, 41))
        self.enter_database_label.setStyleSheet("font: 87 14pt \"Arial Black\";")
        self.enter_database_label.setAlignment(QtCore.Qt.AlignCenter)
        self.enter_database_label.setObjectName("enter_database_label")
        WelcomeWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(WelcomeWindow)
        QtCore.QMetaObject.connectSlotsByName(WelcomeWindow)

    def retranslateUi(self, WelcomeWindow):
        _translate = QtCore.QCoreApplication.translate
        WelcomeWindow.setWindowTitle(_translate("WelcomeWindow", "Connection"))
        self.push_connect_button.setText(_translate("WelcomeWindow", "CONNECT"))
        self.enter_database_label.setText(_translate("WelcomeWindow", "ENTER DATABASE NAME"))
