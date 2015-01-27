# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_process_dock.ui'
#
# Created: Tue Jan 27 14:39:44 2015
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

class Ui_MainProcess_dock(object):
    def setupUi(self, MainProcess_dock):
        MainProcess_dock.setObjectName(_fromUtf8("MainProcess_dock"))
        MainProcess_dock.resize(370, 460)
        MainProcess_dock.setMinimumSize(QtCore.QSize(370, 440))
        MainProcess_dock.setStyleSheet(_fromUtf8(""))
        self.dockWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.process_page = QtGui.QStackedWidget(self.dockWidgetContents)
        self.process_page.setEnabled(True)
        self.process_page.setGeometry(QtCore.QRect(10, 50, 350, 281))
        self.process_page.setAutoFillBackground(False)
        self.process_page.setStyleSheet(_fromUtf8("text-align: left;"))
        self.process_page.setFrameShape(QtGui.QFrame.StyledPanel)
        self.process_page.setFrameShadow(QtGui.QFrame.Plain)
        self.process_page.setLineWidth(2)
        self.process_page.setMidLineWidth(1)
        self.process_page.setObjectName(_fromUtf8("process_page"))
        self.project_basics_page = QtGui.QWidget()
        self.project_basics_page.setAccessibleDescription(_fromUtf8(""))
        self.project_basics_page.setObjectName(_fromUtf8("project_basics_page"))
        self.ol_plugin_installed_chckBox = QtGui.QPushButton(self.project_basics_page)
        self.ol_plugin_installed_chckBox.setEnabled(True)
        self.ol_plugin_installed_chckBox.setGeometry(QtCore.QRect(10, 0, 261, 41))
        self.ol_plugin_installed_chckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ol_plugin_installed_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icons/Icons/openmark.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icons/Icons/checkmark.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.ol_plugin_installed_chckBox.setIcon(icon)
        self.ol_plugin_installed_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.ol_plugin_installed_chckBox.setShortcut(_fromUtf8(""))
        self.ol_plugin_installed_chckBox.setCheckable(True)
        self.ol_plugin_installed_chckBox.setFlat(True)
        self.ol_plugin_installed_chckBox.setProperty("tristate", True)
        self.ol_plugin_installed_chckBox.setObjectName(_fromUtf8("ol_plugin_installed_chckBox"))
        self.project_created_chckBox = QtGui.QPushButton(self.project_basics_page)
        self.project_created_chckBox.setEnabled(True)
        self.project_created_chckBox.setGeometry(QtCore.QRect(10, 80, 261, 41))
        self.project_created_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.project_created_chckBox.setIcon(icon)
        self.project_created_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.project_created_chckBox.setShortcut(_fromUtf8(""))
        self.project_created_chckBox.setCheckable(True)
        self.project_created_chckBox.setFlat(True)
        self.project_created_chckBox.setObjectName(_fromUtf8("project_created_chckBox"))
        self.osm_layer_loaded_chckBox = QtGui.QPushButton(self.project_basics_page)
        self.osm_layer_loaded_chckBox.setEnabled(True)
        self.osm_layer_loaded_chckBox.setGeometry(QtCore.QRect(10, 120, 261, 41))
        self.osm_layer_loaded_chckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.osm_layer_loaded_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.osm_layer_loaded_chckBox.setIcon(icon)
        self.osm_layer_loaded_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.osm_layer_loaded_chckBox.setShortcut(_fromUtf8(""))
        self.osm_layer_loaded_chckBox.setCheckable(True)
        self.osm_layer_loaded_chckBox.setFlat(True)
        self.osm_layer_loaded_chckBox.setObjectName(_fromUtf8("osm_layer_loaded_chckBox"))
        self.pst_plugin_installed_chckBox = QtGui.QPushButton(self.project_basics_page)
        self.pst_plugin_installed_chckBox.setEnabled(True)
        self.pst_plugin_installed_chckBox.setGeometry(QtCore.QRect(10, 40, 261, 41))
        self.pst_plugin_installed_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.pst_plugin_installed_chckBox.setIcon(icon)
        self.pst_plugin_installed_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.pst_plugin_installed_chckBox.setShortcut(_fromUtf8(""))
        self.pst_plugin_installed_chckBox.setCheckable(True)
        self.pst_plugin_installed_chckBox.setFlat(True)
        self.pst_plugin_installed_chckBox.setObjectName(_fromUtf8("pst_plugin_installed_chckBox"))
        self.process_page.addWidget(self.project_basics_page)
        self.investigation_area_page = QtGui.QWidget()
        self.investigation_area_page.setAccessibleDescription(_fromUtf8(""))
        self.investigation_area_page.setObjectName(_fromUtf8("investigation_area_page"))
        self.temp_shapefile_created_chckBox = QtGui.QPushButton(self.investigation_area_page)
        self.temp_shapefile_created_chckBox.setEnabled(True)
        self.temp_shapefile_created_chckBox.setGeometry(QtCore.QRect(10, 0, 261, 41))
        self.temp_shapefile_created_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.temp_shapefile_created_chckBox.setIcon(icon)
        self.temp_shapefile_created_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.temp_shapefile_created_chckBox.setShortcut(_fromUtf8(""))
        self.temp_shapefile_created_chckBox.setCheckable(True)
        self.temp_shapefile_created_chckBox.setFlat(True)
        self.temp_shapefile_created_chckBox.setObjectName(_fromUtf8("temp_shapefile_created_chckBox"))
        self.editing_temp_shapefile_started_chckBox = QtGui.QPushButton(self.investigation_area_page)
        self.editing_temp_shapefile_started_chckBox.setEnabled(True)
        self.editing_temp_shapefile_started_chckBox.setGeometry(QtCore.QRect(10, 40, 261, 41))
        self.editing_temp_shapefile_started_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.editing_temp_shapefile_started_chckBox.setIcon(icon)
        self.editing_temp_shapefile_started_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.editing_temp_shapefile_started_chckBox.setShortcut(_fromUtf8(""))
        self.editing_temp_shapefile_started_chckBox.setCheckable(True)
        self.editing_temp_shapefile_started_chckBox.setFlat(True)
        self.editing_temp_shapefile_started_chckBox.setObjectName(_fromUtf8("editing_temp_shapefile_started_chckBox"))
        self.investigation_area_selected_chckBox = QtGui.QPushButton(self.investigation_area_page)
        self.investigation_area_selected_chckBox.setEnabled(True)
        self.investigation_area_selected_chckBox.setGeometry(QtCore.QRect(10, 80, 411, 41))
        self.investigation_area_selected_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.investigation_area_selected_chckBox.setIcon(icon)
        self.investigation_area_selected_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.investigation_area_selected_chckBox.setShortcut(_fromUtf8(""))
        self.investigation_area_selected_chckBox.setCheckable(True)
        self.investigation_area_selected_chckBox.setFlat(True)
        self.investigation_area_selected_chckBox.setObjectName(_fromUtf8("investigation_area_selected_chckBox"))
        self.editing_temp_shapefile_stopped_chckBox = QtGui.QPushButton(self.investigation_area_page)
        self.editing_temp_shapefile_stopped_chckBox.setEnabled(True)
        self.editing_temp_shapefile_stopped_chckBox.setGeometry(QtCore.QRect(10, 120, 261, 41))
        self.editing_temp_shapefile_stopped_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.editing_temp_shapefile_stopped_chckBox.setIcon(icon)
        self.editing_temp_shapefile_stopped_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.editing_temp_shapefile_stopped_chckBox.setShortcut(_fromUtf8(""))
        self.editing_temp_shapefile_stopped_chckBox.setCheckable(True)
        self.editing_temp_shapefile_stopped_chckBox.setFlat(True)
        self.editing_temp_shapefile_stopped_chckBox.setObjectName(_fromUtf8("editing_temp_shapefile_stopped_chckBox"))
        self.process_page.addWidget(self.investigation_area_page)
        self.building_shapes_page = QtGui.QWidget()
        self.building_shapes_page.setAccessibleDescription(_fromUtf8(""))
        self.building_shapes_page.setObjectName(_fromUtf8("building_shapes_page"))
        self.raster_loaded_chckBox = QtGui.QPushButton(self.building_shapes_page)
        self.raster_loaded_chckBox.setEnabled(True)
        self.raster_loaded_chckBox.setGeometry(QtCore.QRect(10, 0, 261, 41))
        self.raster_loaded_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px;}\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.raster_loaded_chckBox.setIcon(icon)
        self.raster_loaded_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.raster_loaded_chckBox.setCheckable(True)
        self.raster_loaded_chckBox.setFlat(True)
        self.raster_loaded_chckBox.setObjectName(_fromUtf8("raster_loaded_chckBox"))
        self.extent_clipped_chckBox = QtGui.QPushButton(self.building_shapes_page)
        self.extent_clipped_chckBox.setEnabled(True)
        self.extent_clipped_chckBox.setGeometry(QtCore.QRect(10, 40, 321, 41))
        self.extent_clipped_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px;}\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.extent_clipped_chckBox.setIcon(icon)
        self.extent_clipped_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.extent_clipped_chckBox.setCheckable(True)
        self.extent_clipped_chckBox.setFlat(True)
        self.extent_clipped_chckBox.setObjectName(_fromUtf8("extent_clipped_chckBox"))
        self.pyramids_built_chckBox = QtGui.QPushButton(self.building_shapes_page)
        self.pyramids_built_chckBox.setEnabled(True)
        self.pyramids_built_chckBox.setGeometry(QtCore.QRect(10, 80, 321, 41))
        self.pyramids_built_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px;}\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.pyramids_built_chckBox.setIcon(icon)
        self.pyramids_built_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.pyramids_built_chckBox.setShortcut(_fromUtf8(""))
        self.pyramids_built_chckBox.setCheckable(True)
        self.pyramids_built_chckBox.setFlat(True)
        self.pyramids_built_chckBox.setObjectName(_fromUtf8("pyramids_built_chckBox"))
        self.process_page.addWidget(self.building_shapes_page)
        self.sampling_points_page = QtGui.QWidget()
        self.sampling_points_page.setAccessibleDescription(_fromUtf8(""))
        self.sampling_points_page.setObjectName(_fromUtf8("sampling_points_page"))
        self.temp_pointlayer_created_chckBox = QtGui.QPushButton(self.sampling_points_page)
        self.temp_pointlayer_created_chckBox.setEnabled(True)
        self.temp_pointlayer_created_chckBox.setGeometry(QtCore.QRect(10, 0, 176, 41))
        self.temp_pointlayer_created_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.temp_pointlayer_created_chckBox.setIcon(icon)
        self.temp_pointlayer_created_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.temp_pointlayer_created_chckBox.setShortcut(_fromUtf8(""))
        self.temp_pointlayer_created_chckBox.setCheckable(True)
        self.temp_pointlayer_created_chckBox.setFlat(True)
        self.temp_pointlayer_created_chckBox.setObjectName(_fromUtf8("temp_pointlayer_created_chckBox"))
        self.editing_temp_pointlayer_started_chckBox = QtGui.QPushButton(self.sampling_points_page)
        self.editing_temp_pointlayer_started_chckBox.setEnabled(True)
        self.editing_temp_pointlayer_started_chckBox.setGeometry(QtCore.QRect(10, 40, 171, 41))
        self.editing_temp_pointlayer_started_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.editing_temp_pointlayer_started_chckBox.setIcon(icon)
        self.editing_temp_pointlayer_started_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.editing_temp_pointlayer_started_chckBox.setShortcut(_fromUtf8(""))
        self.editing_temp_pointlayer_started_chckBox.setCheckable(True)
        self.editing_temp_pointlayer_started_chckBox.setFlat(True)
        self.editing_temp_pointlayer_started_chckBox.setObjectName(_fromUtf8("editing_temp_pointlayer_started_chckBox"))
        self.points_of_interest_defined_chckBox = QtGui.QPushButton(self.sampling_points_page)
        self.points_of_interest_defined_chckBox.setEnabled(True)
        self.points_of_interest_defined_chckBox.setGeometry(QtCore.QRect(10, 80, 276, 41))
        self.points_of_interest_defined_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.points_of_interest_defined_chckBox.setIcon(icon)
        self.points_of_interest_defined_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.points_of_interest_defined_chckBox.setShortcut(_fromUtf8(""))
        self.points_of_interest_defined_chckBox.setCheckable(True)
        self.points_of_interest_defined_chckBox.setFlat(True)
        self.points_of_interest_defined_chckBox.setObjectName(_fromUtf8("points_of_interest_defined_chckBox"))
        self.editing_temp_pointlayer_stopped_chckBox = QtGui.QPushButton(self.sampling_points_page)
        self.editing_temp_pointlayer_stopped_chckBox.setEnabled(True)
        self.editing_temp_pointlayer_stopped_chckBox.setGeometry(QtCore.QRect(10, 120, 246, 41))
        self.editing_temp_pointlayer_stopped_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.editing_temp_pointlayer_stopped_chckBox.setIcon(icon)
        self.editing_temp_pointlayer_stopped_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.editing_temp_pointlayer_stopped_chckBox.setShortcut(_fromUtf8(""))
        self.editing_temp_pointlayer_stopped_chckBox.setCheckable(True)
        self.editing_temp_pointlayer_stopped_chckBox.setFlat(True)
        self.editing_temp_pointlayer_stopped_chckBox.setObjectName(_fromUtf8("editing_temp_pointlayer_stopped_chckBox"))
        self.information_sampled_chckBox = QtGui.QPushButton(self.sampling_points_page)
        self.information_sampled_chckBox.setEnabled(True)
        self.information_sampled_chckBox.setGeometry(QtCore.QRect(10, 160, 381, 41))
        self.information_sampled_chckBox.setStyleSheet(_fromUtf8(":active{ text-align: left; border: none; margin-left: 3px; }\n"
":checked { border: none; }\n"
":pressed { border: none; }\n"
""))
        self.information_sampled_chckBox.setIcon(icon)
        self.information_sampled_chckBox.setIconSize(QtCore.QSize(17, 17))
        self.information_sampled_chckBox.setShortcut(_fromUtf8(""))
        self.information_sampled_chckBox.setCheckable(True)
        self.information_sampled_chckBox.setFlat(True)
        self.information_sampled_chckBox.setObjectName(_fromUtf8("information_sampled_chckBox"))
        self.process_page.addWidget(self.sampling_points_page)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setGeometry(QtCore.QRect(11, 17, 121, 26))
        self.label.setObjectName(_fromUtf8("label"))
        self.active_page_dropdown = QtGui.QComboBox(self.dockWidgetContents)
        self.active_page_dropdown.setGeometry(QtCore.QRect(143, 20, 221, 26))
        self.active_page_dropdown.setObjectName(_fromUtf8("active_page_dropdown"))
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(5, 340, 114, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.process_button_prev = QtGui.QPushButton(self.dockWidgetContents)
        self.process_button_prev.setGeometry(QtCore.QRect(160, 340, 100, 32))
        self.process_button_prev.setObjectName(_fromUtf8("process_button_prev"))
        self.process_button_next = QtGui.QPushButton(self.dockWidgetContents)
        self.process_button_next.setGeometry(QtCore.QRect(266, 340, 100, 32))
        self.process_button_next.setObjectName(_fromUtf8("process_button_next"))
        MainProcess_dock.setWidget(self.dockWidgetContents)

        self.retranslateUi(MainProcess_dock)
        self.process_page.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainProcess_dock)

    def retranslateUi(self, MainProcess_dock):
        MainProcess_dock.setWindowTitle(_translate("MainProcess_dock", "Open eQuarter - Analysis", None))
        self.project_basics_page.setAccessibleName(_translate("MainProcess_dock", "Project Basics", None))
        self.ol_plugin_installed_chckBox.setText(_translate("MainProcess_dock", "Install the Open Street Map Plugin", None))
        self.project_created_chckBox.setText(_translate("MainProcess_dock", "Create a new project and save it.", None))
        self.osm_layer_loaded_chckBox.setText(_translate("MainProcess_dock", "Open an Open Layers Map", None))
        self.pst_plugin_installed_chckBox.setText(_translate("MainProcess_dock", "Install the PointSamplingTool Plugin", None))
        self.investigation_area_page.setAccessibleName(_translate("MainProcess_dock", "Investigation Area", None))
        self.temp_shapefile_created_chckBox.setText(_translate("MainProcess_dock", "Create a new Polygon-Shapelayer", None))
        self.editing_temp_shapefile_started_chckBox.setText(_translate("MainProcess_dock", "Activate the edit mode", None))
        self.investigation_area_selected_chckBox.setText(_translate("MainProcess_dock", "Add new features to cover your\n"
"investigation area with", None))
        self.editing_temp_shapefile_stopped_chckBox.setText(_translate("MainProcess_dock", "Deactivate the edit mode", None))
        self.building_shapes_page.setAccessibleName(_translate("MainProcess_dock", "Building Shapes", None))
        self.raster_loaded_chckBox.setText(_translate("MainProcess_dock", "Load a new (wms) raster-map", None))
        self.extent_clipped_chckBox.setText(_translate("MainProcess_dock", "Export the investigation areas extent as .tif", None))
        self.pyramids_built_chckBox.setText(_translate("MainProcess_dock", "Open the created .tif-file and build pyramids", None))
        self.sampling_points_page.setAccessibleName(_translate("MainProcess_dock", "Point Sampling", None))
        self.temp_pointlayer_created_chckBox.setText(_translate("MainProcess_dock", "Create a new Pointlayer", None))
        self.editing_temp_pointlayer_started_chckBox.setText(_translate("MainProcess_dock", "Activate the edit mode", None))
        self.points_of_interest_defined_chckBox.setText(_translate("MainProcess_dock", "Add new features to mark the buildings \n"
"you want to extract information from", None))
        self.editing_temp_pointlayer_stopped_chckBox.setText(_translate("MainProcess_dock", "Deactivate the edit mode", None))
        self.information_sampled_chckBox.setText(_translate("MainProcess_dock", "Use the point-sampling-tool to extract\n"
"the information", None))
        self.label.setText(_translate("MainProcess_dock", "Currently viewing:", None))
        self.pushButton.setText(_translate("MainProcess_dock", "Cancel", None))
        self.process_button_prev.setText(_translate("MainProcess_dock", "< Previous", None))
        self.process_button_next.setText(_translate("MainProcess_dock", "Next >", None))

import resources_rc
