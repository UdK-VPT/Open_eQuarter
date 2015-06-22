import operator

from PyQt4.QtGui import QLabel, QPushButton, QLineEdit, QItemDelegate, QIcon, QFont, QColor
from PyQt4.QtCore import SIGNAL, QSize, QPoint, QRect, Qt, QAbstractTableModel, QVariant
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class QRemoveRowDelegate(QItemDelegate):

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        """
        Method paints the models item and icon
        :param painter:
        :type painter: QPainter
        :param option:
        :type option: QStyleOptionViewItem
        :param index:
        :type index: QModelIndex
        :return:
        :rtype:
        """
        painter.setPen(Qt.red)
        painter.setFont(QFont('Lucida Grande', 13, weight=QFont.Bold))
        painter.drawText(option.rect, Qt.AlignLeft, ' -')
        painter.setPen(Qt.black)


class QColorRowDelegate(QItemDelegate):

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        """
        Method paints the models item and icon
        :param painter:
        :type painter: QPainter
        :param option:
        :type option: QStyleOptionViewItem
        :param index:
        :type index: QModelIndex
        :return:
        :rtype:
        """
        model = index.model()
        text = model.in_data[index.row()][index.column()]
        color_array = str.split(str(text)[5:-1], ', ')
        r, g, b, a = map(int, color_array)
        color = QColor(r, g, b, a)
        painter.setBrush(color)
        x, y, width, height = option.rect.getCoords()
        painter.drawRect(x+3, y+3, 15, 15)
        painter.setFont(QFont('Lucida Grande', 13))
        painter.drawText(QRect(x+22, y+3, width - 22, height), Qt.AlignLeft, text)


class MyTableModel(QAbstractTableModel):
    def __init__(self, in_data_map, header_data, parent=None, *args):
        """
        :param in_data_map: A dictionary containing color-keys and triple-values
        :type in_data_map: dict
        :param header_data: A list of strings
        :type header_data: list
        :param parent: Parent Window
        :type parent: QWidget
        :param args:
        :type args:
        :return:
        :rtype:
        """
        QAbstractTableModel.__init__(self, parent, *args)

        items = []
        for key, triple in in_data_map.iteritems():
            temp = [key]
            temp += triple
            items.append(temp)

        self.in_data = items
        self.header_data = header_data

    def rowCount(self, parent):
        return len(self.in_data)

    def columnCount(self, parent):
        return len(self.in_data[0]) + 1

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        else:
            if index.column() == 0:
                return QVariant(self.in_data[index.row()][index.column()])
            elif index.column() == len(self.in_data[0]):
                return QVariant('-')
            else:
                return QVariant(self.in_data[index.row()][index.column()])

    def flags(self, model_index):
        between_second_and_last = model_index.column() > 1 and model_index.column() < len(self.in_data[0])
        if between_second_and_last:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif model_index.column() == len(self.in_data[0]):
            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_data[section])
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return QVariant(section)
        else:
            return QVariant()

    def sort(self, column, order):
        """
        Sort the data stored in a column
        :param column: Column that will be sorted
        :type column: int
        :param order: Descending or Ascending
        :type order: SortOrder
        :return:
        :rtype:
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        try:
            self.in_data = sorted(self.in_data, key=operator.itemgetter(column))
            if order == Qt.DescendingOrder:
                self.in_data.reverse()
        except IndexError as OutOfRangeError:
            if column != len(self.in_data[0]):
                print(self.__module__, OutOfRangeError)

        self.emit(SIGNAL("layoutChanged()"))


class QProcessViewDelegate(QItemDelegate):

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        self.margin_left = 5
        self.margin_top = 7
        self.height = 10
        self.icon_size = 17
        self.width = 300

    def paint(self, painter, option, index):
        """
        Method paints the models item and icon
        :param painter:
        :type painter: QPainter
        :param option:
        :type option: QStyleOptionViewItem
        :param index:
        :type index: QModelIndex
        :return:
        :rtype:
        """
        model = index.model()
        item = model.item(index.row())
        text = item.text()

        x_top, y_top, x_btm, y_btm = option.rect.getCoords()
        # print(x_top, y_top, x_btm, y_btm)
        x_top = x_top + 2 * self.margin_left + self.icon_size
        y_top = y_top + self.margin_top
        x_btm = self.width
        y_btm = y_btm + self.height

        try:
            rectangle = QRect(x_top, y_top, x_btm, y_btm)
            # painter.setBrush(Qt.cyan)
            # painter.setPen(Qt.darkCyan)
            # painter.drawRect(rectangle)
            painter.drawText(rectangle, Qt.AlignLeft | Qt.TextWordWrap, text)

            x_top = x_top - self.margin_left - self.icon_size
            y_top = y_top - 1
            rectangle = QRect(x_top, y_top, x_btm, y_btm)
            self.drawCheck(painter, option, rectangle, item.checkState())
        except TypeError as NoneTypeError:
            print(self.__module__, NoneTypeError)


    def drawCheck(self, painter, style_option, rectangle, check_state):
        start_point = QPoint(rectangle.x(), rectangle.y())
        size = QSize(self.icon_size, self.icon_size)
        pixmap = None

        if check_state == 0:
            pixmap = QIcon(":/Controls/icons/openmark.png").pixmap(size)
        if check_state == 1:
            pixmap = QIcon(":/Controls/icons/semiopenmark.png").pixmap(size)
        elif check_state == 2:
            pixmap = QIcon(":/Controls/icons/checkmark.png").pixmap(size)

        painter.drawPixmap(start_point, pixmap)


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
        background_color = 'background-color: qlineargradient(spread:pad, ' \
                           'x1:0.08, y1:0.1, x2:1, y2:0.1, ' \
                           'stop:0 rgba({0}, {1}, {2}, {3}), ' \
                           'stop:0.02 rgba({0}, {1}, {2}, {3}), ' \
                           'stop:0.02 rgba(0, 0, 0, 0));'

        # background_color = 'background-color: qlineargradient(spread:pad,' \
        #                    ' x1:0, y1:0, x2:0.324739, y2:0, ' \
        #                    'stop:0 rgba({0}, {1}, {2}, {3}), ' \
        #                    'stop:0.3 rgba({0}, {1}, {2}, {3}), ' \
        #                    'stop:1 rgba(255, 255, 255, 255));'
        background_color = background_color.format(r, g, b, a)
        self.setStyleSheet(background_color + ' padding-left: 20px;')

class QRemoveEntryButton(QPushButton):

    def __init(self, parent):
        QPushButton.__init(self, parent)

    def mouseReleaseEvent(self, event):
        self.emit(SIGNAL('remove_widget_and_entry'), self)

    def stylize(self):
        self.setMinimumSize(QtCore.QSize(18, 0))
        self.setMaximumSize(QtCore.QSize(20, 20))
        self.setFlat(True)
        self.setText('-')
        self.setStyleSheet(':active { color: rgb(255, 0, 3); font-weight: bold; margin-left: -5px; font-size: 18px; } '
                           ':pressed { color: rgb(255,0,3); border: 0px; margin-left: -2px; background-color: rgb(237,237,237); }')