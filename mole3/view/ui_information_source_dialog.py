# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/wk/Tresors/VPT/Open eQuarter/Development/oeq_git/mole/view/ui_information_source_dialog.ui'
#
# Created: Fri Aug 21 14:44:00 2015
#      by: qgis.PyQt UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui

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

class Ui_InformationSource_dialog(object):
    def setupUi(self, InformationSource_dialog):
        InformationSource_dialog.setObjectName(_fromUtf8("InformationSource_dialog"))
        InformationSource_dialog.resize(457, 419)
        InformationSource_dialog.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(InformationSource_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridWidget = QtGui.QWidget(InformationSource_dialog)
        self.gridWidget.setStyleSheet(_fromUtf8("QPushButton {\n"
"    margin-bottom: 3px;\n"
"}\n"
"\n"
"QLabel {\n"
"    margin-top: 2px;\n"
"}\n"
"\n"
"#blind1 {\n"
"    border: none;\n"
"    color: rgb(237, 237, 237);\n"
"}\n"
"\n"
"#blind2 {\n"
"    border: none;\n"
"    color: rgb(237, 237, 237);\n"
"}\n"
"\n"
"#blind3 {\n"
"    border: none;\n"
"    color: rgb(237, 237, 237);\n"
"}\n"
"\n"
"#blind4 {\n"
"    border: none;\n"
"    color: rgb(237, 237, 237);\n"
"}"))
        self.gridWidget.setObjectName(_fromUtf8("gridWidget"))
        self.grid = QtGui.QGridLayout(self.gridWidget)
        self.grid.setMargin(0)
        self.grid.setVerticalSpacing(0)
        self.grid.setObjectName(_fromUtf8("grid"))
        self.open_csv_btn = QtGui.QPushButton(self.gridWidget)
        self.open_csv_btn.setMaximumSize(QtCore.QSize(21, 21))
        self.open_csv_btn.setObjectName(_fromUtf8("open_csv_btn"))
        self.grid.addWidget(self.open_csv_btn, 16, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridWidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 25))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.grid.addWidget(self.label_4, 15, 0, 1, 4)
        self.open_shapefile_btn = QtGui.QPushButton(self.gridWidget)
        self.open_shapefile_btn.setMaximumSize(QtCore.QSize(21, 21))
        self.open_shapefile_btn.setObjectName(_fromUtf8("open_shapefile_btn"))
        self.grid.addWidget(self.open_shapefile_btn, 12, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridWidget)
        self.label_3.setMinimumSize(QtCore.QSize(0, 25))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.grid.addWidget(self.label_3, 11, 0, 1, 4)
        self.label = QtGui.QLabel(self.gridWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label.setObjectName(_fromUtf8("label"))
        self.grid.addWidget(self.label, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.grid.addWidget(self.label_5, 9, 0, 1, 1)
        self.gtiff = QtGui.QLineEdit(self.gridWidget)
        self.gtiff.setObjectName(_fromUtf8("gtiff"))
        self.grid.addWidget(self.gtiff, 10, 2, 1, 1)
        self.blind3 = QtGui.QPushButton(self.gridWidget)
        self.blind3.setMaximumSize(QtCore.QSize(21, 21))
        self.blind3.setText(_fromUtf8(""))
        self.blind3.setFlat(False)
        self.blind3.setObjectName(_fromUtf8("blind3"))
        self.grid.addWidget(self.blind3, 13, 3, 1, 1)
        self.dxf = QtGui.QLineEdit(self.gridWidget)
        self.dxf.setObjectName(_fromUtf8("dxf"))
        self.grid.addWidget(self.dxf, 14, 2, 1, 1)
        self.label_13 = QtGui.QLabel(self.gridWidget)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.grid.addWidget(self.label_13, 4, 0, 1, 1)
        self.blind4 = QtGui.QPushButton(self.gridWidget)
        self.blind4.setMaximumSize(QtCore.QSize(21, 21))
        self.blind4.setText(_fromUtf8(""))
        self.blind4.setObjectName(_fromUtf8("blind4"))
        self.grid.addWidget(self.blind4, 4, 3, 1, 1)
        self.label_12 = QtGui.QLabel(self.gridWidget)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.grid.addWidget(self.label_12, 2, 0, 1, 1)
        self.layer_name = QtGui.QLineEdit(self.gridWidget)
        self.layer_name.setObjectName(_fromUtf8("layer_name"))
        self.grid.addWidget(self.layer_name, 5, 2, 1, 1)
        self.label_11 = QtGui.QLabel(self.gridWidget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.grid.addWidget(self.label_11, 5, 0, 1, 1)
        self.blind2 = QtGui.QPushButton(self.gridWidget)
        self.blind2.setMaximumSize(QtCore.QSize(21, 21))
        self.blind2.setText(_fromUtf8(""))
        self.blind2.setFlat(False)
        self.blind2.setObjectName(_fromUtf8("blind2"))
        self.grid.addWidget(self.blind2, 9, 3, 1, 1)
        self.open_dxf_btn = QtGui.QPushButton(self.gridWidget)
        self.open_dxf_btn.setMaximumSize(QtCore.QSize(21, 21))
        self.open_dxf_btn.setObjectName(_fromUtf8("open_dxf_btn"))
        self.grid.addWidget(self.open_dxf_btn, 14, 3, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.grid.addWidget(self.label_6, 10, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.gridWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.grid.addWidget(self.label_8, 13, 0, 1, 1)
        self.wms = QtGui.QLineEdit(self.gridWidget)
        self.wms.setObjectName(_fromUtf8("wms"))
        self.grid.addWidget(self.wms, 9, 2, 1, 1)
        self.blind1 = QtGui.QPushButton(self.gridWidget)
        self.blind1.setMaximumSize(QtCore.QSize(21, 21))
        self.blind1.setText(_fromUtf8(""))
        self.blind1.setCheckable(False)
        self.blind1.setAutoDefault(True)
        self.blind1.setFlat(False)
        self.blind1.setObjectName(_fromUtf8("blind1"))
        self.grid.addWidget(self.blind1, 5, 3, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.grid.addWidget(self.label_7, 12, 0, 1, 1)
        self.extension_dropdown = QtGui.QComboBox(self.gridWidget)
        self.extension_dropdown.setMaximumSize(QtCore.QSize(16777215, 26))
        self.extension_dropdown.setObjectName(_fromUtf8("extension_dropdown"))
        self.grid.addWidget(self.extension_dropdown, 3, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridWidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 25))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.grid.addWidget(self.label_2, 8, 0, 1, 4)
        self.wfs = QtGui.QLineEdit(self.gridWidget)
        self.wfs.setObjectName(_fromUtf8("wfs"))
        self.grid.addWidget(self.wfs, 13, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.grid.addWidget(self.label_9, 14, 0, 1, 1)
        self.shp = QtGui.QLineEdit(self.gridWidget)
        self.shp.setObjectName(_fromUtf8("shp"))
        self.grid.addWidget(self.shp, 12, 2, 1, 1)
        self.open_geotiff_btn = QtGui.QPushButton(self.gridWidget)
        self.open_geotiff_btn.setMaximumSize(QtCore.QSize(21, 21))
        self.open_geotiff_btn.setObjectName(_fromUtf8("open_geotiff_btn"))
        self.grid.addWidget(self.open_geotiff_btn, 10, 3, 1, 1)
        self.label_10 = QtGui.QLabel(self.gridWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.grid.addWidget(self.label_10, 16, 0, 1, 1)
        self.csv = QtGui.QLineEdit(self.gridWidget)
        self.csv.setObjectName(_fromUtf8("csv"))
        self.grid.addWidget(self.csv, 16, 2, 1, 1)
        self.field_id = QtGui.QLineEdit(self.gridWidget)
        self.field_id.setObjectName(_fromUtf8("field_id"))
        self.grid.addWidget(self.field_id, 4, 2, 1, 1)
        self.stateBox = QtGui.QCheckBox(self.gridWidget)
        self.stateBox.setEnabled(True)
        self.stateBox.setChecked(False)
        self.stateBox.setTristate(False)
        self.stateBox.setObjectName(_fromUtf8("stateBox"))
        self.grid.addWidget(self.stateBox, 17, 2, 3, 1)
        self.label_14 = QtGui.QLabel(self.gridWidget)
        self.label_14.setMinimumSize(QtCore.QSize(0, 25))
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.grid.addWidget(self.label_14, 17, 0, 1, 1)
        self.verticalLayout.addWidget(self.gridWidget)
        self.buttonBox = QtGui.QDialogButtonBox(InformationSource_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.NoButton)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(InformationSource_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InformationSource_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InformationSource_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InformationSource_dialog)
        InformationSource_dialog.setTabOrder(self.extension_dropdown, self.field_id)
        InformationSource_dialog.setTabOrder(self.field_id, self.layer_name)
        InformationSource_dialog.setTabOrder(self.layer_name, self.wms)
        InformationSource_dialog.setTabOrder(self.wms, self.gtiff)
        InformationSource_dialog.setTabOrder(self.gtiff, self.shp)
        InformationSource_dialog.setTabOrder(self.shp, self.wfs)
        InformationSource_dialog.setTabOrder(self.wfs, self.dxf)
        InformationSource_dialog.setTabOrder(self.dxf, self.csv)
        InformationSource_dialog.setTabOrder(self.csv, self.stateBox)
        InformationSource_dialog.setTabOrder(self.stateBox, self.blind3)
        InformationSource_dialog.setTabOrder(self.blind3, self.blind1)
        InformationSource_dialog.setTabOrder(self.blind1, self.buttonBox)
        InformationSource_dialog.setTabOrder(self.buttonBox, self.blind4)
        InformationSource_dialog.setTabOrder(self.blind4, self.open_shapefile_btn)
        InformationSource_dialog.setTabOrder(self.open_shapefile_btn, self.open_geotiff_btn)
        InformationSource_dialog.setTabOrder(self.open_geotiff_btn, self.blind2)
        InformationSource_dialog.setTabOrder(self.blind2, self.open_csv_btn)
        InformationSource_dialog.setTabOrder(self.open_csv_btn, self.open_dxf_btn)

    def retranslateUi(self, InformationSource_dialog):
        InformationSource_dialog.setWindowTitle(_translate("InformationSource_dialog", "Dialog", None))
        self.open_csv_btn.setText(_translate("InformationSource_dialog", "...", None))
        self.label_4.setText(_translate("InformationSource_dialog", "Table", None))
        self.open_shapefile_btn.setText(_translate("InformationSource_dialog", "...", None))
        self.label_3.setText(_translate("InformationSource_dialog", "Vector", None))
        self.label.setText(_translate("InformationSource_dialog", "Extension Name:", None))
        self.label_5.setText(_translate("InformationSource_dialog", "WMS ( URL with Params )", None))
        self.gtiff.setToolTip(_translate("InformationSource_dialog", "Name of a GeoTiff file, including path", None))
        self.dxf.setToolTip(_translate("InformationSource_dialog", "Name of a DXF file, including path", None))
        self.label_13.setText(_translate("InformationSource_dialog", "Field ID:", None))
        self.label_12.setText(_translate("InformationSource_dialog", "Load information source", None))
        self.layer_name.setToolTip(_translate("InformationSource_dialog", "Layername, should be unique", None))
        self.label_11.setText(_translate("InformationSource_dialog", "Layer Name:", None))
        self.open_dxf_btn.setText(_translate("InformationSource_dialog", "...", None))
        self.label_6.setText(_translate("InformationSource_dialog", "GeoTiff", None))
        self.label_8.setText(_translate("InformationSource_dialog", "WFS", None))
        self.wms.setToolTip(_translate("InformationSource_dialog",
                                       "WMS - URL with parameters, a string like \'crs=EPSG:4326&dpiMode=7&format=image/png&layers=2&styles=&url=http:/<URL>\'",
                                       None))
        self.label_7.setText(_translate("InformationSource_dialog", "SHP", None))
        self.extension_dropdown.setToolTip(_translate("InformationSource_dialog",
                                                      "To add a new information source just select \'<Select information typer>\' and fill in the relevant fields ",
                                                      None))
        self.label_2.setText(_translate("InformationSource_dialog", "Raster", None))
        self.wfs.setToolTip(_translate("InformationSource_dialog", "WFS - URL ", None))
        self.label_9.setText(_translate("InformationSource_dialog", "DXF", None))
        self.shp.setToolTip(_translate("InformationSource_dialog", "Name of a Shapefile, including path", None))
        self.open_geotiff_btn.setText(_translate("InformationSource_dialog", "...", None))
        self.label_10.setText(_translate("InformationSource_dialog", "CSV", None))
        self.csv.setToolTip(_translate("InformationSource_dialog", "Name of a CSV file, including path", None))
        self.field_id.setToolTip(_translate("InformationSource_dialog",
                                            "Unique Field ID (used as attribute prefix in further evaluations) ", None))
        self.stateBox.setToolTip(_translate("InformationSource_dialog", "If set, the extension will be used", None))
        self.stateBox.setText(_translate("InformationSource_dialog", "Active", None))
        self.label_14.setText(_translate("InformationSource_dialog", "State", None))
