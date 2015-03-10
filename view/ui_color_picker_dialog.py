# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_color_picker_dialog.ui'
#
# Created: Tue Mar 10 13:26:42 2015
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

class Ui_color_picker_dialog(object):
    def setupUi(self, color_picker_dialog):
        color_picker_dialog.setObjectName(_fromUtf8("color_picker_dialog"))
        color_picker_dialog.resize(539, 285)
        color_picker_dialog.setStyleSheet(_fromUtf8("QRemoveEntryButton:active {\n"
"    color: rgb(255, 0, 3);\n"
"    font-weight: bold;\n"
"    margin-left: -5px;\n"
"    font-size: 18px;\n"
"    background-color: rgb(237,237,237);\n"
"}\n"
"\n"
"QRemoveEntryButton:pressed {\n"
"    color: rgb(255,0,3);\n"
"    border: 0px;\n"
"    margin-left: -2px;\n"
"    background-color: rgb(237,237,237);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(color_picker_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line = QtGui.QFrame(color_picker_dialog)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.raster_dlg = QtGui.QWidget(color_picker_dialog)
        self.raster_dlg.setObjectName(_fromUtf8("raster_dlg"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.raster_dlg)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(self.raster_dlg)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.layers_dropdown = QtGui.QComboBox(self.raster_dlg)
        self.layers_dropdown.setObjectName(_fromUtf8("layers_dropdown"))
        self.horizontalLayout.addWidget(self.layers_dropdown)
        self.verticalLayout.addWidget(self.raster_dlg)
        self.color_table_widget = QtGui.QWidget(color_picker_dialog)
        self.color_table_widget.setObjectName(_fromUtf8("color_table_widget"))
        self.verticalLayout.addWidget(self.color_table_widget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(color_picker_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(color_picker_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), color_picker_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), color_picker_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(color_picker_dialog)

    def retranslateUi(self, color_picker_dialog):
        color_picker_dialog.setWindowTitle(_translate("color_picker_dialog", "Dialog", None))
        self.label_4.setText(_translate("color_picker_dialog", "Chose clipped raster layers (*tif files only):", None))

