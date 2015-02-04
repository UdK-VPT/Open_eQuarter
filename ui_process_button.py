from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton
from PyQt4.QtCore import SIGNAL

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class QProcessButton(QPushButton):

    def __init(self, parent):
        QPushButton.__init(self, parent)

    def mouseReleaseEvent(self, event):
        print "emit"
        self.emit(SIGNAL('step_clicked'), self.objectName(), self)