# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_project_does_not_exist_dialog.ui'
#
# Created: Tue Jun  9 11:36:33 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ProjectDoesNotExist_dialog(object):
    def setupUi(self, ProjectDoesNotExist_dialog):
        ProjectDoesNotExist_dialog.setObjectName(_fromUtf8("ProjectDoesNotExist_dialog"))
        ProjectDoesNotExist_dialog.resize(540, 122)
        self.buttonBox = QtGui.QDialogButtonBox(ProjectDoesNotExist_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(175, 70, 190, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Abort|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textBrowser = QtGui.QTextBrowser(ProjectDoesNotExist_dialog)
        self.textBrowser.setGeometry(QtCore.QRect(25, 30, 490, 31))
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setStyleSheet(_fromUtf8("background-color: rgb(237,237,237);"))
        self.textBrowser.setFrameShape(QtGui.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Plain)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))

        self.retranslateUi(ProjectDoesNotExist_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProjectDoesNotExist_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProjectDoesNotExist_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProjectDoesNotExist_dialog)

    def retranslateUi(self, ProjectDoesNotExist_dialog):
        ProjectDoesNotExist_dialog.setWindowTitle(_translate("ProjectDoesNotExist_dialog", "No project found", None))
        self.textBrowser.setHtml(_translate("ProjectDoesNotExist_dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Please save your workspace as a project before calling the Open eQuarter plugin.</span></p></body></html>", None))

