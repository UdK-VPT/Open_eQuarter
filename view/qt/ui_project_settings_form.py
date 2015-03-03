# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/qt/ui_project_settings_form.ui'
#
# Created: Tue Mar  3 11:14:16 2015
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

class Ui_project_settings_form(object):
    def setupUi(self, project_settings_form):
        project_settings_form.setObjectName(_fromUtf8("project_settings_form"))
        project_settings_form.resize(374, 409)
        project_settings_form.setStyleSheet(_fromUtf8("#form QLineEdit {\n"
"    color: rgb(151, 151, 151,95);\n"
"}\n"
"\n"
"#form QLineEdit:focus {\n"
"    color: rgb(0,0,0);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(project_settings_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.form = QtGui.QFrame(project_settings_form)
        self.form.setStyleSheet(_fromUtf8(""))
        self.form.setFrameShape(QtGui.QFrame.StyledPanel)
        self.form.setFrameShadow(QtGui.QFrame.Raised)
        self.form.setObjectName(_fromUtf8("form"))
        self.gridLayout = QtGui.QGridLayout(self.form)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.project_name = QtGui.QLineEdit(self.form)
        self.project_name.setObjectName(_fromUtf8("project_name"))
        self.gridLayout.addWidget(self.project_name, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.description = QtGui.QLineEdit(self.form)
        self.description.setObjectName(_fromUtf8("description"))
        self.gridLayout.addWidget(self.description, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.climate_zone = QtGui.QLineEdit(self.form)
        self.climate_zone.setObjectName(_fromUtf8("climate_zone"))
        self.gridLayout.addWidget(self.climate_zone, 5, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.average_build_year = QtGui.QLineEdit(self.form)
        self.average_build_year.setObjectName(_fromUtf8("average_build_year"))
        self.gridLayout.addWidget(self.average_build_year, 7, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
        self.population_density = QtGui.QLineEdit(self.form)
        self.population_density.setObjectName(_fromUtf8("population_density"))
        self.gridLayout.addWidget(self.population_density, 9, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.form)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 1)
        self.verticalLayout.addWidget(self.form)

        self.retranslateUi(project_settings_form)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), project_settings_form.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), project_settings_form.reject)
        QtCore.QMetaObject.connectSlotsByName(project_settings_form)

    def retranslateUi(self, project_settings_form):
        project_settings_form.setWindowTitle(_translate("project_settings_form", "Dialog", None))
        self.label.setToolTip(_translate("project_settings_form", "Name of the project", None))
        self.label.setText(_translate("project_settings_form", "Project Name:", None))
        self.project_name.setToolTip(_translate("project_settings_form", "Name of the project", None))
        self.project_name.setText(_translate("project_settings_form", "MyProject", None))
        self.label_2.setToolTip(_translate("project_settings_form", "Short description of the project", None))
        self.label_2.setText(_translate("project_settings_form", "Description:", None))
        self.description.setText(_translate("project_settings_form", "The aim of this project, is to analyse a quarter.", None))
        self.label_3.setToolTip(_translate("project_settings_form", "Köppen–Geiger climate classification of the investigation area (for more informatoin visit: http://en.wikipedia.org/wiki/Köppen_climate_classification)", None))
        self.label_3.setText(_translate("project_settings_form", "Climate Zone:", None))
        self.climate_zone.setText(_translate("project_settings_form", "e.g. Dfb, Cfb, Dfc", None))
        self.label_4.setToolTip(_translate("project_settings_form", "Average year of construction on the building stock", None))
        self.label_4.setText(_translate("project_settings_form", "Average Build Year", None))
        self.average_build_year.setText(_translate("project_settings_form", "1917", None))
        self.label_5.setToolTip(_translate("project_settings_form", "Population density of the investigation area (inhabitants per square kilometre)", None))
        self.label_5.setText(_translate("project_settings_form", "Population Density:", None))
        self.population_density.setText(_translate("project_settings_form", "3.859", None))

