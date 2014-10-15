# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_investigation_area_selected_help_dialog.ui'
#
# Created: Wed Oct 15 12:27:30 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_InvestigationAreaSelectedHelp_dialog(object):
    def setupUi(self, InvestigationAreaSelectedHelp_dialog):
        InvestigationAreaSelectedHelp_dialog.setObjectName(_fromUtf8("InvestigationAreaSelectedHelp_dialog"))
        InvestigationAreaSelectedHelp_dialog.resize(502, 190)
        InvestigationAreaSelectedHelp_dialog.setFocusPolicy(QtCore.Qt.ClickFocus)
        InvestigationAreaSelectedHelp_dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.buttonBox = QtGui.QDialogButtonBox(InvestigationAreaSelectedHelp_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(191, 140, 120, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textBrowser = QtGui.QTextBrowser(InvestigationAreaSelectedHelp_dialog)
        self.textBrowser.setGeometry(QtCore.QRect(25, 10, 450, 111))
        self.textBrowser.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setStyleSheet(_fromUtf8("background-color: rgb(237,237,237);"))
        self.textBrowser.setFrameShape(QtGui.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Plain)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))

        self.retranslateUi(InvestigationAreaSelectedHelp_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InvestigationAreaSelectedHelp_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InvestigationAreaSelectedHelp_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InvestigationAreaSelectedHelp_dialog)

    def retranslateUi(self, InvestigationAreaSelectedHelp_dialog):
        InvestigationAreaSelectedHelp_dialog.setWindowTitle(_translate("InvestigationAreaSelectedHelp_dialog", "How to select the Investigation Area", None))
        self.textBrowser.setHtml(_translate("InvestigationAreaSelectedHelp_dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Cover your investigation area by adding new features (left click to add a new corner, click right when one part of your IA is completely covered). </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Once the whole IA is slected, click \'Ok\' to confirm the selection and to continue the process.</p></body></html>", None))

