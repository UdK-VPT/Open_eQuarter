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
from InvestigationAreaSelected_dialog import InvestigationAreaSelected_dialog
import OsmInteraction
from saveselectionwithpyramid import SaveSelectionWithPyramid

from socket import gaierror
import os.path
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

        self.confirm_selection_of_investigation_area_dlg = InvestigationAreaSelected_dialog()

        # ToDo set crs back to 4326
        self.project_crs = 'EPSG:4326'
        # extent of Germany
        self.default_extent = QgsRectangle(numpy.float64(480310.4063808322), numpy.float64(5930330.009070959), numpy.float64(1813151.46638856), numpy.float64(7245291.493883461))
        self.default_extent_crs = 'EPSG:3857'
        self.default_scale = 4607478

        # name of the shapefile which will be created to define the investigation area
        self.investigation_shape_layer_name = 'Investigation Area'

        # name of the wms-raster which will be loaded and is the basis for the clipping
        self.clipping_raster_layer_name = "Investigation Area - raster"

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
        """
        If the current workspace has not been saved as a project, prompt the user to "Save As..." project
        :return:
        :rtype:
        """
        # read the current project path
        self.project_path = QgsProject.instance().readPath('./')

        # if the path is './', the project has not yet been saved
        if self.project_path == './':

            # prompt the user to save the project
            self.project_does_not_exist_dlg.show()
            yes_to_save = self.project_does_not_exist_dlg.exec_()

            if yes_to_save:
                project_actions = self.iface.projectMenu().actions()

                # trigger qgis "Save As"-function
                for act in project_actions:
                    if act.text() == 'Save &As...':
                        act.trigger()

    def enable_on_the_fly_projection(self):
        """
        Enable on the fly projection in the current project.
        :return:
        :rtype:
        """
        self.iface.mapCanvas().mapRenderer().setProjectionsEnabled(True)

    def load_osm_layer(self):
        """
        Use the OsmInteraction-methods to interact with the Open-Street-Map plugin and open an open street map according to self.open_layer_type_id
        :return:
        :rtype:
        """
        # save a static reference to the methods that interact with the open-layers plugin
        osmi = OsmInteraction
        open_layers_plugin_installed = osmi.get_open_layers_plugin_ifexists(self.plugin_name)

        if open_layers_plugin_installed:

            # open an osm-layer according to its id
            osmi.open_osm_layer(self.open_layer_type_id)

            # if current scale is below osm-layers visibility, rescale canvas
            canvas = self.iface.mapCanvas()
            if canvas.scale() < 850:
                canvas.zoomScale(850)
                canvas.refresh()

    def zoom_to_default_extent(self):
        """
        Set the canvas-extent to the extent and scale specified in self.default_extent and self.default_scale
        :return:
        :rtype:
        """
        canvas = self.iface.mapCanvas()

        # if plugin was started out of new or empty project, zoom to default extent
        # !!!!!! A print statement has to be executed prior to calling the layerCount() function
        print ""
        # !!!!!! apparently the layerCount()-function does not flush properly
        if canvas.layerCount() >= 0 and canvas.layerCount() <= 2:
            canvas.zoomScale(self.default_scale)
            canvas.setExtent(self.default_extent)
            canvas.refresh()

    def create_new_shapefile(self, layer_name):
        """
        Create and add a new Polygon-Vectorlayer, with the name as specified in layer_name
        :param layer_name: The name of the new vectorlayer
        :type layer_name: str
        :return:
        :rtype:
        """
        if layer_name and not layer_name.isspace():
            # surpress crs-choice dialog
            old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'prompt'))
            QSettings().setValue('/Projections/defaultBehaviour', 'useProject')

            # create a new polygon shape-file called layer_name, with system encoding and project crs
            type = 'Polygon'
            crs = '?crs=' + self.project_crs
            shape_layer = QgsVectorLayer(type + crs, layer_name, 'memory')
            shape_layer.setProviderEncoding('System')

            # add the layer to the layer-legend
            QgsMapLayerRegistry.instance().addMapLayer(shape_layer)

            #ToDo change the layer order and put the new layer first
            # (not nescessary atm, since the layer already is on top, if loaded in an empty project)

            # reset appearance of crs-choice dialog to previous settings
            QSettings().setValue('/Projections/defaultBehaviour', old_validation)

    def change_to_edit_mode(self, layer_name):
        """
        Iterate over all layers and activate the Layer called layer_name. Then toggle the edit mode of that layer.
        :param layer_name: Name of the layer, that shall be switched to edit_mode
        :type layer_name: str
        :return:
        :rtype:
        """
        if layer_name and not layer_name.isspace():

            edit_layer = self.find_layer_by_name(layer_name)

            # if the layer was found, it is activated and the editing and the adding of features will be triggered
            if edit_layer:
                self.iface.setActiveLayer(layer)
                self.iface.actionToggleEditing().trigger()
                self.iface.actionAddFeature().trigger()

    def confirm_selection_of_investigation_area(self, layer_name):
        """
        Select the layer named 'layer_name' from layers list and trigger the ToggleEditing button
        :param layer_name: Name of the layer whose editing mode shall be triggered
        :type layer_name: str
        :return:
        :rtype:
        """
        if layer_name and not layer_name.isspace():

            edit_layer = self.find_layer_by_name(layer_name)

            # if the layer was found, prompt the user to confirm the adding-feature-process was finished
            if edit_layer:

                self.confirm_selection_of_investigation_area_dlg.show()
                confirmation = self.confirm_selection_of_investigation_area_dlg.exec_()

                # if the finalization of the process was confirmed, turn of the edit mode (by default, the user will be asked to save his changes)
                if confirmation:
                    self.iface.setActiveLayer(edit_layer)
                    self.iface.actionToggleEditing().trigger()

    def request_wms_layer_url(self):
        """
        Open a dialog and request an url to a wms-server. Check if the given url is valid, by trying to connect to the server.
        :return:
        :rtype:
        """
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

    def open_wms_as_raster(self):
        """
        Use the url in self.wms_url to open and add a raster layer
        :return:
        :rtype:
        """
        urlWithParams = 'crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k5'
        rlayer = QgsRasterLayer(urlWithParams, self.clipping_raster_layer_name, 'wms')
        #rlayer = QgsRasterLayer(self.wms_url, 'Raster layer basis', 'wms')
        if not rlayer.isValid():
            print "Layer failed to load!"
        else:
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            self.iface.setActiveLayer(rlayer)

    def open_add_wms_dialog(self):
        """
        Open the common QGIS "Add WMS/WMTS Layer..."-dialog
        :return:
        :rtype:
        """
        #ToDo use this or the open_wms_as_raster function
        self.iface.actionAddWmsLayer().trigger()

    def set_project_crs(self, crs):
        """
        Set the project crs to the given crs and do a re-projection to keep the currently viewed extent focused
        :param crs: The new crs to set the project to
        :type crs: str
        :return:
        :rtype:
        """
        # if the given crs is valid
        if not crs.isspace() and QgsCoordinateReferenceSystem().createFromUserInput(crs):

            canvas = self.iface.mapCanvas()

            extent = canvas.extent()             # save formerly viewed extent
            current_crs = self.get_project_crs() # get project-crs
            current_scale = canvas.scale()

            renderer = canvas.mapRenderer()
            new_crs = QgsCoordinateReferenceSystem(crs)
            renderer.setDestinationCrs(new_crs)

            canvas.zoomScale(current_scale)

            if not current_crs == new_crs:
                # set extent, by transforming the formerly saved extent to new Projection
                coord_transformer = QgsCoordinateTransform(current_crs, new_crs)
                extent = coord_transformer.transform(extent)

            canvas.setExtent(extent)
            canvas.refresh()

    def get_project_crs(self):
        """
        Return the project crs
        :return: The project crs
        :rtype: QgsCoordinateReferenceSystem
        """

        canvas = iface.mapCanvas()
        crs = canvas.mapSettings().destinationCrs()

        return crs

    def clip_zoom_to_layer_view_from_raster(self, layer_name, raster_name):
        """
        Zoom to a given vector-layer, containing shape files. Extract the currently viewed extent from an underlying raster-layer into a new .tif and open it.
        :param layer_name: Name of the vector-layer
        :type layer_name: str
        :param raster_name: Name of the raster-layer, which will be the basis of the new clip
        :type raster_name:
        :return:
        :rtype:
        """
        if layer_name and not layer_name.isspace() and raster_name and not raster_name.isspace():
            investigation_shape = None
            clipping_raster = None

            # get the shapefile and the raster layer
            for layer in self.iface.legendInterface().layers():

                if layer.name() == layer_name:
                    investigation_shape = layer
                elif layer.name() == raster_name:
                    clipping_raster = layer

            # if the shapefile was found set the layer active
            if investigation_shape is not None and clipping_raster is not None:
                self.iface.setActiveLayer(investigation_shape)
                view_actions = self.iface.viewMenu().actions()

                # trigger the "zoom to layer"-function on the formerly activated layer
                for act in view_actions:
                    if act.text() == 'Zoom to Layer':
                        act.trigger()

                # set the rasterlayer as active and start the export
                self.iface.setActiveLayer(clipping_raster)
                pyramid_exporter = SaveSelectionWithPyramid(self.iface)
                pyramid_exporter.export()

    # Method not yet used
    def get_extent_per_feature(self, layer_name):
        """
        Iterate over all features of a given layer and return the extents (as a list of rectangles) of each feature
        :param layer_name: Name of the layer
        :type layer_name: str
        :return feature_extents:
        :rtype <QgsRectangle>:
        """
        if layer_name and not layer_name.isspace():
            shape = None
            # get the shapefile
            for layer in self.iface.legendInterface().layers():

                 if layer.name() == layer_name:
                    shape = layer

            if shape is not None:

                iterator = shape.getFeatures()
                feature_extents = []

                for feature in iterator:

                    geom = feature.geometry()
                    polygons = geom.asPolygon()

                    for polygon in polygons:

                        extent_coordinates = self.find_x_min_y_min_x_max_y_max(polygon)
                        extent = QgsRectangle(extent_coordinates[0], extent_coordinates[1], extent_coordinates[2], extent_coordinates[3])
                        feature_extents.append(extent)

        return feature_extents

    # Method not yet used
    def find_x_min_y_min_x_max_y_max(self, polygon):
        """
        Iterate over all points of a given polygon and return the x- and y-extremes.
        :param polygon: A list of QgsPoint-Objects, which form a polygon
        :type polygon: <QgsPoint>
        :return: the extent of the polygon (lowest x, y and highest x,y)
        :rtype: float, float, float, float
        """

        x_max = x_min = polygon[0].x()
        y_max = y_min = polygon[0].y()

        for point in polygon[1:]:

            if point.x() >= x_max:
                x_max = point.x()
            elif point.x() <= x_min:
                x_min = point.x()

            if point.y() >= y_max:
                y_max = point.y()
            elif point.y() <= y_min:
                y_min = point.y()

        return x_min, y_min, x_max, y_max

    def hide_or_remove_layer(self, layer_name, mode='hide'):
        """
        Hide or remove the given layer from the MapLayerRegistry, depending on the mode.
        :param layer_name: Name of the layer to remove/hide
        :type layer_name: str
        :param mode: What to do with the layer; valid arguments are 'hide' or 'remove'
        :type mode: str
        :return:
        :rtype:
        """
        if layer_name and not layer_name.isspace():
            for layer in self.iface.mapCanvas().layers():
                if layer.name() == layer_name:
                    if mode == 'remove':
                        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())

                    if mode == 'hide':
                        self.iface.legendInterface().setLayerVisible(layer, False)

    def find_layer_by_name(self, layer_name):
        """
        Iterate over all layers and find and return the layer with the name layer_name
        :param layer_name: Name of the layer that shall be looked for
        :type layer_name: str
        :return:
        :rtype:
        """
        if layer_name and not layer_name.isspace():

            for layer in self.iface.mapCanvas().layers():
                if layer.name() == layer_name:
                    return layer

    def load_housing_layer(self):
        #ToDo
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
            self.enable_on_the_fly_projection()

            self.load_osm_layer()
            self.zoom_to_default_extent()
            self.create_new_shapefile(self.investigation_shape_layer_name)

            self.change_to_edit_mode(self.investigation_shape_layer_name)
            self.confirm_selection_of_investigation_area(self.investigation_shape_layer_name)

            #self.request_wms_layer_url()
            self.open_wms_as_raster()

            self.clip_zoom_to_layer_view_from_raster(self.investigation_shape_layer_name, self.clipping_raster_layer_name)
            self.hide_or_remove_layer(self.clipping_raster_layer_name, 'remove')
            self.hide_or_remove_layer("Google Streets", 'hide')
            self.set_project_crs(self.project_crs)

