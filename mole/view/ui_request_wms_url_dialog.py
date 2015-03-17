# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_request_wms_url_dialog.ui'
#
# Created: Tue Mar 17 16:39:49 2015
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

class Ui_RequestWmsUrl_dialog(object):
    def setupUi(self, RequestWmsUrl_dialog):
        RequestWmsUrl_dialog.setObjectName(_fromUtf8("RequestWmsUrl_dialog"))
        RequestWmsUrl_dialog.resize(540, 159)
        self.buttonBox = QtGui.QDialogButtonBox(RequestWmsUrl_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(175, 100, 190, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Abort|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.textBrowser = QtGui.QTextBrowser(RequestWmsUrl_dialog)
        self.textBrowser.setGeometry(QtCore.QRect(35, 30, 490, 31))
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setStyleSheet(_fromUtf8("background-color: rgb(237,237,237);"))
        self.textBrowser.setFrameShape(QtGui.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Plain)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.wms_url = QtGui.QLineEdit(RequestWmsUrl_dialog)
        self.wms_url.setGeometry(QtCore.QRect(40, 60, 460, 22))
        self.wms_url.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.wms_url.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.wms_url.setText(_fromUtf8(""))
        self.wms_url.setObjectName(_fromUtf8("wms_url"))

        self.retranslateUi(RequestWmsUrl_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RequestWmsUrl_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RequestWmsUrl_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RequestWmsUrl_dialog)

    def retranslateUi(self, RequestWmsUrl_dialog):
        RequestWmsUrl_dialog.setWindowTitle(_translate("RequestWmsUrl_dialog", "Open WMS from url", None))
        self.textBrowser.setHtml(_translate("RequestWmsUrl_dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Please enter the WMS-url to the map you want to work with.</span></p></body></html>", None))
        self.wms_url.setPlaceholderText(_translate("RequestWmsUrl_dialog", "http://", None))

