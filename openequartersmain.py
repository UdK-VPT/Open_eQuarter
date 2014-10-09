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
from RequestWmsUrl_dialog import RequestWmsUrl_dialog
from socket import gaierror
import os.path
import OsmInteraction
import numpy
import time
import httplib

class OpenEQuartersMain:

    def __init__(self, iface):

        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'openequartersmain_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialogues (after translation) and keep references
        self.project_does_not_exist_dlg = ProjectDoesNotExist_dialog()
        self.project_path = QgsProject.instance().readPath('./')

        self.request_wms_url_dlg = RequestWmsUrl_dialog()
        self.wms_url = ""

        # ToDo set crs back to 4326
        self.project_crs = 'EPSG:3857'
        # extent of Germany
        self.default_extent = QgsRectangle(numpy.float64(480310.4063808322), numpy.float64(5930330.009070959), numpy.float64(1813151.46638856), numpy.float64(7245291.493883461))
        self.default_extent_crs = 'EPSG:3857'
        self.default_scale = 4607478


        self.plugin_name = 'openlayers_plugin'
        # id=0 - Google Physical
        # id=1 - Google Streets
        self.open_layer_type_id = 1

    def initGui(self):
        # Create action that will start plugin configuration
        plugin_icon = QIcon('/Users/VPTtutor/Documents/QGIS/plugins/OpenEQuartersMain/icon.png')
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

        return


    def zoom_to_default_extent(self):

        canvas = self.iface.mapCanvas()

        # if plugin was started out of new or empty project, zoom to default extent
        # !!!!!! A print statement has to be executed prior to calling the layerCount() function
        print "Zoom to default extent"
        # !!!!!! apparently the layerCount()-function does not flush properly
        if canvas.layerCount() >= 0 and canvas.layerCount() <= 2:
            canvas.zoomScale(self.default_scale)
            canvas.setExtent(self.default_extent)
            canvas.refresh()

        return

    def set_project_crs(self, crs):

        # if the given crs is valid
        if not crs.isspace() and QgsCoordinateReferenceSystem().createFromUserInput(crs):

            canvas = self.iface.mapCanvas()


            # if some layers were existing prior to starting the plugin
            # !!!!!! A print statement has to be executed prior to calling the layerCount() function
            print "Zoom to default extent"
            # !!!!!! apparently the layerCount()-function does not flush properly
            if canvas.layerCount() > 2:
                extent = canvas.extent()                                # save formerly viewed extent
                current_crs = canvas.mapSettings().destinationCrs()     # set to project-crs
                current_scale = canvas.scale()

            # if the plugin was started from a new or empty project
            else:
                print "Else default"
                print canvas.layerCount()
                extent = self.default_extent                                        # set extent to default view
                current_crs = QgsCoordinateReferenceSystem(self.default_extent_crs) # corresponding crs
                current_scale = self.default_scale

            renderer = canvas.mapRenderer()
            new_crs = QgsCoordinateReferenceSystem(crs)
            renderer.setDestinationCrs(new_crs)


            canvas.zoomScale(current_scale)

            if not current_crs == new_crs:
                # set extent, by transforming the formerly saved extent to new Projection
                coord_transformer = QgsCoordinateTransform(current_crs, new_crs)
                canvas.setExtent(coord_transformer.transform(extent))

            canvas.setExtent(extent)
            canvas.refresh()

        return


    def load_osm_layer(self):

        osmi = OsmInteraction
        open_layers_plugin = osmi.get_open_layers_plugin_ifexists(self.plugin_name)
        if open_layers_plugin:
            osmi.open_osm_layer(open_layers_plugin, self.open_layer_type_id)

            canvas = self.iface.mapCanvas()
            # if current scale is below osm-layers visibility, rescale canvas
            if canvas.scale() < 850:
                canvas.zoomScale(850)
                canvas.refresh()

        return


    def get_project_crs(self, iface):

        canvas = iface.mapCanvas()
        crs = canvas.mapSettings().destinationCrs()

        return crs


    def create_new_shapefile(self):

        # surpress crs-choice dialog
        old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'prompt'))
        QSettings().setValue('/Projections/defaultBehaviour', 'useProject')

        # create a new polygon shape-file, named 'Investigation Area' with system encoding and project crs
        type = 'Polygon'
        crs = '?crs=' + self.project_crs
        shape_layer = QgsVectorLayer(type + crs, 'Investigation Area', 'memory')
        shape_layer.setProviderEncoding('System')

        # add the layer to the layer-legend
        QgsMapLayerRegistry.instance().addMapLayer(shape_layer)

        #ToDo change the layer order and put the new layer first

        # reset appearance of crs-choice dialog to previous settings
        QSettings().setValue('/Projections/defaultBehaviour', old_validation)

        return


    def change_to_edit_mode(self):

        # activate the shape-layer to start adding features
        for layer in self.iface.legendInterface().layers():

            if layer.name() == 'Investigation Area':
                self.iface.setActiveLayer(layer)

        # once the layer is activated, the editing and the adding of features will be triggered
        self.iface.actionToggleEditing().trigger()
        self.iface.actionAddFeature().trigger()

        return


    def request_wms_layer_url(self):

        self.request_wms_url_dlg.show()
        url_confirmed = self.request_wms_url_dlg.exec_()

        # if 'ok' was hit, get the url
        if url_confirmed:
            wms_url = self.request_wms_url_dlg.wms_url.text()

            try:
                if wms_url.startswith("http"):
                    socket = httplib.HTTPConnection(wms_url[7:])
                    socket.connect()
                else:
                    socket = httplib.HTTPConnection(wms_url)
                    socket.connect()

            except (httplib.HTTPException, gaierror) as ex:
                print "Invalid url"
                return

            self.wms_url = wms_url

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
            """
            self.load_osm_layer()
            self.create_new_shapefile()
            self.zoom_to_default_extent()
            self.change_to_edit_mode()
            """
            self.request_wms_layer_url()

            #self.set_project_crs(self.project_crs)
