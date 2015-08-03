# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/ui_main_process_dock.ui'
#
# Created: Mon Aug  3 17:56:39 2015
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

class Ui_MainProcess_dock(object):
    def setupUi(self, MainProcess_dock):
        MainProcess_dock.setObjectName(_fromUtf8("MainProcess_dock"))
        MainProcess_dock.resize(374, 516)
        MainProcess_dock.setMinimumSize(QtCore.QSize(374, 500))
        MainProcess_dock.setStyleSheet(_fromUtf8("QStackedWidget QWidget { \n"
"    text-align: left; \n"
"}\n"
"\n"
"QStackedWidget QAbstractButton {\n"
"    border: none;\n"
"    margin-left: 2px;\n"
"    min-width: 261px;\n"
"    max-width: 320px;\n"
"    min-height: 32px;\n"
"    max-height: 40px;\n"
"    qproperty-icon: url(\":/Controls/icons/openmark.png\") off,\n"
"                            url(\":/Controls/icons/checkmark.png\") on ;\n"
"    qproperty-iconSize: 17px; \n"
"    qproperty-flat: true;\n"
"    qproperty-checkable: true;\n"
"}\n"
"\n"
"QStackedWidget QAbstractButton:active {\n"
"    border: none;\n"
"}\n"
"\n"
"QListView {\n"
"    text-align: left;\n"
"    background-color: #f0f0f0;\n"
"}\n"
"#menu_bar {\n"
"    padding: -10px;\n"
"}\n"
"\n"
"\n"
"\n"
""))
        self.dockWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.menu_bar = QtGui.QWidget(self.dockWidgetContents)
        self.menu_bar.setMinimumSize(QtCore.QSize(60, 0))
        self.menu_bar.setObjectName(_fromUtf8("menu_bar"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.menu_bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.settings_dropdown_btn = QtGui.QToolButton(self.menu_bar)
        self.settings_dropdown_btn.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/gearwheel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_dropdown_btn.setIcon(icon)
        self.settings_dropdown_btn.setIconSize(QtCore.QSize(17, 17))
        self.settings_dropdown_btn.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.settings_dropdown_btn.setObjectName(_fromUtf8("settings_dropdown_btn"))
        self.horizontalLayout.addWidget(self.settings_dropdown_btn)
        self.tools_dropdown_btn = QtGui.QToolButton(self.menu_bar)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/tools.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tools_dropdown_btn.setIcon(icon1)
        self.tools_dropdown_btn.setIconSize(QtCore.QSize(17, 17))
        self.tools_dropdown_btn.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.tools_dropdown_btn.setObjectName(_fromUtf8("tools_dropdown_btn"))
        self.horizontalLayout.addWidget(self.tools_dropdown_btn)
        self.horizontalLayout_3.addWidget(self.menu_bar, QtCore.Qt.AlignLeft)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.active_page_dropdown = QtGui.QComboBox(self.dockWidgetContents)
        self.active_page_dropdown.setObjectName(_fromUtf8("active_page_dropdown"))
        self.horizontalLayout_3.addWidget(self.active_page_dropdown)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.process_page = QtGui.QStackedWidget(self.dockWidgetContents)
        self.process_page.setEnabled(True)
        self.process_page.setMinimumSize(QtCore.QSize(350, 280))
        self.process_page.setMaximumSize(QtCore.QSize(16777215, 280))
        self.process_page.setAutoFillBackground(False)
        self.process_page.setStyleSheet(_fromUtf8(""))
        self.process_page.setFrameShape(QtGui.QFrame.StyledPanel)
        self.process_page.setFrameShadow(QtGui.QFrame.Plain)
        self.process_page.setLineWidth(2)
        self.process_page.setMidLineWidth(1)
        self.process_page.setObjectName(_fromUtf8("process_page"))
        self.project_basics_page = QtGui.QWidget()
        self.project_basics_page.setAccessibleDescription(_fromUtf8(""))
        self.project_basics_page.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.project_basics_page.setStyleSheet(_fromUtf8(""))
        self.project_basics_page.setObjectName(_fromUtf8("project_basics_page"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.project_basics_page)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.ol_plugin_installed_chckBox = QProcessButton(self.project_basics_page)
        self.ol_plugin_installed_chckBox.setObjectName(_fromUtf8("ol_plugin_installed_chckBox"))
        self.verticalLayout_2.addWidget(self.ol_plugin_installed_chckBox)
        self.pst_plugin_installed_chckBox = QProcessButton(self.project_basics_page)
        self.pst_plugin_installed_chckBox.setObjectName(_fromUtf8("pst_plugin_installed_chckBox"))
        self.verticalLayout_2.addWidget(self.pst_plugin_installed_chckBox)
        self.project_created_chckBox = QProcessButton(self.project_basics_page)
        self.project_created_chckBox.setObjectName(_fromUtf8("project_created_chckBox"))
        self.verticalLayout_2.addWidget(self.project_created_chckBox)
        self.osm_layer_loaded_chckBox = QProcessButton(self.project_basics_page)
        self.osm_layer_loaded_chckBox.setObjectName(_fromUtf8("osm_layer_loaded_chckBox"))
        self.verticalLayout_2.addWidget(self.osm_layer_loaded_chckBox)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.process_page.addWidget(self.project_basics_page)
        self.investigation_area_page = QtGui.QWidget()
        self.investigation_area_page.setAccessibleDescription(_fromUtf8(""))
        self.investigation_area_page.setObjectName(_fromUtf8("investigation_area_page"))
        self.verticalLayout = QtGui.QVBoxLayout(self.investigation_area_page)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.temp_shapefile_created_chckBox = QProcessButton(self.investigation_area_page)
        self.temp_shapefile_created_chckBox.setObjectName(_fromUtf8("temp_shapefile_created_chckBox"))
        self.verticalLayout.addWidget(self.temp_shapefile_created_chckBox)
        self.editing_temp_shapefile_started_chckBox = QProcessButton(self.investigation_area_page)
        self.editing_temp_shapefile_started_chckBox.setObjectName(_fromUtf8("editing_temp_shapefile_started_chckBox"))
        self.verticalLayout.addWidget(self.editing_temp_shapefile_started_chckBox)
        self.investigation_area_selected_chckBox = QProcessButton(self.investigation_area_page)
        self.investigation_area_selected_chckBox.setObjectName(_fromUtf8("investigation_area_selected_chckBox"))
        self.verticalLayout.addWidget(self.investigation_area_selected_chckBox)
        self.editing_temp_shapefile_stopped_chckBox = QProcessButton(self.investigation_area_page)
        self.editing_temp_shapefile_stopped_chckBox.setObjectName(_fromUtf8("editing_temp_shapefile_stopped_chckBox"))
        self.verticalLayout.addWidget(self.editing_temp_shapefile_stopped_chckBox)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.process_page.addWidget(self.investigation_area_page)
        self.building_shapes_page = QtGui.QWidget()
        self.building_shapes_page.setObjectName(_fromUtf8("building_shapes_page"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.building_shapes_page)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.housing_layer_loaded_chckBox = QProcessButton(self.building_shapes_page)
        self.housing_layer_loaded_chckBox.setObjectName(_fromUtf8("housing_layer_loaded_chckBox"))
        self.verticalLayout_6.addWidget(self.housing_layer_loaded_chckBox)
        self.building_coordinates_loaded_chckBox = QProcessButton(self.building_shapes_page)
        self.building_coordinates_loaded_chckBox.setObjectName(_fromUtf8("building_coordinates_loaded_chckBox"))
        self.verticalLayout_6.addWidget(self.building_coordinates_loaded_chckBox)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem4)
        self.process_page.addWidget(self.building_shapes_page)
        self.real_estate_cadaster_page = QtGui.QWidget()
        self.real_estate_cadaster_page.setAccessibleDescription(_fromUtf8(""))
        self.real_estate_cadaster_page.setObjectName(_fromUtf8("real_estate_cadaster_page"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.real_estate_cadaster_page)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.raster_loaded_chckBox = QProcessButton(self.real_estate_cadaster_page)
        self.raster_loaded_chckBox.setObjectName(_fromUtf8("raster_loaded_chckBox"))
        self.verticalLayout_3.addWidget(self.raster_loaded_chckBox)
        self.extent_clipped_chckBox = QProcessButton(self.real_estate_cadaster_page)
        self.extent_clipped_chckBox.setObjectName(_fromUtf8("extent_clipped_chckBox"))
        self.verticalLayout_3.addWidget(self.extent_clipped_chckBox)
        self.legend_created_chckBox = QProcessButton(self.real_estate_cadaster_page)
        self.legend_created_chckBox.setObjectName(_fromUtf8("legend_created_chckBox"))
        self.verticalLayout_3.addWidget(self.legend_created_chckBox)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.process_page.addWidget(self.real_estate_cadaster_page)
        self.sampling_points_page = QtGui.QWidget()
        self.sampling_points_page.setAccessibleDescription(_fromUtf8(""))
        self.sampling_points_page.setObjectName(_fromUtf8("sampling_points_page"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.sampling_points_page)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.temp_pointlayer_created_chckBox = QProcessButton(self.sampling_points_page)
        self.temp_pointlayer_created_chckBox.setObjectName(_fromUtf8("temp_pointlayer_created_chckBox"))
        self.verticalLayout_4.addWidget(self.temp_pointlayer_created_chckBox)
        self.editing_temp_pointlayer_started_chckBox = QProcessButton(self.sampling_points_page)
        self.editing_temp_pointlayer_started_chckBox.setObjectName(_fromUtf8("editing_temp_pointlayer_started_chckBox"))
        self.verticalLayout_4.addWidget(self.editing_temp_pointlayer_started_chckBox)
        self.points_of_interest_defined_chckBox = QProcessButton(self.sampling_points_page)
        self.points_of_interest_defined_chckBox.setObjectName(_fromUtf8("points_of_interest_defined_chckBox"))
        self.verticalLayout_4.addWidget(self.points_of_interest_defined_chckBox)
        self.editing_temp_pointlayer_stopped_chckBox = QProcessButton(self.sampling_points_page)
        self.editing_temp_pointlayer_stopped_chckBox.setObjectName(_fromUtf8("editing_temp_pointlayer_stopped_chckBox"))
        self.verticalLayout_4.addWidget(self.editing_temp_pointlayer_stopped_chckBox)
        self.information_sampled_chckBox = QProcessButton(self.sampling_points_page)
        self.information_sampled_chckBox.setObjectName(_fromUtf8("information_sampled_chckBox"))
        self.verticalLayout_4.addWidget(self.information_sampled_chckBox)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        self.process_page.addWidget(self.sampling_points_page)
        self.verticalLayout_5.addWidget(self.process_page)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.setSpacing(5)
        self.button_layout.setObjectName(_fromUtf8("button_layout"))
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.button_layout.addWidget(self.pushButton)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem7)
        self.process_button_next = QtGui.QPushButton(self.dockWidgetContents)
        self.process_button_next.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Controls/icons/arrow_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.process_button_next.setIcon(icon2)
        self.process_button_next.setIconSize(QtCore.QSize(16, 16))
        self.process_button_next.setObjectName(_fromUtf8("process_button_next"))
        self.button_layout.addWidget(self.process_button_next)
        self.verticalLayout_5.addLayout(self.button_layout)
        spacerItem8 = QtGui.QSpacerItem(20, 32, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem8)
        self.logo_layout = QtGui.QHBoxLayout()
        self.logo_layout.setObjectName(_fromUtf8("logo_layout"))
        self.oeq_clickable_logo = QClickableLabel(self.dockWidgetContents)
        self.oeq_clickable_logo.setMinimumSize(QtCore.QSize(350, 57))
        self.oeq_clickable_logo.setText(_fromUtf8(""))
        self.oeq_clickable_logo.setPixmap(QtGui.QPixmap(_fromUtf8(":/Brands/icons/OeQ_logo_footer.png")))
        self.oeq_clickable_logo.setObjectName(_fromUtf8("oeq_clickable_logo"))
        self.logo_layout.addWidget(self.oeq_clickable_logo)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.logo_layout.addItem(spacerItem9)
        self.verticalLayout_5.addLayout(self.logo_layout)
        MainProcess_dock.setWidget(self.dockWidgetContents)

        self.retranslateUi(MainProcess_dock)
        self.process_page.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainProcess_dock)

    def retranslateUi(self, MainProcess_dock):
        MainProcess_dock.setWindowTitle(_translate("MainProcess_dock", "Open eQuarter - Analysis", None))
        self.tools_dropdown_btn.setText(_translate("MainProcess_dock", "...", None))
        self.label.setText(_translate("MainProcess_dock", "Currently viewing:", None))
        self.project_basics_page.setAccessibleName(_translate("MainProcess_dock", "Project Basics", None))
        self.ol_plugin_installed_chckBox.setText(_translate("MainProcess_dock", "Install the Open Street Map Plugin", None))
        self.pst_plugin_installed_chckBox.setText(_translate("MainProcess_dock", "Install the PointSamplingTool Plugin", None))
        self.project_created_chckBox.setText(_translate("MainProcess_dock", "Create a new project and save it.", None))
        self.osm_layer_loaded_chckBox.setText(_translate("MainProcess_dock", "Open an Open Layers Map", None))
        self.investigation_area_page.setAccessibleName(_translate("MainProcess_dock", "Investigation Area", None))
        self.temp_shapefile_created_chckBox.setText(_translate("MainProcess_dock", "Create a new Polygon-Shapelayer", None))
        self.editing_temp_shapefile_started_chckBox.setText(_translate("MainProcess_dock", "Activate the edit mode", None))
        self.investigation_area_selected_chckBox.setText(_translate("MainProcess_dock", "Add new features to cover your\n"
"investigation area with", None))
        self.editing_temp_shapefile_stopped_chckBox.setText(_translate("MainProcess_dock", "Deactivate the edit mode", None))
        self.building_shapes_page.setAccessibleName(_translate("MainProcess_dock", "Building Shapes", None))
        self.housing_layer_loaded_chckBox.setText(_translate("MainProcess_dock", "Load a floor plan layer (\'Hausumringe\')", None))
        self.building_coordinates_loaded_chckBox.setText(_translate("MainProcess_dock", "Load building coordinates", None))
        self.real_estate_cadaster_page.setAccessibleName(_translate("MainProcess_dock", "Real Estate Cadaster", None))
        self.raster_loaded_chckBox.setText(_translate("MainProcess_dock", "Load a new (wms) raster-map", None))
        self.extent_clipped_chckBox.setText(_translate("MainProcess_dock", "Export the investigation areas extent as .tif", None))
        self.legend_created_chckBox.setText(_translate("MainProcess_dock", "Create a legend for the clipped .tif-file", None))
        self.sampling_points_page.setAccessibleName(_translate("MainProcess_dock", "Point Sampling", None))
        self.temp_pointlayer_created_chckBox.setText(_translate("MainProcess_dock", "Create a new Pointlayer", None))
        self.editing_temp_pointlayer_started_chckBox.setText(_translate("MainProcess_dock", "Activate the edit mode", None))
        self.points_of_interest_defined_chckBox.setText(_translate("MainProcess_dock", "Add new features to mark the buildings \n"
"you want to extract information from", None))
        self.editing_temp_pointlayer_stopped_chckBox.setText(_translate("MainProcess_dock", "Deactivate the edit mode", None))
        self.information_sampled_chckBox.setText(_translate("MainProcess_dock", "Use the point-sampling-tool to extract\n"
"the information", None))
        self.pushButton.setText(_translate("MainProcess_dock", "Cancel", None))
        self.process_button_next.setText(_translate("MainProcess_dock", "Next step", None))

from oeq_ui_classes import QClickableLabel, QProcessButton
import resources_rc
