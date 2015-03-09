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
from oeq_ui_classes import QRemoveEntryButton
from ui_main_process_dock import Ui_MainProcess_dock, _fromUtf8
from ui_project_does_not_exist_dialog import Ui_ProjectDoesNotExist_dialog
from ui_project_settings_form import Ui_project_settings_form
from ui_modular_info_dialog import Ui_ModularInfo_dialog
from ui_modular_dialog import Ui_Modular_dialog
from ui_request_wms_url_dialog import Ui_RequestWmsUrl_dialog

class ColorPicker_dialog(QDialog, Ui_color_picker_dialog):

    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.rows = 1
        self.id = 0
        self.color_field = self.chosen_color_0
        self.value_field_one = self.value_one_0
        self.value_field_two = self.value_two_0

        self.connect(self.remove_entries_0, SIGNAL('remove_entry'), self.remove_entry)

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
        self.color_field.setText('RGBa({}, {}, {}, {})'.format(color.red(), color.green(), color.blue(), color.alpha()))
        if self.value_field_one.text().isspace():
            self.value_field_one.setText(str(value1))
        if self.value_field_two.text().isspace():
            self.value_field_two.setText(str(value2))

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
        self.rows += 1
        self.id +=1

        row_number = QLabel(self)
        row_number.setObjectName('row_number_{}'.format(self.id))
        row_number.setText(str(self.rows))
        self.color_table.addWidget(row_number, self.rows,0, 1, 1)

        chosen_color = QLineEdit(self)
        chosen_color.setEnabled(False)
        chosen_color.setObjectName('chosen_color_{}'.format(self.id))
        self.color_table.addWidget(chosen_color, self.rows, 1, 1, 1)

        value_one = QLineEdit(self)
        value_one.setObjectName('value_one_{}'.format(self.id))
        self.color_table.addWidget(value_one, self.rows, 2, 1, 1)

        value_two = QLineEdit(self)
        value_two.setObjectName('value_two_{}'.format(self.id))
        self.color_table.addWidget(value_two, self.rows, 3, 1, 1)

        remove_entries = QRemoveEntryButton(self)
        remove_entries.setObjectName('remove_entries_{}'.format(self.id))
        remove_entries.stylize()
        self.connect(remove_entries, SIGNAL('remove_entry'), self.remove_entry)
        self.color_table.addWidget(remove_entries, self.rows, 4, 1, 1)

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
        try:
            row_number = str(button.objectName())
            underscore = button.objectName().rfind('_')
            row_number = row_number[underscore+1:]
            color_field = 'chosen_color_{}'.format(row_number)
            color_field = getattr(self, color_field)

            # clear textfields only, if the first row shall be deleted and no further entries exist
            # if this row would be deleted, errors would occur when appending further values
            if self.rows == 1:
                exec('self.chosen_color_{}.clear()'.format(row_number))
                exec('self.value_one_{}.clear()'.format(row_number))
                exec('self.value_two_{}.clear()'.format(row_number))

            elif not color_field.text().isspace():
                exec('self.color_table.removeWidget(self.row_number_{})'.format(row_number))
                exec('self.color_table.removeWidget(self.chosen_color_{})'.format(row_number))
                exec('self.color_table.removeWidget(self.value_one_{})'.format(row_number))
                exec('self.color_table.removeWidget(self.value_two_{})'.format(row_number))
                exec('self.color_table.removeWidget(self.remove_entries_{})'.format(row_number))
                self.rows -= 1

        except AttributeError as Att_Error:
            print(Att_Error)


class MainProcess_dock(QDockWidget, Ui_MainProcess_dock):

    def __init__(self):
        QDockWidget.__init__(self)
        self.setupUi(self)
        self.selection_to_page = OrderedDict([])
        self._check_mark = QPixmap(_fromUtf8(":/Controls/icons/checkmark.png"))
        self._open_mark = QPixmap(_fromUtf8(":/Controls/icons/openmark.png"))

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