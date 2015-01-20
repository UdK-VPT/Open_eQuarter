# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenEQuarterMain
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
import time
from qgis.core import *
from qgis.utils import iface, plugins
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from MainstayProcess_dialog import MainstayProcess_dialog
from ProjectDoesNotEexist_dialog import ProjectDoesNotExist_dialog
from RequestWmsUrl_dialog import RequestWmsUrl_dialog
from InvestigationAreaSelected_dialog import InvestigationAreaSelected_dialog
from PstInteraction import *
from OlInteraction import *
import LayerInteraction
from ExportWMSasTif import SaveSelectionWithPyramid
from Processing import *
from Tests.LayerInteraction_test import LayerInteraction_test

from socket import gaierror
import os.path
import numpy
import httplib
import unittest

class OpenEQuarterMain:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        ### Plugin specific settings
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'OpenEQuartermain_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        ### UI specific settings
        # Create the dialogues (after translation) and keep references
        self.mainstay_process_dlg = MainstayProcess_dialog()
        self.project_does_not_exist_dlg = ProjectDoesNotExist_dialog()
        self.request_wms_url_dlg = RequestWmsUrl_dialog()
        self.wms_url = 'crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k5'
        self.confirm_selection_of_investigation_area_dlg = InvestigationAreaSelected_dialog()


        ### Project specific settings
        # the project path is './' as long as the project has not been saved
        self.project_path = QgsProject.instance().readPath('./')
        self.project_crs = 'EPSG:3857' # ToDo set crs back to 4326


        ### Information needed to use external plugins
        # PointSamplingTool
        self.pst_plugin_name = 'pointsamplingtool'
        self.pst_input_layer_name = 'testpunkte'
        self.pst_output_layer_path = '/Users/VPTtutor/Documents/QGIS/plugin_oeq-qgs_project/Testpunkte/'
        self.pst_output_layer_name = 'pst_out'


        # OpenStreetMap plugin
        self.ol_plugin_name = 'openlayers_plugin'
        # id=0 - Google Physical
        # id=1 - Google Streets
        # id=4 - OpenStreetMap
        self.open_layer_type_id = 4


        ### Default values
        # default extent, after the OSM-layer was loaded (currently: extent of Germany)
        self.default_extent = QgsRectangle(numpy.float64(480310.4063808322), numpy.float64(5930330.009070959), numpy.float64(1813151.46638856), numpy.float64(7245291.493883461))
        self.default_extent_crs = 'EPSG:3857'
        self.default_scale = 4607478

        # name of the shapefile which will be created to define the investigation area
        self.investigation_shape_layer_name = 'Investigation Area'
        self.investigation_shape_layer_style = os.path.join(self.plugin_dir, 'Styles', 'oeq_ia_style.qml')

        # name of the wms-raster which will be loaded and is the basis for the clipping
        self.clipping_raster_layer_name = 'Investigation Area - raster'

        ### Monitor the users progress
        self.process_monitor = Processing(self.mainstay_process_dlg)
        #ToDo have step_queue created from the process list in the Processing class
        self.step_queue = ['ol_plugin_installed', 'pst_plugin_installed', 'project_created', 'osm_layer_loaded',
                           'temp_shapefile_created', 'editing_temp_shapefile_started', 'investigation_area_selected', 'editing_temp_shapefile_stopped',
                           'raster_loaded', 'extent_clipped', 'pyramids_built',
                           'temp_pointlayer_created', 'editing_temp_pointlayer_started', 'points_of_interest_defined', 'editing_temp_pointlayer_stopped', 'information_sampled']

    def initGui(self):

        # Create action that will start plugin configuration
        plugin_icon = QIcon(os.path.join(self.plugin_dir, 'Icons', 'main.png'))
        self.main_action = QAction( plugin_icon, u"OpenEQuarter-Process", self.iface.mainWindow())
        # connect the action to the run method
        self.main_action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.main_action)
        self.iface.addPluginToMenu(u"&OpenEQuarter", self.main_action)

        clipping_icon = QIcon(os.path.join(self.plugin_dir, 'Icons', 'scissor.png'))
        self.clipping_action = QAction(clipping_icon, u"Extract extent from active WMS", self.iface.mainWindow())
        self.clipping_action.triggered.connect(lambda: self.clip_from_raster(self.iface.activeLayer()))
        self.iface.addToolBarIcon(self.clipping_action)
        self.iface.addPluginToMenu(u"&OpenEQuarter", self.clipping_action)

        testing_icon = QIcon(os.path.join(self.plugin_dir, 'Icons', 'lightbulb.png'))
        self.testing_action = QAction(testing_icon, u"Run all unit-tests", self.iface.mainWindow())
        self.testing_action.triggered.connect(lambda: self.run_tests())
        self.iface.addToolBarIcon(self.testing_action)
        self.iface.addPluginToMenu(u"&OpenEQuarter", self.testing_action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&OpenEQuarter", self.main_action)
        self.iface.removeToolBarIcon(self.main_action)
        self.iface.removeToolBarIcon(self.clipping_action)
        self.iface.removeToolBarIcon(self.testing_action)

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
                iface.actionSaveProjectAs().trigger()


    def get_plugin_ifexists(self, plugin_name):
        """
        Check if a plugin with the given name exists.

        :param plugin_name: Name of the plugin to check existence of.
        :type plugin_name: str

        :return plugin: Return the plugin if it was found
        :rtype: OpenlayersPlugin instance

        :return False: Return False if the plugin was not found and the lookup resulted in an exception.
        :rtype: bool
        """

        if not plugin_name or plugin_name.isspace():
            return None

        plugin_dict = plugins

        try:
            plugin = plugin_dict[plugin_name]
            return plugin
        except KeyError:
            print "No plugin with the given name '" + plugin_name + "' found. Please check the plugin settings."
            return None

    def osm_layer_is_loaded(self):
        """
        Iterate over all layers and check if an osm plugin-layer exists.
        :return True if the layer is available:
        :rtype bool:
        """
        for layer in QgsMapLayerRegistry.instance().mapLayers():
            if 'OpenLayers_plugin_layer' in layer:
                return True

        return False

    def zoom_to_default_extent(self):
        """
        Set the canvas-extent to the extent and scale specified in self.default_extent and self.default_scale
        :return:
        :rtype:
        """

        print "zoom"
        canvas = self.iface.mapCanvas()
        layers = QgsMapLayerRegistry.instance().mapLayers()

        if len(layers) >= 0 and len(layers) <= 2:
            print "zoom2"
            canvas.zoomScale(self.default_scale)
            canvas.setExtent(self.default_extent)
            canvas.refresh()

    def confirm_selection_of_investigation_area(self, layer_name):
        """
        Select the layer named 'layer_name' from layers list and trigger the ToggleEditing button
        :param layer_name: Name of the layer whose editing mode shall be triggered
        :type layer_name: str
        :return:
        :rtype:
        """
        if layer_name and not layer_name.isspace():

            edit_layer = LayerInteraction.find_layer_by_name(layer_name)

            # if the layer was found, prompt the user to confirm the adding-feature-process was finished
            if edit_layer:

                self.confirm_selection_of_investigation_area_dlg.show()
                confirmation = self.confirm_selection_of_investigation_area_dlg.exec_()

                # if the finalization of the process was confirmed, return True
                if confirmation:
                    return True

                else:
                    return False

    # method currently not in use
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

    def clip_from_raster(self, raster_layer):

        if raster_layer is not None and raster_layer.isValid():
            # set the rasterlayer as active, since only the active layer will be clipped and start the export
            self.iface.setActiveLayer(raster_layer)
            pyramid_exporter = SaveSelectionWithPyramid(self.iface)
            pyramid_exporter.export(raster_layer.name())

    def clip_zoom_to_layer_view_from_raster(self, layer_name):
        """
        Zoom to a given vector-layer, containing shape files. Extract the currently viewed extent from an underlying raster-layer into a new .tif and open it.
        :param layer_name: Name of the vector-layer
        :type layer_name: str
        :return:
        :rtype:
        """
        if layer_name and not layer_name.isspace():

            # get the shapefile and the raster layer
            investigation_shape = LayerInteraction.find_layer_by_name(layer_name)

            # if the shapefile was found set the layer active
            if investigation_shape is not None:
                self.iface.setActiveLayer(investigation_shape)
                view_actions = self.iface.viewMenu().actions()

                # trigger the "zoom to layer"-function on the formerly activated layer
                for act in view_actions:
                    if act.text() == 'Zoom to Layer':
                        act.trigger()

                # clip extent from visible raster layers
                raster_layers = LayerInteraction.get_wms_layer_list(self.iface, 'visible')
                for clipping_raster in raster_layers:
                    self.clip_from_raster(clipping_raster)

    # Method not used yet
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

    # Method not used yet
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

    def load_housing_layer(self):
        #ToDo
        return

    def add_housing_coordinates(self):
        #ToDo
        return

    def start_or_continue_process(self):

        next_step = self.process_monitor.calculate_progress()

        ### Project basics
        # check if "open layers"-plugin is installed
        if self.step_queue[next_step] == 'ol_plugin_installed' and self.get_plugin_ifexists(self.ol_plugin_name) is not None:
            self.process_monitor.update_progress('project_basics', 'ol_plugin_installed', True)



        # check if the pointsampling-tool is installed
        if self.step_queue[next_step] == 'pst_plugin_installed' and self.get_plugin_ifexists(self.pst_plugin_name) is not None:
            self.process_monitor.update_progress('project_basics', 'pst_plugin_installed', True)



        # check if the project has been saved
        if self.step_queue[next_step] == 'project_created' and not self.process_monitor.is_in_progress('project_basics', 'pst_plugin_installed', 'ol_plugin_installed'):

            self.mainstay_process_dlg.go_to_page('project_basics')

            # if no project exists, create one first
            self.create_project_ifNotExists()
            self.project_path = QgsProject.instance().readPath('./')

            # if project was created stop execution
            if self.project_path != './':
                self.process_monitor.update_progress('project_basics', 'project_created', True)



        # check if steps 1 to 3 have succeeded
        if self.step_queue[next_step] == 'osm_layer_loaded' and not self.process_monitor.is_in_progress('project_basics','pst_plugin_installed', 'ol_plugin_installed', 'project_created'):

            if self.osm_layer_is_loaded():
                self.process_monitor.update_progress('project_basics', 'osm_layer_loaded', True)

            else:
                ol_plugin = OlInteraction(self.ol_plugin_name)
                # self.enable_on_the_fly_projection()
                # self.set_project_crs(self.default_extent_crs)

                if ol_plugin.open_osm_layer(self.open_layer_type_id):
                    self.process_monitor.update_progress('project_basics', 'osm_layer_loaded', True)
                    self.zoom_to_default_extent()



        ### Investigation Area
        # if the "project basics"-process is done, continue with the IA-process
        if self.step_queue[next_step] == 'temp_shapefile_created' and not self.process_monitor.is_in_progress('project_basics') and self.process_monitor.is_in_progress('investigation_area'):

            # create a new shape-layer
            if self.process_monitor.is_in_progress('investigation_area', 'temp_shapefile_created'):
                self.mainstay_process_dlg.go_to_page('investigation_area')

                investigation_area = LayerInteraction.create_temporary_layer(self.investigation_shape_layer_name, 'Polygon', self.project_crs)

                if investigation_area is not None:
                    LayerInteraction.add_style_to_layer(self.investigation_shape_layer_style, investigation_area)
                    LayerInteraction.add_layer_to_registry(investigation_area)
                    self.process_monitor.update_progress('investigation_area', 'temp_shapefile_created', True)


        # trigger the edit-mode of the recently created layer
        if self.step_queue[next_step] == 'editing_temp_shapefile_started' and self.process_monitor.is_in_progress('investigation_area', 'investigation_area_selected'):
            if not self.process_monitor.is_in_progress('investigation_area', 'temp_shapefile_created'):
                LayerInteraction.trigger_edit_mode(self.iface, self.investigation_shape_layer_name)
                self.process_monitor.update_progress('investigation_area', 'editing_temp_shapefile_started', True)

            if not self.process_monitor.is_in_progress('investigation_area', 'temp_shapefile_created', 'editing_temp_shapefile_started'):
                ia_covered = self.confirm_selection_of_investigation_area(self.investigation_shape_layer_name)
                self.process_monitor.update_progress('investigation_area', 'investigation_area_selected', ia_covered)

            if not self.process_monitor.is_in_progress('investigation_area', 'temp_shapefile_created', 'editing_temp_shapefile_started', 'investigation_area_selected'):
                LayerInteraction.trigger_edit_mode(self.iface, self.investigation_shape_layer_name, 'off')
                self.process_monitor.update_progress('investigation_area', 'editing_temp_shapefile_stopped', True)

        ### Raster-clipping and shape-building process
        # if the "investigation area"-process is completed
        if self.step_queue[next_step] == 'raster_loaded' and not self.process_monitor.is_in_progress('investigation_area'):

            # open a wms-raster
            if self.process_monitor.is_in_progress('building_shapes', 'raster_loaded'):
                self.mainstay_process_dlg.go_to_page('building_shapes')
                #self.request_wms_layer_url()
                investigation_raster_layer = LayerInteraction.open_wms_as_raster(self.iface, self.wms_url, self.clipping_raster_layer_name)

                if investigation_raster_layer is not None and investigation_raster_layer.isValid():
                    LayerInteraction.add_layer_to_registry(investigation_raster_layer)
                    self.iface.setActiveLayer(investigation_raster_layer)
                    self.process_monitor.update_progress('building_shapes', 'raster_loaded', True )

                else:
                    self.iface.actionAddWmsLayer().trigger()

        if self.step_queue[next_step] == 'extent_clipped' and not self.process_monitor.is_in_progress('investigation_area'):

            if not self.process_monitor.is_in_progress('building_shapes', 'raster_loaded') and self.process_monitor.is_in_progress('building_shapes', 'extent_clipped'):
                self.clip_zoom_to_layer_view_from_raster(self.investigation_shape_layer_name)
                self.process_monitor.update_progress('building_shapes', 'extent_clipped', True)
                self.process_monitor.update_progress('building_shapes', 'pyramids_built', True)
                LayerInteraction.hide_or_remove_layer(self.clipping_raster_layer_name, 'hide', self.iface)
                LayerInteraction.hide_or_remove_layer('OpenStreetMap', 'hide', self.iface)


        ### Point sampling
        if self.step_queue[next_step] == 'temp_pointlayer_created' and not self.process_monitor.is_in_progress('building_shapes'):
            pst_plugin = self.get_plugin_ifexists(self.pst_plugin_name)
            psti = PstInteraction(pst_plugin, iface)

            if self.process_monitor.is_in_progress('sampling_points', 'temp_pointlayer_created'):
                self.mainstay_process_dlg.go_to_page('sampling_points')
                pst_input_layer = LayerInteraction.create_temporary_layer(self.pst_input_layer_name, 'Point', self.project_crs)
                LayerInteraction.add_layer_to_registry(pst_input_layer)
                self.process_monitor.update_progress('sampling_points', 'temp_pointlayer_created', True)

        if self.step_queue[next_step] == 'editing_temp_pointlayer_started' and not self.process_monitor.is_in_progress('building_shapes'):
            pst_plugin = self.get_plugin_ifexists(self.pst_plugin_name)
            psti = PstInteraction(pst_plugin, iface)

            if self.process_monitor.is_in_progress('sampling_points', 'editing_temp_pointlayer_started') and not self.process_monitor.is_in_progress('sampling_points', 'temp_pointlayer_created'):
                LayerInteraction.trigger_edit_mode(self.iface, self.pst_input_layer_name)
                self.process_monitor.update_progress('sampling_points', 'editing_temp_pointlayer_started', True)

            if self.process_monitor.is_in_progress('sampling_points', 'points_of_interest_defined') and not self.process_monitor.is_in_progress('sampling_points', 'editing_temp_pointlayer_started'):
                self.confirm_selection_of_investigation_area_dlg.set_dialog_text("Click \'OK\' once the sampling points are selected.", "Choose sample points")
                points_selected = self.confirm_selection_of_investigation_area(self.pst_input_layer_name)
                if points_selected:
                    self.process_monitor.update_progress('sampling_points', 'points_of_interest_defined', True)

            if self.process_monitor.is_in_progress('sampling_points', 'editing_temp_pointlayer_stopped') and not self.process_monitor.is_in_progress('sampling_points', 'points_of_interest_defined'):
                LayerInteraction.trigger_edit_mode(self.iface, self.pst_input_layer_name, 'off')
                self.process_monitor.update_progress('sampling_points', 'editing_temp_pointlayer_stopped', True)

        if self.step_queue[next_step] == 'information_sampled' and not self.process_monitor.is_in_progress('building_shapes'):
            pst_plugin = self.get_plugin_ifexists(self.pst_plugin_name)
            psti = PstInteraction(pst_plugin, iface)

            if self.process_monitor.is_in_progress('sampling_points', 'information_sampled') and not self.process_monitor.is_in_progress('sampling_points', 'editing_temp_pointlayer_stopped'):
                psti.set_input_layer(self.pst_input_layer_name)
                psti.select_files_for_sampling()

                pst_output_layer = psti.start_sampling(self.project_path, self.pst_output_layer_name)
                vlayer = QgsVectorLayer(pst_output_layer, unicode('pst_out'), "ogr")
                LayerInteraction.add_layer_to_registry(vlayer)

                self.process_monitor.update_progress('sampling_points', 'information_sampled', True)

    # run method that puts the process in an order
    def run(self):

        self.mainstay_process_dlg.show()

        self.mainstay_process_dlg.process_button_next.clicked.connect(self.start_or_continue_process)

    def run_tests(self):

        test_class = LayerInteraction_test
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(test_class)

        suite = unittest.TestSuite()
        for test_method in test_names:
            suite.addTest(test_class(test_method, self.iface))

        unittest.TextTestRunner(sys.stdout).run(suite)
