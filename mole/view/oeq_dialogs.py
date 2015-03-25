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
from oeq_ui_classes import QRemoveEntryButton, QColorizedLineEdit
from ui_main_process_dock import Ui_MainProcess_dock, _fromUtf8
from ui_project_does_not_exist_dialog import Ui_ProjectDoesNotExist_dialog
from ui_project_settings_form import Ui_project_settings_form
from ui_modular_info_dialog import Ui_ModularInfo_dialog
from ui_modular_dialog import Ui_Modular_dialog
from ui_request_wms_url_dialog import Ui_RequestWmsUrl_dialog
from mole.model.file_manager import ColorEntryManager, MunicipalInformationTree


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
        self.row_offset = 1
        self.row_count = 2
        self.connect(self.remove_entries_0, SIGNAL('remove_entry'), self.remove_entry)
        self.color_entry_manager = ColorEntryManager()
        self.recent_layer = ''

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
        layer = self.layers_dropdown.currentText()
        self.recent_layer = layer
        color_map = self.color_entry_manager.layer_values_map[layer]
        color_key = 'RGBa({}, {}, {}, {})'.format(color.red(), color.green(), color.blue(), color.alpha())
        if color_map.has_key(color_key):
            self.warning_label.setText('Attention: Color {} is defined already.'.format(color_key))

        else:
            self.warning_label.clear()
            self.color_entry_manager.add_color_value_triple_to_layer((color_key, 0, 0), layer)

            last_row = self.row_count - self.row_offset
            color_field = self.color_table.itemAtPosition(last_row, 1).widget()
            parameter_name = self.color_table.itemAtPosition(last_row, 2).widget()
            value_field_one = self.color_table.itemAtPosition(last_row, 3).widget()
            value_field_two = self.color_table.itemAtPosition(last_row, 4).widget()

            color_field.setText(color_key)
            color_field.colorize(color.red(), color.green(), color.blue(), color.alpha())
            if value_field_one.text().isspace():
                value_field_one.setText(str(value1))
            if value_field_two.text().isspace():
                value_field_two.setText(str(value2))

            self.add_row()

    def restore_color_value_pairs(self, layer):
        try:
            color_map = self.color_entry_manager.layer_values_map[layer]
            row = self.row_offset
            for color, values in color_map.iteritems():
                color_field = self.color_table.itemAtPosition(row, 1).widget()
                value_field_one = self.color_table.itemAtPosition(row, 2).widget()
                value_field_two = self.color_table.itemAtPosition(row, 3).widget()
                row += 1
                color_field.setText(color)
                color = color[5:-1]
                colors = color.split(',')
                color_field.colorize(colors[0], colors[1], colors[2], colors[3])
                value_field_one.setText(values[0])
                value_field_two.setText(values[1])
                self.add_row()

        except KeyError, Error:
            print(Error)

    def update_color_values(self):
        grid = self.color_table
        removal = []
        for i in range(0, self.row_count-2):
            row = i + self.row_offset
            color = grid.itemAtPosition(row, 1).widget().text()
            para_name = grid.itemAtPosition(row, 2).widget().text()
            value1 = grid.itemAtPosition(row, 3).widget().text()
            value2 = grid.itemAtPosition(row, 4).widget().text()
            removal.append(grid.itemAtPosition(row, 5).widget())
            self.color_entry_manager.add_color_value_triple_to_layer((color, value1, value2), self.recent_layer)

        for remove_button in removal:
            self.remove_entry(remove_button)

        layer = self.layers_dropdown.currentText()
        self.restore_color_value_pairs(layer)
        self.recent_layer = layer

    def add_row(self):
        """
        Add a new row consisting of number, color, value1, value2 and remove-button to the
        color-picker-table and keep track of the row-number and update the currently empty row.
        :return:
        :rtype:
        """
        entry_number = self.row_count - self.row_offset + 1
        current_row = self.row_count
        row_number = QLabel(self)
        row_number.setObjectName('row_number_{}'.format(current_row - 1))
        row_number.setText(str(entry_number))
        self.color_table.addWidget(row_number, current_row, 0, 1, 1)

        chosen_color = QColorizedLineEdit(self)
        chosen_color.setEnabled(False)
        chosen_color.setObjectName('chosen_color_{}'.format(current_row - 1))
        self.color_table.addWidget(chosen_color, current_row, 1, 1, 1)

        parameter_name = QLineEdit(self)
        parameter_name.setObjectName('parameter_name_{}'.format(current_row - 1))
        self.color_table.addWidget(parameter_name, current_row, 2, 1, 1)

        value_one = QLineEdit(self)
        value_one.setObjectName('value_one_{}'.format(current_row - 1))
        self.color_table.addWidget(value_one, current_row, 3, 1, 1)

        value_two = QLineEdit(self)
        value_two.setObjectName('value_two_{}'.format(current_row - 1))
        self.color_table.addWidget(value_two, current_row, 4, 1, 1)

        remove_entries = QRemoveEntryButton(self)
        remove_entries.setObjectName('remove_entries_{}'.format(current_row - 1))
        remove_entries.stylize()
        self.connect(remove_entries, SIGNAL('remove_entry'), self.remove_entry)
        self.color_table.addWidget(remove_entries, current_row, 5, 1, 1)
        self.row_count += 1

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
        row_number = str(button.objectName())
        underscore = button.objectName().rfind('_')
        row_number = int(row_number[underscore+1:])
        row_number += self.row_offset
        last_row = self.row_count - 1

        number_field = self.color_table.itemAtPosition(row_number, 0).widget()
        color_field = self.color_table.itemAtPosition(row_number, 1).widget()
        parameter_name = self.color_table.itemAtPosition(row_number, 2).widget()
        value_one = self.color_table.itemAtPosition(row_number, 3).widget()
        value_two = self.color_table.itemAtPosition(row_number, 4).widget()
        remove_button = self.color_table.itemAtPosition(row_number, 5).widget()

        if row_number == last_row:
            color_field.clear()
            value_one.clear()
            value_two.clear()

        else:
            self.color_table.removeWidget(number_field)
            self.color_table.removeWidget(color_field)
            self.color_table.removeWidget(parameter_name)
            self.color_table.removeWidget(value_one)
            self.color_table.removeWidget(value_two)
            self.color_table.removeWidget(remove_button)

            number_field.deleteLater()
            color_field.deleteLater()
            parameter_name.deleteLater()
            value_one.deleteLater()
            value_two.deleteLater()
            remove_button.deleteLater()
            self.row_count -= 1
            self.renumber(row_number)

    def renumber(self, empty_row):

        for i in range(empty_row, self.row_count):
            number_field = self.color_table.itemAtPosition(i+1, 0).widget()
            color_field = self.color_table.itemAtPosition(i+1, 1).widget()
            parameter_name = self.color_table.itemAtPosition(i+1, 2).widget()
            value_one = self.color_table.itemAtPosition(i+1, 3).widget()
            value_two = self.color_table.itemAtPosition(i+1, 4).widget()
            remove_button = self.color_table.itemAtPosition(i+1, 5).widget()

            self.color_table.removeWidget(number_field)
            self.color_table.removeWidget(color_field)
            self.color_table.removeWidget(parameter_name)
            self.color_table.removeWidget(value_one)
            self.color_table.removeWidget(value_two)
            self.color_table.removeWidget(remove_button)

            number_field.setObjectName('row_number_{}'.format(i - self.row_offset))
            color_field.setObjectName('chosen_color_{}'.format(i - self.row_offset))
            parameter_name.setObjectName('parameter_name_{}'.format(i - self.row_offset))
            value_one.setObjectName('value_one_{}'.format(i - self.row_offset))
            value_two.setObjectName('value_two_{}'.format(i - self.row_offset))
            remove_button.setObjectName('remove_entries_{}'.format(i - self.row_offset))
            number_field.setText(str(i - self.row_offset + 1))

            self.color_table.addWidget(number_field, i, 0)
            self.color_table.addWidget(color_field, i, 1)
            self.color_table.addWidget(parameter_name, i, 2)
            self.color_table.addWidget(value_one, i, 3)
            self.color_table.addWidget(value_two, i, 4)
            self.color_table.addWidget(remove_button, i, 5)


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
        self.municipals = [{}]
        self.location_postal.editingFinished.connect(self.find_municipal_information)
        self.municipal_information = MunicipalInformationTree()

        if self.municipal_information.tree == {}:
            self.municipal_information.split_data_to_tree_model()

        for field in self.form.findChildren(QLineEdit)[:]:
            self.defaults[field.objectName()] = field.text()
            field.textChanged.connect(partial(self.text_changed, field))

    def text_changed(self, input_field):
        if input_field.text() != self.defaults[input_field.objectName()]:
            input_field.setStyleSheet('color: rgb(0,0,0)')

    def find_municipal_information(self):
        postcode = self.location_postal.text()

        if postcode:
            try:
                l0_key = postcode[0]
                l1_key = postcode[1]
                l2_key = postcode[2:]
                municipals = self.municipal_information.tree[l0_key][l1_key][l2_key]
            except (KeyError, ValueError):
                self.location_postal.setStyleSheet('color: rgb(255, 0, 0)')
                return

            self.municipals = municipals
            if len(municipals) == 1:
                self.lineedit_city_layout()
                self.fill_municipal_information(0)

            elif len(municipals) > 1:
                self.combobox_city_layout()
                self.location_city.clear()

                for municipal in municipals:
                    self.location_city.addItem(_fromUtf8(municipal['NAME']))

                self.location_city.currentIndexChanged.connect(self.fill_municipal_information)
                self.fill_municipal_information(0)

    def fill_municipal_information(self, index):
        municipal = self.municipals[index]

        if issubclass(type(self.location_city), QLineEdit):
            city_name = _fromUtf8(municipal['NAME'])
            self.location_city.setText(city_name)

        pop_dens = '{}'.format(municipal['POP_DENS'])
        avg_yoc = '{}'.format(municipal['AVG_YOC'])
        self.average_build_year.setText(avg_yoc)
        self.population_density.setText(pop_dens)

    def combobox_city_layout(self):
        location_box = self.gridLayout.findChild(QHBoxLayout, 'location_layout')
        city_edit = location_box.itemAt(0).widget()

        if isinstance(city_edit, QLineEdit):
            location_box.removeWidget(city_edit)
            city_edit.deleteLater()
            self.location_city = QComboBox()
            self.location_city.setObjectName('location_city')
            location_box.insertWidget(0, self.location_city)

    def lineedit_city_layout(self):
        location_box = self.gridLayout.findChild(QHBoxLayout, 'location_layout')
        city_edit = location_box.itemAt(0).widget()

        if isinstance(city_edit, QComboBox):
            location_box.removeWidget(city_edit)
            city_edit.deleteLater()
            self.location_city = QLineEdit(self.form)
            self.location_city.setMinimumSize(QSize(0, 0))
            self.location_city.setObjectName(_fromUtf8("location_city"))
            self.location_city.setStyleSheet('color: rgb(0,0,0)')
            location_box.insertWidget(0, self.location_city)


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