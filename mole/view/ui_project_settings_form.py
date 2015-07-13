# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_project_settings_form.ui'
#
# Created: Mon Jul 13 12:51:16 2015
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

class Ui_project_settings_form(object):
    def setupUi(self, project_settings_form):
        project_settings_form.setObjectName(_fromUtf8("project_settings_form"))
        project_settings_form.resize(409, 516)
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
        self.gridLayout.setVerticalSpacing(6)
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
        self.heating_degree_days = QtGui.QLineEdit(self.form)
        self.heating_degree_days.setObjectName(_fromUtf8("heating_degree_days"))
        self.gridLayout.addWidget(self.heating_degree_days, 9, 0, 1, 1)
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
        self.location_city.setMinimumSize(QtCore.QSize(228, 0))
        self.location_city.setObjectName(_fromUtf8("location_city"))
        self.location_layout.addWidget(self.location_city)
        self.location_postal = QtGui.QLineEdit(self.form)
        self.location_postal.setMaximumSize(QtCore.QSize(100, 16777215))
        self.location_postal.setObjectName(_fromUtf8("location_postal"))
        self.location_layout.addWidget(self.location_postal)
        self.lookup_by_address = QtGui.QPushButton(self.form)
        self.lookup_by_address.setMinimumSize(QtCore.QSize(32, 32))
        self.lookup_by_address.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/magnifying_glass.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lookup_by_address.setIcon(icon)
        self.lookup_by_address.setFlat(True)
        self.lookup_by_address.setObjectName(_fromUtf8("lookup_by_address"))
        self.location_layout.addWidget(self.lookup_by_address)
        self.gridLayout.addLayout(self.location_layout, 5, 0, 1, 1)
        self.climate_zone_layout = QtGui.QHBoxLayout()
        self.climate_zone_layout.setSpacing(0)
        self.climate_zone_layout.setObjectName(_fromUtf8("climate_zone_layout"))
        self.heating_degree_days_label = QtGui.QLabel(self.form)
        self.heating_degree_days_label.setToolTip(_fromUtf8(""))
        self.heating_degree_days_label.setObjectName(_fromUtf8("heating_degree_days_label"))
        self.climate_zone_layout.addWidget(self.heating_degree_days_label)
        self.gridLayout.addLayout(self.climate_zone_layout, 8, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.location_lon = QtGui.QLineEdit(self.form)
        self.location_lon.setObjectName(_fromUtf8("location_lon"))
        self.horizontalLayout.addWidget(self.location_lon)
        self.location_lat = QtGui.QLineEdit(self.form)
        self.location_lat.setObjectName(_fromUtf8("location_lat"))
        self.horizontalLayout.addWidget(self.location_lat)
        self.location_crs = QtGui.QLineEdit(self.form)
        self.location_crs.setObjectName(_fromUtf8("location_crs"))
        self.horizontalLayout.addWidget(self.location_crs)
        self.lookup_by_coords = QtGui.QPushButton(self.form)
        self.lookup_by_coords.setMinimumSize(QtCore.QSize(32, 32))
        self.lookup_by_coords.setText(_fromUtf8(""))
        self.lookup_by_coords.setIcon(icon)
        self.lookup_by_coords.setFlat(True)
        self.lookup_by_coords.setObjectName(_fromUtf8("lookup_by_coords"))
        self.horizontalLayout.addWidget(self.lookup_by_coords)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 1)
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
        self.heating_degree_days.setText(_translate("project_settings_form", "390.06", None))
        self.average_build_year_label.setToolTip(_translate("project_settings_form", "Average year of construction on the building stock", None))
        self.average_build_year_label.setText(_translate("project_settings_form", "Average Build Year", None))
        self.average_build_year.setText(_translate("project_settings_form", "1917", None))
        self.population_density_label.setToolTip(_translate("project_settings_form", "Population density of the investigation area (inhabitants per square kilometre)", None))
        self.population_density_label.setText(_translate("project_settings_form", "Population Density:", None))
        self.population_density.setText(_translate("project_settings_form", "3.859", None))
        self.location_city.setText(_translate("project_settings_form", "City or street", None))
        self.location_postal.setText(_translate("project_settings_form", "Postal", None))
        self.lookup_by_address.setToolTip(_translate("project_settings_form", "Lookup address", None))
        self.heating_degree_days_label.setText(_translate("project_settings_form", "Heating degree days:", None))
        self.location_lon.setText(_translate("project_settings_form", "Lon", None))
        self.location_lat.setText(_translate("project_settings_form", "Lat", None))
        self.location_crs.setText(_translate("project_settings_form", "CRS", None))
        self.lookup_by_coords.setToolTip(_translate("project_settings_form", "Lookup coordinates", None))

import resources_rc
