# -*- coding: utf-8 -*-
'''
/***************************************************************************
 Open eQuarter Dialogs

                             -------------------
        begin                : 2014-10-07
        copyright            : (C) 2014 by Kim Gülle / UdK-Berlin
        email                : firstdayofjune@users.noreply.github.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from collections import OrderedDict
from functools import partial

from ui_color_picker_dialog import Ui_color_picker_dialog
from ui_main_process_dock import Ui_MainProcess_dock, _fromUtf8
from ui_project_does_not_exist_dialog import Ui_ProjectDoesNotExist_dialog
from ui_project_settings_form import Ui_project_settings_form
from ui_modular_info_dialog import Ui_ModularInfo_dialog
from ui_modular_dialog import Ui_Modular_dialog
from ui_request_wms_url_dialog import Ui_RequestWmsUrl_dialog
from oeq_ui_classes import QRemoveEntryButton, QResponsiveGridLayout
from Open_eQuarter.model.grid_matrix import WidgetLinkedListNode, WidgetLinkedList

class ColorPicker_dialog(QDialog, Ui_color_picker_dialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.color_table = QResponsiveGridLayout(self, 1)
        self.color_table.setSizeConstraint(QLayout.SetFixedSize)
        self.color_table.setObjectName(_fromUtf8('color_table'))

        # Table headings
        headings_font = QFont()
        headings_font.setBold(True)
        headings_font.setWeight(75)

        self.row_number_label = QLabel()
        self.row_number_label.setMinimumSize(QSize(15,0))

        self.color_value_label = QLabel()
        self.color_value_label.setText('Color-value')
        self.color_value_label.setFont(headings_font)
        self.color_value_label.setMinimumSize(QSize(200, 0))
        self.color_value_label.setObjectName(_fromUtf8('color_value_label'))

        self.value_one_label = QLabel()
        self.value_one_label.setText('Value 1')
        self.value_one_label.setFont(headings_font)
        self.value_one_label.setMinimumSize(QSize(200, 0))
        self.value_one_label.setObjectName(_fromUtf8('value_one_label'))

        self.value_two_label = QLabel()
        self.value_two_label.setFont(headings_font)
        self.value_two_label.setObjectName(_fromUtf8('value_two_label'))
        self.value_two_label.setMinimumSize(QSize(200, 0))
        self.value_two_label.setText('Value 2')

        self.remove_button_label = QLabel()
        self.remove_button_label.setMinimumSize(QSize(18,0))

        self.color_table.addWidget(self.row_number_label, 0, 0)
        self.color_table.addWidget(self.color_value_label, 0, 1, Qt.AlignLeft)
        self.color_table.addWidget(self.value_one_label, 0, 2)
        self.color_table.addWidget(self.value_two_label, 0, 3)
        self.color_table.addWidget(self.remove_button_label, 0, 4)

        # Initialise first row
        self.row_number_0 = QLabel()
        self.row_number_0.setMinimumSize(QSize(15, 0))
        self.row_number_0.setObjectName(_fromUtf8('row_number_0'))
        self.row_number_0.setText('1')

        self.chosen_color_0 = QLineEdit()
        self.chosen_color_0.setEnabled(False)
        self.chosen_color_0.setObjectName(_fromUtf8('chosen_color_0'))

        self.value_one_0 = QLineEdit()
        self.value_one_0.setObjectName(_fromUtf8('value_one_0'))

        self.value_two_0 = QLineEdit()
        self.value_two_0.setObjectName(_fromUtf8('value_two_0'))

        self.remove_entries_0 = QRemoveEntryButton()
        self.remove_entries_0.setMinimumSize(QSize(18, 0))
        self.remove_entries_0.setMaximumSize(QSize(20, 20))
        self.remove_entries_0.setFlat(True)
        self.remove_entries_0.setObjectName(_fromUtf8('remove_entries_0'))
        self.remove_entries_0.setToolTip('<html><head/><body><p style="color: #000000; font-size: 12px; font-weight: normal; margin-left: 5px;">Remove entry 1</p></body></html>')
        self.remove_entries_0.setText('-')
        self.connect(self.remove_entries_0, SIGNAL('remove_entry'), self.remove_entry)

        # Add first row
        self.color_table.addWidget(self.row_number_0, 1, 0)
        self.color_table.addWidget(self.chosen_color_0, 1, 1)
        self.color_table.addWidget(self.value_one_0, 1, 2)
        self.color_table.addWidget(self.value_two_0, 1, 3)
        self.color_table.addWidget(self.remove_entries_0, 1, 4)
        self.color_table_widget.setLayout(self.color_table)

    def add_color(self, color, value1=0, value2=0):
        """
        Insert a new color (and the values associated to it, if any), into the color-table. Append a new row, afterwards.
        :param color: The color in RGBa
        :type color: QColor
        :param value1: Lower threshold
        :type value1: int
        :param value2: Upper threshold
        :type value2: int
        :return:
        :rtype:
        """
        # substract 1 from size, since indexing starts at 0, add first_responsive_row (the offset to the first input-field)
        last_row = self.color_table.grid_matrix._size - 1 + self.color_table.first_responsive_row
        color_field = self.color_table.itemAtPosition(last_row, 1).widget()
        value_field_one = self.color_table.itemAtPosition(last_row, 2).widget()
        value_field_two = self.color_table.itemAtPosition(last_row, 3).widget()

        color_field.setText('RGBa({}, {}, {}, {})'.format(color.red(), color.green(), color.blue(), color.alpha()))
        if value_field_one.text().isspace():
            value_field_one.setText(str(value1))
        if value_field_two.text().isspace():
            value_field_two.setText(str(value2))

        self.add_row()
        # pixmap = QPixmap(QSize(20,20))
        # painter = QPainter(pixmap)

    def add_row(self):
        """
        Add a new row consisting of number, color, value1, value2 and remove-button to the
        color-picker-table and keep track of the row-number and update the currently empty row.
        :return:
        :rtype:
        """
        row_number = self.color_table.grid_matrix._size
        # the labels object-name has to be 'row_number' to be recognised by the QResponsiveGridLayout's repopulate method
        row_number_label = QLabel(self)
        row_number_label.setObjectName(self.color_table.row_label_name)
        row_number_label.setText('{}'.format(row_number + 1))

        chosen_color = QLineEdit(self)
        chosen_color.setEnabled(False)
        chosen_color.setObjectName('chosen_color_{}'.format(row_number))

        value_one = QLineEdit(self)
        value_one.setObjectName('value_one_{}'.format(row_number))

        value_two = QLineEdit(self)
        value_two.setObjectName('value_two_{}'.format(row_number))

        remove_entries = QRemoveEntryButton(self)
        remove_entries.setObjectName('remove_entries_{}'.format(row_number))
        remove_entries.stylize()
        self.connect(remove_entries, SIGNAL('remove_entry'), self.remove_entry)

        self.color_table.add_row(row_number_label, chosen_color, value_one, value_two, remove_entries)
        self.color_field = chosen_color
        self.value_field_one = value_one
        self.value_field_two = value_two

    #ToDo A different way of removing the entries has to be found.
    def remove_entry(self, button):
        """
        Remove a row consisting of number, color, value1, value2 and remove-button from the
        color-picker-table. The row-number is identified by the characters in the invoking buttons name,
        following the last underscore.
        :param button: The button-object which invoked the remove-call
        :type button: QRemoveEntryButton
        :return:
        :rtype:
        """
        print('remove')
        row_number = str(button.objectName())
        number_start = row_number.rfind('_') + 1
        row_number = int(row_number[number_start:])

        print(row_number)
        print(self.color_table.itemAtPosition(row_number+1, 1).widget())
        print(self.color_field)
        print(self.color_field.objectName())
        if self.color_field:
            bottom_field_number = str(self.color_field.objectName())
            number_start = bottom_field_number.rfind('_') + 1
            bottom_field_number = int(bottom_field_number[number_start:])

            print (row_number, bottom_field_number)

            # clear textfields only, if the first row shall be deleted and no further entries exist
            # if this row would be deleted, errors would occur when appending further values
            if row_number == 0 and row_number == bottom_field_number:
                self.chosen_color_0.clear()
                self.value_one_0.clear()
                self.value_two_0.clear()

            elif row_number == bottom_field_number:
                self.color_field.clear()
                self.value_field_one.clear()
                self.value_field_two.clear()
            else:
                self.color_table.remove_row(row_number)
                self.color_table.repopulate()

                # subtract one since the indexing starts with 0
                last_row = self.color_table.grid_matrix._size - 1

                self.color_field = self.color_table_widget.findChild(QLineEdit, 'chosen_color_{}'.format(last_row))
                self.value_field_one = self.color_table_widget.findChild(QLineEdit, 'value_one_{}'.format(last_row))
                self.value_field_two = self.color_table_widget.findChild(QLineEdit, 'value_two_{}'.format(last_row))

                print(last_row, self.color_field, self.value_field_one, self.value_field_two)

class MainProcess_dock(QDockWidget, Ui_MainProcess_dock):

    def __init__(self):
        QDockWidget.__init__(self)
        self.setupUi(self)
        self.selection_to_page = OrderedDict([])
        self._check_mark = QPixmap(_fromUtf8(':/Controls/icons/checkmark.png'))
        self._open_mark = QPixmap(_fromUtf8(':/Controls/icons/openmark.png'))

        page_triples = []

        # put each page-widget in a list of triples, as they are not sorted properly
        for page in self.process_page.children():
            if isinstance(page, QWidget):
                index = self.process_page.indexOf(page)
                page_triples.append((index, page.accessibleName(), page))

        page_triples_sorted = sorted(page_triples, key=lambda tup: tup[0])
        self.selection_to_page = OrderedDict(map(lambda trip: trip[1:], page_triples_sorted))


        # add page-names to according position in dropdown-menu, so the user can navigate through the process
        for page_number, page in enumerate(self.selection_to_page.keys()):
            self.active_page_dropdown.addItem(page)
            self.active_page_dropdown.setItemData(page_number, self._open_mark, Qt.DecorationRole)

        self.active_page_dropdown.currentIndexChanged.connect(lambda: self.go_to_page(self.active_page_dropdown.currentText()))

        # set the currently displayed widget to the first process-page, otherwise the correct display is not guaranteed
        self.process_page.setCurrentWidget(self.selection_to_page.values()[0])

    def go_to_page(self, selection_name):
        [self.process_page.setCurrentWidget(page)
         for page in self.selection_to_page.values() if selection_name == page.accessibleName()]

    def set_checkbox_on_page(self, checkbox_name, page_name, check_yes_no):
        if isinstance(check_yes_no, bool):
            page = self.findChild(QWidget, page_name)
            checkbox = page.findChild(QPushButton, checkbox_name)

            if checkbox:
                checkbox.setChecked(check_yes_no)

    def is_checkbox_on_page_checked(self, checkbox_name, page_name):
        page = self.process_page.findChild(QWidget, page_name)
        return page.findChild(QPushButton, checkbox_name).isChecked()

    def set_current_page_done(self, value):
        if isinstance(value, bool):
            page_name = self.active_page_dropdown.currentText()
            page = self.selection_to_page[page_name]

            if (page_name) == page.accessibleName():
                index = self.active_page_dropdown.currentIndex()
                self.active_page_dropdown.setItemData(index, self._check_mark, Qt.DecorationRole)
                self.active_page_dropdown.setCurrentIndex((index+1) % len(self.selection_to_page))


class ProjectDoesNotExist_dialog(QDialog, Ui_ProjectDoesNotExist_dialog):

    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)


class ProjectSettings_form(QDialog, Ui_project_settings_form):

    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.defaults = {}

        for field in self.form.findChildren(QLineEdit)[:]:
            self.defaults[field.objectName()] = field.text()
            field.textChanged.connect(partial(self.text_changed, field))


    def text_changed(self, input_field):
        if input_field.text() != self.defaults[input_field.objectName()]:
            input_field.setStyleSheet('color: rgb(0,0,0)')


class ModularInfo_dialog(QDialog, Ui_ModularInfo_dialog):
    def __init__(self):
        QDialog.__init__(self)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)


class Modular_dialog(QDialog, Ui_Modular_dialog):
    def __init__(self):
        QDialog.__init__(self)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setContentsMargins(500, 500, 0, 0)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.help_dialog = ModularInfo_dialog()
        self.buttonBox.button(QDialogButtonBox.Help).clicked.connect(self.help_dialog.show)

    def set_dialog_text(self, text, title=""):

        if not title.isspace():
            self.setWindowTitle(title)

        if text is not None and not text.isspace():

            html_prefix = ('<p align="center" style=" margin-top:0px; margin-bottom:0px; '
                           'margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">')

            html_postfix = "</p>"
            browser_text = html_prefix + text + html_postfix
            self.textBrowser.setHtml(QApplication.translate('InvestigationAreaSelected_dialog', browser_text, None))


class RequestWmsUrl_dialog(QDialog, Ui_RequestWmsUrl_dialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)