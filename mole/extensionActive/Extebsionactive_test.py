# _*_ coding: utf-8 _*_

import sys, os

import sys
from PyQt4 import QtCore, QtGui

from ui_extensions_active import Ui_Dialog


class MyForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    print app.exec_()
    sys.exit()
