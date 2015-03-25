# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_project_settings_form.ui'
#
# Created: Wed Mar 25 15:53:09 2015
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
        project_settings_form.resize(374, 516)
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
        self.location_label = QtGui.QLabel(self.form)
        self.location_label.setObjectName(_fromUtf8("location_label"))
        self.gridLayout.addWidget(self.location_label, 4, 0, 1, 1)
        self.project_name_label = QtGui.QLabel(self.form)
        self.project_name_label.setObjectName(_fromUtf8("project_name_label"))
        self.gridLayout.addWidget(self.project_name_label, 0, 0, 1, 1)
        self.project_name = QtGui.QLineEdit(self.form)
        self.project_name.setObjectName(_fromUtf8("project_name"))
        self.gridLayout.addWidget(self.project_name, 1, 0, 1, 1)
        self.description_label = QtGui.QLabel(self.form)
        self.description_label.setObjectName(_fromUtf8("description_label"))
        self.gridLayout.addWidget(self.description_label, 2, 0, 1, 1)
        self.description = QtGui.QLineEdit(self.form)
        self.description.setObjectName(_fromUtf8("description"))
        self.gridLayout.addWidget(self.description, 3, 0, 1, 1)
        self.climate_zone = QtGui.QLineEdit(self.form)
        self.climate_zone.setObjectName(_fromUtf8("climate_zone"))
        self.gridLayout.addWidget(self.climate_zone, 9, 0, 1, 1)
        self.average_build_year_label = QtGui.QLabel(self.form)
        self.average_build_year_label.setObjectName(_fromUtf8("average_build_year_label"))
        self.gridLayout.addWidget(self.average_build_year_label, 10, 0, 1, 1)
        self.average_build_year = QtGui.QLineEdit(self.form)
        self.average_build_year.setObjectName(_fromUtf8("average_build_year"))
        self.gridLayout.addWidget(self.average_build_year, 11, 0, 1, 1)
        self.population_density_label = QtGui.QLabel(self.form)
        self.population_density_label.setObjectName(_fromUtf8("population_density_label"))
        self.gridLayout.addWidget(self.population_density_label, 12, 0, 1, 1)
        self.population_density = QtGui.QLineEdit(self.form)
        self.population_density.setObjectName(_fromUtf8("population_density"))
        self.gridLayout.addWidget(self.population_density, 13, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.form)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 14, 0, 1, 1)
        self.location_layout = QtGui.QHBoxLayout()
        self.location_layout.setObjectName(_fromUtf8("location_layout"))
        self.location_city = QtGui.QLineEdit(self.form)
        self.location_city.setMinimumSize(QtCore.QSize(0, 0))
        self.location_city.setObjectName(_fromUtf8("location_city"))
        self.location_layout.addWidget(self.location_city)
        self.location_postal = QtGui.QLineEdit(self.form)
        self.location_postal.setMaximumSize(QtCore.QSize(100, 16777215))
        self.location_postal.setObjectName(_fromUtf8("location_postal"))
        self.location_layout.addWidget(self.location_postal)
        self.gridLayout.addLayout(self.location_layout, 5, 0, 1, 1)
        self.climate_zone_layout = QtGui.QHBoxLayout()
        self.climate_zone_layout.setSpacing(0)
        self.climate_zone_layout.setObjectName(_fromUtf8("climate_zone_layout"))
        self.climate_zone_label = QtGui.QLabel(self.form)
        self.climate_zone_label.setToolTip(_fromUtf8(""))
        self.climate_zone_label.setObjectName(_fromUtf8("climate_zone_label"))
        self.climate_zone_layout.addWidget(self.climate_zone_label)
        self.pushButton = QtGui.QPushButton(self.form)
        self.pushButton.setMaximumSize(QtCore.QSize(18, 16777215))
        self.pushButton.setStyleSheet(_fromUtf8(""))
        self.pushButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/info.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.climate_zone_layout.addWidget(self.pushButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.climate_zone_layout.addItem(spacerItem)
        self.gridLayout.addLayout(self.climate_zone_layout, 8, 0, 1, 1)
        self.verticalLayout.addWidget(self.form)

        self.retranslateUi(project_settings_form)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), project_settings_form.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), project_settings_form.reject)
        QtCore.QMetaObject.connectSlotsByName(project_settings_form)

    def retranslateUi(self, project_settings_form):
        project_settings_form.setWindowTitle(_translate("project_settings_form", "Dialog", None))
        self.location_label.setText(_translate("project_settings_form", "Location:", None))
        self.project_name_label.setToolTip(_translate("project_settings_form", "Name of the project", None))
        self.project_name_label.setText(_translate("project_settings_form", "Project Name:", None))
        self.project_name.setToolTip(_translate("project_settings_form", "Name of the project", None))
        self.project_name.setText(_translate("project_settings_form", "MyProject", None))
        self.description_label.setToolTip(_translate("project_settings_form", "Short description of the project", None))
        self.description_label.setText(_translate("project_settings_form", "Description:", None))
        self.description.setText(_translate("project_settings_form", "The aim of this project, is to analyse a quarter.", None))
        self.climate_zone.setText(_translate("project_settings_form", "e.g. Dfb, Cfb, Dfc", None))
        self.average_build_year_label.setToolTip(_translate("project_settings_form", "Average year of construction on the building stock", None))
        self.average_build_year_label.setText(_translate("project_settings_form", "Average Build Year", None))
        self.average_build_year.setText(_translate("project_settings_form", "1917", None))
        self.population_density_label.setToolTip(_translate("project_settings_form", "Population density of the investigation area (inhabitants per square kilometre)", None))
        self.population_density_label.setText(_translate("project_settings_form", "Population Density:", None))
        self.population_density.setText(_translate("project_settings_form", "3.859", None))
        self.location_city.setText(_translate("project_settings_form", "City", None))
        self.location_postal.setText(_translate("project_settings_form", "Postal", None))
        self.climate_zone_label.setText(_translate("project_settings_form", "Climate Zone:", None))
        self.pushButton.setToolTip(_translate("project_settings_form", "Köppen–Geiger climate classification of the investigation area (for more informatoin visit: http://en.wikipedia.org/wiki/Köppen_climate_classification)", None))

import resources_rc
