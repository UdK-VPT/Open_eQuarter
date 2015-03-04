# -*- coding: utf-8 -*-
'''
/***************************************************************************
 OpenEQuartersMainDialog
                                 A QGIS plugin
 The plugin automates the setup for investigating an area.
                             -------------------
        begin                : 2014-10-07
        copyright            : (C) 2014 by Kim Gülle / UdK-Berlin
        email                : kimonline@example.com
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

from qt.ui_color_picker_dialog import Ui_color_picker_dialog
from qt.ui_remove_entry_button import QRemoveEntryButton

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
            self.color_table.chi
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




