# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/qt/ui_modular_dialog.ui'
#
# Created: Mon Mar  9 10:16:13 2015
#      by: PyQt4 UI code generator 4.11.2
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

class Ui_Modular_dialog(object):
    def setupUi(self, Modular_dialog):
        Modular_dialog.setObjectName(_fromUtf8("Modular_dialog"))
        Modular_dialog.resize(500, 101)
        Modular_dialog.setFocusPolicy(QtCore.Qt.ClickFocus)
        Modular_dialog.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.buttonBox = QtGui.QDialogButtonBox(Modular_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 50, 120, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textBrowser = QtGui.QTextBrowser(Modular_dialog)
        self.textBrowser.setGeometry(QtCore.QRect(25, 10, 450, 31))
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setStyleSheet(_fromUtf8("background-color: rgb(237,237,237);"))
        self.textBrowser.setFrameShape(QtGui.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Plain)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))

        self.retranslateUi(Modular_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Modular_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Modular_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Modular_dialog)

    def retranslateUi(self, Modular_dialog):
        Modular_dialog.setWindowTitle(_translate("Modular_dialog", "Investigation Area selected", None))
        self.textBrowser.setHtml(_translate("Modular_dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Click \'Ok\' once the investigation area is selected.</p></body></html>", None))

