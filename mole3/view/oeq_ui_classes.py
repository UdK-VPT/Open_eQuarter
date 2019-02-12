import operator

from qgis.PyQt.QtGui import QLabel, QPushButton, QLineEdit, QItemDelegate, QIcon, QFont, QColor, QStyle
from qgis.PyQt.QtCore import SIGNAL, QSize, QPoint, QRect, Qt, QAbstractTableModel
from qgis.PyQt import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class QColorTableDelegate(QItemDelegate):
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
        if option.state == QStyle.State_Editing:
            print('Edit')

        if index.column() == 4:
            painter.save()
            painter.setPen(Qt.red)
            painter.setFont(QFont('Lucida Grande', 17, weight=QFont.Bold))
            painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, ' -')
            painter.restore()

        else:
            model = index.model()
            text = model.data(index, Qt.DisplayRole)
            margin = 3
            x, y, width, height = option.rect.getCoords()
            painter.setBrush(Qt.white)
            painter.setFont(QFont('Lucida Grande', 13))

            if 2 <= index.column() <= 3:
                painter.setPen(QColor(155, 155, 155))
                painter.drawRect(x+margin, y+margin, width-2*margin-x, height-y-2*margin)
                painter.setPen(Qt.black)
                rect = QRect(x, y+margin, width-x, height-y-2*margin)
                painter.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, str(text))
            else:
                painter.setPen(QColor(208, 208, 208))
                painter.drawRect(x+margin, y+margin, width-2*margin-x, height-y-2*margin)
                painter.setPen(Qt.black)

                if index.column() == 0:
                    color_array = str.split(str(text)[5:-1], ', ')
                    r, g, b, a = list(map(int, color_array))
                    color = QColor(r, g, b, a)
                    painter.setBrush(color)
                    color_box_size = 15
                    offset = (height - color_box_size - y) / 2
                    painter.drawRect(x+offset, y+offset, color_box_size, color_box_size)
                    painter.drawText(QRect(x+color_box_size+offset+offset,
                                           y+offset,
                                           width - (color_box_size+2*offset),
                                           height),
                                     Qt.AlignLeft, text)
                else:
                    painter.drawText(QRect(x+10, y+margin,
                                           width-10-x, height-y-2*margin),
                                     Qt.AlignLeft | Qt.AlignVCenter, text)


class QColorTableModel(QAbstractTableModel):
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
        self.in_data = in_data_map
        self.header_data = header_data

    def rowCount(self, model_index):
        try:
            return len(self.in_data)
        except IndexError as IndexOutOfBounds_Err:
            print((self.__module__, IndexOutOfBounds_Err))
            return 2

    def columnCount(self, mode_index):
        try:
            return len(list(self.in_data.values())[0]) + 2
        except IndexError as IndexOutOfBounds_Err:
            print((self.__module__, IndexOutOfBounds_Err))
            return len(self.header_data)

    def data(self, index, role):
        '''

        :param index:
        :type index: QModelIndex
        :param role:
        :type role:
        :return:
        :rtype:
        '''
        if not index.isValid():
            return None
        elif role == Qt.EditRole:
            color_key = list(self.in_data.keys())[index.row()]
            if index.column() == 0:
                return color_key
            elif index.column() == self.columnCount(index):
                return '-'
            else:
                value_triple = self.in_data[color_key]
                return value_triple[index.column()-1]
        elif role == Qt.DisplayRole:
            color_key = list(self.in_data.keys())[index.row()]
            if index.column() == 0:
                return color_key

            if 0 < index.column() < self.columnCount(index):
                value_triple = self.in_data[color_key]
                return value_triple[index.column()-1]
            else:
                return '-'

        else:
            return None

    def setData(self, index, data, display_role=None):
        '''
        Change the model according to the changes on the UI-component.
        :param index:
        :type index: QModelIndex
        :param variant:
        :type variant: QVariant
        :param display_role:
        :type display_role:
        :return: True, if the data was changed successfully
        :rtype: bool
        '''
        if display_role == Qt.EditRole:
            row = index.row()
            col = index.column()
            key = list(self.in_data.keys())[row]
            self.in_data[key][col-1] = data
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def flags(self, model_index):
        between_second_and_last = 2 <= model_index.column() < 4
        if between_second_and_last:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header_data[section]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section
        else:
            return None

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
            items = []
            for key, triple in self.in_data.items():
                temp = [key]
                temp += triple
                items.append(temp)
            # print('Items:')
            # print(items)
            sorted_values = sorted(items, key=lambda value: value[column])
            # print('Sorted by {}:'.format(column))
            # print(sorted_values)
            if order == Qt.DescendingOrder:
                sorted_values.reverse()
            # print(sorted_values)

            self.in_data.clear()
            for quadruple in sorted_values:
                key = quadruple[0]
                values = quadruple[1:]
                self.in_data[key] = values
                # print('Data:\t', self.in_data)
        except IndexError as OutOfRangeError:
            print((self.__module__, OutOfRangeError))

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
            print((self.__module__, NoneTypeError))


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