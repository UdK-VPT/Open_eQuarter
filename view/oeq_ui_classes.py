from PyQt4.QtGui import QLabel, QPushButton, QGridLayout
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from Open_eQuarter.model import grid_matrix

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


class QResponsiveGridLayout(QGridLayout):

    def __init__(self, parent, first_responsive_row=0):
        QGridLayout.__init__(self, parent)
        self.first_responsive_row = first_responsive_row
        self.grid_matrix = grid_matrix.WidgetLinkedList()

    def add_row(self, item, *items):

        row = self.rowCount()

        self.addWidget(item, row, 0)

        for i, item in enumerate(items):
            self.addWidget(item, row, i+1)

    def addWidget(self, widget, row=None, column=None, alignment=0):
        if alignment:
            QGridLayout.addWidget(self, widget, row, column, alignment)
        else:
            QGridLayout.addWidget(self, widget, row, column)

        # Every widget with a row-number less equal first_responsive_row must be deletable and therefore be tracked in the grid_matrix
        # Furthermore the widgets are assumed to be added in order of appearance
        if row >= self.first_responsive_row:
            matrix_index = row - self.first_responsive_row

            node = self.grid_matrix.get_node_at_position(matrix_index)
            if node:
                node.add_widget(widget)
            else:
                node = grid_matrix.WidgetLinkedListNode()
                node.add_widget(widget)
                self.grid_matrix.add_node(node)