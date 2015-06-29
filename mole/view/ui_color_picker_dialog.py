# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_color_picker_dialog.ui'
#
# Created: Tue Jun 23 15:39:50 2015
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

class Ui_color_picker_dialog(object):
    def setupUi(self, color_picker_dialog):
        color_picker_dialog.setObjectName(_fromUtf8("color_picker_dialog"))
        color_picker_dialog.resize(658, 385)
        color_picker_dialog.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(color_picker_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line = QtGui.QFrame(color_picker_dialog)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.raster_plugin_dlg = QtGui.QWidget(color_picker_dialog)
        self.raster_plugin_dlg.setStyleSheet(_fromUtf8(""))
        self.raster_plugin_dlg.setObjectName(_fromUtf8("raster_plugin_dlg"))
        self.gridLayout = QtGui.QGridLayout(self.raster_plugin_dlg)
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plugins_dropdown = QtGui.QComboBox(self.raster_plugin_dlg)
        self.plugins_dropdown.setObjectName(_fromUtf8("plugins_dropdown"))
        self.gridLayout.addWidget(self.plugins_dropdown, 1, 1, 1, 1)
        self.chose_raster_info = QtGui.QLabel(self.raster_plugin_dlg)
        self.chose_raster_info.setStyleSheet(_fromUtf8(""))
        self.chose_raster_info.setObjectName(_fromUtf8("chose_raster_info"))
        self.gridLayout.addWidget(self.chose_raster_info, 0, 0, 1, 1)
        self.refresh_layers_dropdown = QtGui.QPushButton(self.raster_plugin_dlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_layers_dropdown.sizePolicy().hasHeightForWidth())
        self.refresh_layers_dropdown.setSizePolicy(sizePolicy)
        self.refresh_layers_dropdown.setMinimumSize(QtCore.QSize(20, 20))
        self.refresh_layers_dropdown.setMaximumSize(QtCore.QSize(27, 27))
        self.refresh_layers_dropdown.setStyleSheet(_fromUtf8(":pressed {\n"
"    background-color: rgb(237, 237, 237);\n"
"}\n"
""))
        self.refresh_layers_dropdown.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh_layers_dropdown.setIcon(icon)
        self.refresh_layers_dropdown.setIconSize(QtCore.QSize(15, 15))
        self.refresh_layers_dropdown.setFlat(True)
        self.refresh_layers_dropdown.setObjectName(_fromUtf8("refresh_layers_dropdown"))
        self.gridLayout.addWidget(self.refresh_layers_dropdown, 0, 2, 1, 1)
        self.refresh_plugins_dropdown = QtGui.QPushButton(self.raster_plugin_dlg)
        self.refresh_plugins_dropdown.setMinimumSize(QtCore.QSize(20, 20))
        self.refresh_plugins_dropdown.setMaximumSize(QtCore.QSize(27, 27))
        self.refresh_plugins_dropdown.setStyleSheet(_fromUtf8(":pressed {\n"
"    background-color: rgb(237, 237, 237);\n"
"}\n"
""))
        self.refresh_plugins_dropdown.setText(_fromUtf8(""))
        self.refresh_plugins_dropdown.setIcon(icon)
        self.refresh_plugins_dropdown.setFlat(True)
        self.refresh_plugins_dropdown.setObjectName(_fromUtf8("refresh_plugins_dropdown"))
        self.gridLayout.addWidget(self.refresh_plugins_dropdown, 1, 2, 1, 1)
        self.layers_dropdown = QtGui.QComboBox(self.raster_plugin_dlg)
        self.layers_dropdown.setObjectName(_fromUtf8("layers_dropdown"))
        self.gridLayout.addWidget(self.layers_dropdown, 0, 1, 1, 1)
        self.chose_plugin_info = QtGui.QLabel(self.raster_plugin_dlg)
        self.chose_plugin_info.setObjectName(_fromUtf8("chose_plugin_info"))
        self.gridLayout.addWidget(self.chose_plugin_info, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.raster_plugin_dlg)
        self.color_table_view = QtGui.QTableView(color_picker_dialog)
        self.color_table_view.setStyleSheet(_fromUtf8("border: 0px;\n"
"background-color: rgb(237, 237, 237);"))
        self.color_table_view.setObjectName(_fromUtf8("color_table_view"))
        self.verticalLayout.addWidget(self.color_table_view)
        self.widget = QtGui.QWidget(color_picker_dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout.addWidget(self.widget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.warning_label = QtGui.QLabel(color_picker_dialog)
        self.warning_label.setStyleSheet(_fromUtf8("color: red;"))
        self.warning_label.setText(_fromUtf8(""))
        self.warning_label.setObjectName(_fromUtf8("warning_label"))
        self.verticalLayout.addWidget(self.warning_label)
        self.buttonBox = QtGui.QDialogButtonBox(color_picker_dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(color_picker_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), color_picker_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), color_picker_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(color_picker_dialog)

    def retranslateUi(self, color_picker_dialog):
        color_picker_dialog.setWindowTitle(_translate("color_picker_dialog", "Create Color Palette", None))
        self.chose_raster_info.setText(_translate("color_picker_dialog", "Chose clipped raster layers (*tif files only):", None))
        self.chose_plugin_info.setText(_translate("color_picker_dialog", "Chose the corresponding plugin:", None))

import resources_rc
