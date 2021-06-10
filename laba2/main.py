import sys
from PyQt5 import QtWidgets
from gui import Application, WelcomeWindow

def start():
    app = QtWidgets.QApplication(sys.argv)

    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    start()
