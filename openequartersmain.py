# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenEQuartersMain
                                 A QGIS plugin
 The plugin automates the setup for investigating an area.
                              -------------------
        begin                : 2014-10-07
        copyright            : (C) 2014 by Kim Gülle / UdK-Berlin
        email                : kimonline@example.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import iface
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from ProjectDoesNotEexist_dialog import ProjectDoesNotExist_dialog
import os.path
import OsmInteraction


class OpenEQuartersMain:

    def __init__(self, iface):

        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'openequartersmain_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.project_does_not_exist_dlg = ProjectDoesNotExist_dialog()

        self.project_path = QgsProject.instance().readPath('./')

        self.plugin_name = 'openlayers_plugin'
        self.open_layer_type_id = 0

    def initGui(self):
        # Create action that will start plugin configuration
        plugin_icon = QIcon("/Users/VPTtutor/Documents/QGIS/plugins/OpenEQuartersMain/icon.png")
        self.action = QAction( plugin_icon, u"OpenEQuarters-Process", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&OpenEQuarters", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&OpenEQuarters", self.action)
        self.iface.removeToolBarIcon(self.action)


    def create_project_ifNotExists(self):

        self.project_path = QgsProject.instance().readPath('./')
        if self.project_path == './':
            self.project_does_not_exist_dlg.show()
            yes_to_save = self.project_does_not_exist_dlg.exec_()

            if yes_to_save:
                project_actions = self.iface.projectMenu().actions()

                for act in project_actions:
                    if act.text() == 'Save &As...':
                        act.trigger()


    def load_osm_layer(self):

        osmi = OsmInteraction
        open_layers_plugin = osmi.get_open_layers_plugin_ifexists(self.plugin_name)
        if open_layers_plugin:
            osmi.open_osm_layer(open_layers_plugin, self.open_layer_type_id)


    def create_new_shapefile(self):
        #ToDo surpress crs-choice-dlg
        # shapeLayer = QgsVectorLayer("Polygon", "Investigation Area", "memory")


        return


    def change_to_edit_mode(self):
        #ToDo
        return


    def change_osm_layer(self, mode='hide'):
        #ToDo
        # either hide or remove the formerly loaded osm layer
        return


    def load_housing_layer(self):
        #ToDo
        return


    def extract_shape_views(self):
        #ToDo
        # store local copies of the selected areas
        return


    def add_housing_coordinates(self):
        #ToDo
        return


    # run method that performs all the real work
    def run(self):

        # if no project exists, create one first
        self.create_project_ifNotExists()
        self.project_path = QgsProject.instance().readPath('./')

        # if no project was created stop execution
        if self.project_path == './':
            return

        # start the process, if a project was created
        else:
            self.load_osm_layer()
