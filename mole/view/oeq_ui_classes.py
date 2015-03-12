from PyQt4.QtGui import QLabel, QPushButton, QLineEdit
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class QClickableLabel(QLabel):

    def __init(self, parent):
        QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))


class QProcessButton(QPushButton):

    def __init(self, parent):
        QPushButton.__init(self, parent)

    def mouseReleaseEvent(self, event):
        self.emit(SIGNAL('process_button_click'), self.objectName(), self)


class QColorizedLineEdit(QLineEdit):

    def __init__(self, parent):
        QLineEdit.__init__(self, parent)

    def colorize(self, r, g, b, a):

        background_color = 'background-color: qlineargradient(spread:pad,' \
                           ' x1:0, y1:0, x2:0.324739, y2:0, ' \
                           'stop:0 rgba({0}, {1}, {2}, {3}), ' \
                           'stop:0.3 rgba({0}, {1}, {2}, {3}), ' \
                           'stop:1 rgba(255, 255, 255, 255));'
        background_color = background_color.format(r, g, b, a)
        self.setStyleSheet(background_color)

class QRemoveEntryButton(QPushButton):

    def __init(self, parent):
        QPushButton.__init(self, parent)

    def mouseReleaseEvent(self, event):
        self.emit(SIGNAL('remove_entry'), self)

    def stylize(self):
        self.setMinimumSize(QtCore.QSize(18, 0))
        self.setMaximumSize(QtCore.QSize(20, 20))
        self.setFlat(True)
        self.setText('-')
        self.setStyleSheet(':active { color: rgb(255, 0, 3); font-weight: bold; margin-left: -5px; font-size: 18px; } '
                           ':pressed { color: rgb(255,0,3); border: 0px; margin-left: -2px; background-color: rgb(237,237,237); }')