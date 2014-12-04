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
from ui_investigation_area_selected_dialog import Ui_InvestigationAreaSelected_dialog
from InvestigationAreaSelectedHelp_dialog import InvestigationAreaSelectedHelp_dialog
# create the dialog for zoom to point


class InvestigationAreaSelected_dialog(QtGui.QDialog, Ui_InvestigationAreaSelected_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setContentsMargins(500,500,0,0)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.help_dialog = InvestigationAreaSelectedHelp_dialog()
        self.buttonBox.button(QtGui.QDialogButtonBox.Help).clicked.connect(self.help_dialog.show)


    def set_dialog_text(self, text, title=""):

        if not title.isspace():
            self.setWindowTitle(title)

        if text is not None and not text.isspace():

            html_prefix = ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                            "p, li { white-space: pre-wrap; }\n"
                            "</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">")

            html_postfix = "</p></body></html>"
            self.textBrowser.setHtml(html_prefix + text + html_postfix)
