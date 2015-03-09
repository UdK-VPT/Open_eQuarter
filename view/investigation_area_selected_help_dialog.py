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

from qt.ui_modular_info_dialog import Ui_ModularInfo_dialog

# create the dialog for zoom to point


class ModularInfo_dialog(QtGui.QDialog, Ui_ModularInfo_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
