# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_color_picker_dialog.ui'
#
# Created: Tue Mar 17 13:36:41 2015
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
        color_picker_dialog.resize(687, 285)
        color_picker_dialog.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(color_picker_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line = QtGui.QFrame(color_picker_dialog)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.raster_dlg = QtGui.QWidget(color_picker_dialog)
        self.raster_dlg.setStyleSheet(_fromUtf8(""))
        self.raster_dlg.setObjectName(_fromUtf8("raster_dlg"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.raster_dlg)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chose_raster_info = QtGui.QLabel(self.raster_dlg)
        self.chose_raster_info.setStyleSheet(_fromUtf8(""))
        self.chose_raster_info.setObjectName(_fromUtf8("chose_raster_info"))
        self.horizontalLayout.addWidget(self.chose_raster_info)
        self.layers_dropdown = QtGui.QComboBox(self.raster_dlg)
        self.layers_dropdown.setObjectName(_fromUtf8("layers_dropdown"))
        self.horizontalLayout.addWidget(self.layers_dropdown)
        self.refresh_layers_dropdown = QtGui.QPushButton(self.raster_dlg)
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
        self.horizontalLayout.addWidget(self.refresh_layers_dropdown)
        self.verticalLayout.addWidget(self.raster_dlg)
        self.color_table = QtGui.QGridLayout()
        self.color_table.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.color_table.setContentsMargins(0, -1, -1, -1)
        self.color_table.setObjectName(_fromUtf8("color_table"))
        self.value_one_label = QtGui.QLabel(color_picker_dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.value_one_label.setFont(font)
        self.value_one_label.setObjectName(_fromUtf8("value_one_label"))
        self.color_table.addWidget(self.value_one_label, 0, 2, 1, 1)
        self.value_two_label = QtGui.QLabel(color_picker_dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.value_two_label.setFont(font)
        self.value_two_label.setObjectName(_fromUtf8("value_two_label"))
        self.color_table.addWidget(self.value_two_label, 0, 3, 1, 1)
        self.chosen_color_0 = QColorizedLineEdit(color_picker_dialog)
        self.chosen_color_0.setEnabled(False)
        self.chosen_color_0.setMinimumSize(QtCore.QSize(190, 0))
        self.chosen_color_0.setStyleSheet(_fromUtf8(""))
        self.chosen_color_0.setText(_fromUtf8(""))
        self.chosen_color_0.setObjectName(_fromUtf8("chosen_color_0"))
        self.color_table.addWidget(self.chosen_color_0, 1, 1, 1, 1)
        self.value_one_0 = QtGui.QLineEdit(color_picker_dialog)
        self.value_one_0.setMinimumSize(QtCore.QSize(190, 0))
        self.value_one_0.setObjectName(_fromUtf8("value_one_0"))
        self.color_table.addWidget(self.value_one_0, 1, 2, 1, 1)
        self.chosen_color_label = QtGui.QLabel(color_picker_dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.chosen_color_label.setFont(font)
        self.chosen_color_label.setObjectName(_fromUtf8("chosen_color_label"))
        self.color_table.addWidget(self.chosen_color_label, 0, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.value_two_0 = QtGui.QLineEdit(color_picker_dialog)
        self.value_two_0.setMinimumSize(QtCore.QSize(190, 0))
        self.value_two_0.setObjectName(_fromUtf8("value_two_0"))
        self.color_table.addWidget(self.value_two_0, 1, 3, 1, 1)
        self.remove_entries_0 = QRemoveEntryButton(color_picker_dialog)
        self.remove_entries_0.setMinimumSize(QtCore.QSize(18, 0))
        self.remove_entries_0.setMaximumSize(QtCore.QSize(20, 20))
        self.remove_entries_0.setStyleSheet(_fromUtf8(":active {\n"
"    color: rgb(255, 0, 3);\n"
"    font-weight: bold;\n"
"    margin-left: -5px;\n"
"    font-size: 18px;\n"
"    background-color: rgb(237,237,237);\n"
"}\n"
"\n"
":pressed {\n"
"    color: rgb(255,0,3);\n"
"    border: 0px;    \n"
"    margin-left: -2px;\n"
"    background-color: rgb(237,237,237);\n"
"}\n"
""))
        self.remove_entries_0.setFlat(True)
        self.remove_entries_0.setObjectName(_fromUtf8("remove_entries_0"))
        self.color_table.addWidget(self.remove_entries_0, 1, 4, 1, 1)
        self.row_number_0 = QtGui.QLabel(color_picker_dialog)
        self.row_number_0.setMinimumSize(QtCore.QSize(15, 0))
        self.row_number_0.setObjectName(_fromUtf8("row_number_0"))
        self.color_table.addWidget(self.row_number_0, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.color_table)
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
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(color_picker_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), color_picker_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), color_picker_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(color_picker_dialog)

    def retranslateUi(self, color_picker_dialog):
        color_picker_dialog.setWindowTitle(_translate("color_picker_dialog", "Create Color Palette", None))
        self.chose_raster_info.setText(_translate("color_picker_dialog", "Chose clipped raster layers (*tif files only):", None))
        self.value_one_label.setText(_translate("color_picker_dialog", "Value 1", None))
        self.value_two_label.setText(_translate("color_picker_dialog", "Value 2", None))
        self.chosen_color_label.setText(_translate("color_picker_dialog", "Color-value", None))
        self.remove_entries_0.setToolTip(_translate("color_picker_dialog", "<html><head/><body><p style=\'color: #000000; font-size: 12px; font-weight: normal; margin-left: 5px;\'>Remove entry 1</p></body></html>", None))
        self.remove_entries_0.setText(_translate("color_picker_dialog", "-", None))
        self.row_number_0.setText(_translate("color_picker_dialog", "1", None))

from oeq_ui_classes import QColorizedLineEdit, QRemoveEntryButton
import resources_rc
