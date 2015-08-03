# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_information_source_dialog.ui'
#
# Created: Mon Aug  3 17:16:50 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(457, 421)
        Dialog.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridWidget = QtGui.QWidget(Dialog)
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
""))
        self.gridWidget.setObjectName(_fromUtf8("gridWidget"))
        self.grid = QtGui.QGridLayout(self.gridWidget)
        self.grid.setMargin(0)
        self.grid.setVerticalSpacing(0)
        self.grid.setObjectName(_fromUtf8("grid"))
        self.open_dxf_btn = QtGui.QPushButton(self.gridWidget)
        self.open_dxf_btn.setMaximumSize(QtCore.QSize(21, 21))
        self.open_dxf_btn.setObjectName(_fromUtf8("open_dxf_btn"))
        self.grid.addWidget(self.open_dxf_btn, 9, 2, 1, 1)
        self.dxf = QtGui.QLineEdit(self.gridWidget)
        self.dxf.setObjectName(_fromUtf8("dxf"))
        self.grid.addWidget(self.dxf, 9, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.grid.addWidget(self.label_7, 7, 0, 1, 1)
        self.wms = QtGui.QLineEdit(self.gridWidget)
        self.wms.setObjectName(_fromUtf8("wms"))
        self.grid.addWidget(self.wms, 4, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.grid.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.gridWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.grid.addWidget(self.label_8, 8, 0, 1, 1)
        self.open_geotiff_btn = QtGui.QPushButton(self.gridWidget)
        self.open_geotiff_btn.setMaximumSize(QtCore.QSize(21, 21))
        self.open_geotiff_btn.setObjectName(_fromUtf8("open_geotiff_btn"))
        self.grid.addWidget(self.open_geotiff_btn, 5, 2, 1, 1)
        self.open_shapefile_btn = QtGui.QPushButton(self.gridWidget)
        self.open_shapefile_btn.setMaximumSize(QtCore.QSize(21, 21))
        self.open_shapefile_btn.setObjectName(_fromUtf8("open_shapefile_btn"))
        self.grid.addWidget(self.open_shapefile_btn, 7, 2, 1, 1)
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
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.grid.addWidget(self.label_2, 3, 0, 1, 3)
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
        self.grid.addWidget(self.label_4, 10, 0, 1, 3)
        self.open_csv_btn = QtGui.QPushButton(self.gridWidget)
        self.open_csv_btn.setMaximumSize(QtCore.QSize(21, 21))
        self.open_csv_btn.setObjectName(_fromUtf8("open_csv_btn"))
        self.grid.addWidget(self.open_csv_btn, 11, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.grid.addWidget(self.label_9, 9, 0, 1, 1)
        self.wfs = QtGui.QLineEdit(self.gridWidget)
        self.wfs.setObjectName(_fromUtf8("wfs"))
        self.grid.addWidget(self.wfs, 8, 1, 1, 1)
        self.shapefile = QtGui.QLineEdit(self.gridWidget)
        self.shapefile.setObjectName(_fromUtf8("shapefile"))
        self.grid.addWidget(self.shapefile, 7, 1, 1, 1)
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
        self.grid.addWidget(self.label_3, 6, 0, 1, 3)
        self.label = QtGui.QLabel(self.gridWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label.setObjectName(_fromUtf8("label"))
        self.grid.addWidget(self.label, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.grid.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.gridWidget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.grid.addWidget(self.label_11, 2, 0, 1, 1)
        self.geotiff = QtGui.QLineEdit(self.gridWidget)
        self.geotiff.setObjectName(_fromUtf8("geotiff"))
        self.grid.addWidget(self.geotiff, 5, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.gridWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.grid.addWidget(self.label_10, 11, 0, 1, 1)
        self.csv = QtGui.QLineEdit(self.gridWidget)
        self.csv.setObjectName(_fromUtf8("csv"))
        self.grid.addWidget(self.csv, 11, 1, 1, 1)
        self.extension_dropdown = QtGui.QComboBox(self.gridWidget)
        self.extension_dropdown.setMaximumSize(QtCore.QSize(16777215, 26))
        self.extension_dropdown.setObjectName(_fromUtf8("extension_dropdown"))
        self.grid.addWidget(self.extension_dropdown, 1, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.gridWidget)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.grid.addWidget(self.label_12, 0, 0, 1, 3)
        self.layer_name = QtGui.QLineEdit(self.gridWidget)
        self.layer_name.setObjectName(_fromUtf8("layer_name"))
        self.grid.addWidget(self.layer_name, 2, 1, 1, 1)
        self.blind2 = QtGui.QPushButton(self.gridWidget)
        self.blind2.setMaximumSize(QtCore.QSize(21, 21))
        self.blind2.setText(_fromUtf8(""))
        self.blind2.setFlat(False)
        self.blind2.setObjectName(_fromUtf8("blind2"))
        self.grid.addWidget(self.blind2, 4, 2, 1, 1)
        self.blind1 = QtGui.QPushButton(self.gridWidget)
        self.blind1.setMaximumSize(QtCore.QSize(21, 21))
        self.blind1.setText(_fromUtf8(""))
        self.blind1.setCheckable(False)
        self.blind1.setAutoDefault(True)
        self.blind1.setFlat(False)
        self.blind1.setObjectName(_fromUtf8("blind1"))
        self.grid.addWidget(self.blind1, 2, 2, 1, 1)
        self.blind3 = QtGui.QPushButton(self.gridWidget)
        self.blind3.setMaximumSize(QtCore.QSize(21, 21))
        self.blind3.setText(_fromUtf8(""))
        self.blind3.setFlat(False)
        self.blind3.setObjectName(_fromUtf8("blind3"))
        self.grid.addWidget(self.blind3, 8, 2, 1, 1)
        self.verticalLayout.addWidget(self.gridWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.open_dxf_btn.setText(_translate("Dialog", "...", None))
        self.label_7.setText(_translate("Dialog", "SHP", None))
        self.label_6.setText(_translate("Dialog", "GeoTiff", None))
        self.label_8.setText(_translate("Dialog", "WFS", None))
        self.open_geotiff_btn.setText(_translate("Dialog", "...", None))
        self.open_shapefile_btn.setText(_translate("Dialog", "...", None))
        self.label_2.setText(_translate("Dialog", "Raster", None))
        self.label_4.setText(_translate("Dialog", "Table", None))
        self.open_csv_btn.setText(_translate("Dialog", "...", None))
        self.label_9.setText(_translate("Dialog", "DXF", None))
        self.label_3.setText(_translate("Dialog", "Vector", None))
        self.label.setText(_translate("Dialog", "Information type:", None))
        self.label_5.setText(_translate("Dialog", "WMS", None))
        self.label_11.setText(_translate("Dialog", "Layer name:", None))
        self.label_10.setText(_translate("Dialog", "CSV", None))
        self.label_12.setText(_translate("Dialog", "Load information source", None))

