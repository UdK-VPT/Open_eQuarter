# -*- coding: utf-8 -*-
"""
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
"""

from PyQt4 import QtCore, QtGui
from ui_mainstay_process_dialog import Ui_MainstayProcess_dialog


class MainstayProcess_dialog(QtGui.QDialog, Ui_MainstayProcess_dialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        tool_buttons = self.findChildren(QtGui.QToolButton)
        self.button_to_page_dictionary = {}

        for btn in tool_buttons:
            btn_name = btn.objectName()

            if btn_name.endswith('_btn'):
                page_name = btn_name.replace('_btn', '_page', -1)
                page = self.findChild(QtGui.QWidget, page_name)
                self.button_to_page_dictionary.update({btn_name: page})

    def set_checkbox_on_page(self, checkbox_name, page_name, value):

        if not checkbox_name or checkbox_name.isspace():
            print "A checkbox with the given name " + checkbox_name + " was not found."

        elif not page_name or page_name.isspace():
            print "A page with the given name " + page_name + " was not found."

        elif type(value) is not bool:
            print "A boolean value has to be passed as a third parameter."
        else:
            page = self.findChild(QtGui.QWidget, page_name)
            checkbox = page.findChild(QtGui.QCheckBox, checkbox_name)
            if value:
                checkbox.setCheckState(QtCore.Qt.Checked)
            else:
                checkbox.setCheckState(QtCore.Qt.Unchecked)

    def is_checkbox_on_page_checked(self, checkbox_name, page_name):

        if not checkbox_name or checkbox_name.isspace():
            print "A checkbox with the given name " + checkbox_name + " was not found."

        elif not page_name or page_name.isspace():
            print "A page with the given name " + page_name + " was not found."

        else:
            if self.mainstay_process_widget is not None:
                page = self.mainstay_process_widget.findChild(QtGui.QWidget, page_name)
                return page.findChild(QtGui.QCheckBox, checkbox_name).isChecked()

    def set_progress_button(self, button_name, value):

        if not button_name or button_name.isspace():
            print "A button-checkbox with the given name " + button_name + " was not found."

        elif type(value) is not bool:
            print "A boolean value has to be passed as a third parameter."

        else:
            check_button = self.findChild(QtGui.QToolButton, button_name)
            check_button.setChecked(value)

    def update(self, *__args):

        sender = self.sender()
        sender_name = sender.objectName()

        if type(sender) is QtGui.QToolButton and sender_name.endswith('_btn'):
            page = self.button_to_page_dictionary[sender_name]
            self.process_page.setCurrentWidget(page)
            sender.setChecked(not sender.isChecked())
            sender.setStyleSheet('QToolButton:{background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:0.5, stop:0 rgba(175, 175, 175, 255), stop:1 rgba(230, 230, 230, 203); border: 1px solid rgb(192,192,192);}')
