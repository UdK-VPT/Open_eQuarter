# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_color_picker_dialog.ui'
#
# Created: Mon Aug  3 17:56:39 2015
#      by: qgis.PyQt UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui, QtWidgets, QtWebKitWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_color_picker_dialog(object):
    def setupUi(self, color_picker_dialog):
        color_picker_dialog.setObjectName(_fromUtf8("color_picker_dialog"))
        color_picker_dialog.resize(648, 740)
        color_picker_dialog.setStyleSheet(_fromUtf8(""))
        color_picker_dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.verticalLayout = QtWidgets.QVBoxLayout(color_picker_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line = QtWidgets.QFrame(color_picker_dialog)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.raster_plugin_dlg = QtWidgets.QWidget(color_picker_dialog)
        self.raster_plugin_dlg.setStyleSheet(_fromUtf8(""))
        self.raster_plugin_dlg.setObjectName(_fromUtf8("raster_plugin_dlg"))
        self.gridLayout = QtWidgets.QGridLayout(self.raster_plugin_dlg)
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.refresh_layers_dropdown = QtWidgets.QPushButton(self.raster_plugin_dlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
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
        self.plugins_dropdown = QtWidgets.QComboBox(self.raster_plugin_dlg)
        self.plugins_dropdown.setObjectName(_fromUtf8("plugins_dropdown"))
        self.gridLayout.addWidget(self.plugins_dropdown, 1, 1, 1, 1)
        self.chose_plugin_info = QtWidgets.QLabel(self.raster_plugin_dlg)
        self.chose_plugin_info.setObjectName(_fromUtf8("chose_plugin_info"))
        self.gridLayout.addWidget(self.chose_plugin_info, 1, 0, 1, 1)
        self.refresh_plugins_dropdown = QtWidgets.QPushButton(self.raster_plugin_dlg)
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
        self.chose_raster_info = QtWidgets.QLabel(self.raster_plugin_dlg)
        self.chose_raster_info.setStyleSheet(_fromUtf8(""))
        self.chose_raster_info.setObjectName(_fromUtf8("chose_raster_info"))
        self.gridLayout.addWidget(self.chose_raster_info, 0, 0, 1, 1)
        self.layers_dropdown = QtWidgets.QComboBox(self.raster_plugin_dlg)
        self.layers_dropdown.setObjectName(_fromUtf8("layers_dropdown"))
        self.gridLayout.addWidget(self.layers_dropdown, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.raster_plugin_dlg)
        self.color_table_view = QtWidgets.QTableView(color_picker_dialog)
        self.color_table_view.setMinimumSize(QtCore.QSize(550, 250))
        self.color_table_view.setStyleSheet(_fromUtf8("border: 0px;\n"
"background-color: rgb(237, 237, 237);"))
        self.color_table_view.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.color_table_view.setShowGrid(False)
        self.color_table_view.setSortingEnabled(True)
        self.color_table_view.setCornerButtonEnabled(False)
        self.color_table_view.setObjectName(_fromUtf8("color_table_view"))
        self.verticalLayout.addWidget(self.color_table_view)
        self.legend_view = QtWebKitWidgets.QWebView(color_picker_dialog)
        self.legend_view.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.legend_view.setObjectName(_fromUtf8("legend_view"))
        self.verticalLayout.addWidget(self.legend_view)
        self.widget = QtWidgets.QWidget(color_picker_dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout.addWidget(self.widget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.message_label = QtWidgets.QLabel(color_picker_dialog)
        self.message_label.setStyleSheet(_fromUtf8("color: red;"))
        self.message_label.setText(_fromUtf8(""))
        self.message_label.setObjectName(_fromUtf8("message_label"))
        self.verticalLayout.addWidget(self.message_label)
        self.start_colorpicking = QtWidgets.QPushButton(color_picker_dialog)
        self.start_colorpicking.setMinimumSize(QtCore.QSize(20, 20))
        self.start_colorpicking.setMaximumSize(QtCore.QSize(27, 27))
        self.start_colorpicking.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/crosshair.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_colorpicking.setIcon(icon1)
        self.start_colorpicking.setIconSize(QtCore.QSize(25, 25))
        self.start_colorpicking.setFlat(True)
        self.start_colorpicking.setObjectName(_fromUtf8("start_colorpicking"))
        self.verticalLayout.addWidget(self.start_colorpicking)
        self.buttonBox = QtWidgets.QDialogButtonBox(color_picker_dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(color_picker_dialog)
        self.buttonBox.accepted.connect(color_picker_dialog.accept)
        self.buttonBox.rejected.connect(color_picker_dialog.reject)

        QtCore.QMetaObject.connectSlotsByName(color_picker_dialog)

    def retranslateUi(self, color_picker_dialog):
        color_picker_dialog.setWindowTitle(_translate("color_picker_dialog", "Create Color Palette", None))
        self.chose_plugin_info.setText(_translate("color_picker_dialog", "Chose the corresponding plugin:", None))
        self.chose_raster_info.setText(_translate("color_picker_dialog", "Chose clipped raster layers (*tif files only):", None))
        self.start_colorpicking.setToolTip(_translate("color_picker_dialog", "Pick a color from the map", None))


from . import resources_rc
