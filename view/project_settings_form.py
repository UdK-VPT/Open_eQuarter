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

from functools import partial

from PyQt4 import QtGui

from qt.ui_project_settings_form import Ui_project_settings_form


class ProjectSettings_form(QtGui.QDialog, Ui_project_settings_form):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.defaults = {}

        for field in self.form.findChildren(QtGui.QLineEdit)[:]:
            self.defaults[field.objectName()] = field.text()
            field.textChanged.connect(partial(self.text_changed, field))


    def text_changed(self, input_field):
        if input_field.text() != self.defaults[input_field.objectName()]:
            input_field.setStyleSheet('color: rgb(0,0,0)')

