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
import OsmInteraction
import LayerInteraction
from saveselectionwithpyramid import SaveSelectionWithPyramid

from socket import gaierror
import os.path
import numpy
import httplib


class OpenEQuartersMain:

    def __init__(self, iface):

        # Save reference to the QGIS interface
        self.iface = iface

        ### Plugin specific settings
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


        ### UI specific settings
        # Create the dialogues (after translation) and keep references
        self.mainstay_process_dlg = MainstayProcess_dialog()
        self.project_does_not_exist_dlg = ProjectDoesNotExist_dialog()
        self.request_wms_url_dlg = RequestWmsUrl_dialog()
        self.wms_url = ""
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
        self.open_layer_type_id = 1


        ### Default values
        # default extent, after the OSM-layer was loaded (currently: extent of Germany)
        self.default_extent = QgsRectangle(numpy.float64(480310.4063808322), numpy.float64(5930330.009070959), numpy.float64(1813151.46638856), numpy.float64(7245291.493883461))
        self.default_extent_crs = 'EPSG:3857'
        self.default_scale = 4607478

        # name of the shapefile which will be created to define the investigation area
        self.investigation_shape_layer_name = 'Investigation Area'
        self.investigation_shape_layer_style = os.path.join(self.plugin_dir, 'Layerstyle', 'oeq_ia_style.qml')

        # name of the wms-raster which will be loaded and is the basis for the clipping
        self.clipping_raster_layer_name = 'Investigation Area - raster'


        ### Information regarding the users progress
        # list that captures the progress of the oeq-process
        self.progress = {'project_basics': {'ol_plugin_installed': False, 'pst_plugin_installed': False, 'project_created': False, 'osm_layer_loaded': False}}

    def initGui(self):
        # Create action that will start plugin configuration
        plugin_icon = QIcon(os.path.join(self.plugin_dir, 'Icons', 'icon.png'))
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

    def load_osm_layer(self, open_layer_type_id):
        """
        Use the OsmInteraction-methods to interact with the Open-Street-Map plugin and open an open street map according to open_layer_type_id
        :param open_layer_type_id: ID of the open-layer type
        :type open_layer_type_id: int
        :return:
        :rtype:
        """
        # if the plugin is installed under a different name
        if self.ol_plugin_name != 'openlayers_plugin':
            layer_loaded = OsmInteraction.open_osm_layer(open_layer_type_id, self.ol_plugin_name)
        else:
            layer_loaded = OsmInteraction.open_osm_layer(open_layer_type_id)


        if layer_loaded:
            # if current scale is below osm-layers visibility, rescale canvas
            canvas = self.iface.mapCanvas()
            if canvas.scale() < 850:
                canvas.zoomScale(850)
                canvas.refresh()

        return layer_loaded

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
        canvas = self.iface.mapCanvas()

        # if plugin was started out of new or empty project, zoom to default extent
        # !!!!!! A print statement has to be executed prior to calling the layerCount() function
        print ""
        # !!!!!! apparently the layerCount()-function does not flush properly
        if canvas.layerCount() >= 0 and canvas.layerCount() <= 2:
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

    def update_progress(self, section, step, is_done):
        """
        Update the progress dictionary acoording to the section, step and the new value.
        :param section The key related to the oeq-GUI page name:
        :type section str:
        :param step The key related to the oeq-GUI checkbox name:
        :type step str:
        :param is_done Value telling if the step was completed successfully:
        :type is_done bool:
        :return:
        :rtype:
        """
        try:
            self.progress[section][step] = is_done
            self.mainstay_process_dlg.set_checkbox_on_page(step + '_chckBox', section + '_page', is_done)

            if not self.is_in_progress(section):
                self.mainstay_process_dlg.set_progress_button(section + '_btn', True)
        except KeyError, error:
            print str(error)

    def is_in_progress(self, section, *steps):
        """
        Sum the number of steps completed in a given section and compare them against the total amount of steps in that section / Calculate how many of the given steps are still uncompleted.
        :param section The key related to the oeq-GUI page name:
        :type section str:
        :param steps The key(s) related to the oeq-GUI checkbox name:
        :type steps *str:
        :return The amount of uncompleted steps in a section / list of steps. Returns 0 if all steps are completed:
        :rtype int:
        """
        if not section or section.isspace():
            return 0

        if len(steps) == 0:
            steps_in_section = 0
            steps_done = 0

            try:
                for key in self.progress[section]:
                    steps_in_section += 1
                    steps_done += self.progress[section][key]
                return steps_in_section - steps_done
            except KeyError, error:
                print str(error)
                return -1

        else:
            steps_done = 0
            try:
                for step in steps:
                    steps_done += self.progress[section][step]
                return len(steps) - steps_done
            except KeyError, error:
                print str(error)
                return -1



    # run method that puts the process in an order
    def run(self):

        self.mainstay_process_dlg.show()


        if self.get_plugin_ifexists(self.ol_plugin_name) is not None:
            self.update_progress('project_basics', 'ol_plugin_installed', True)


        if self.get_plugin_ifexists(self.pst_plugin_name) is not None:
            self.update_progress('project_basics', 'pst_plugin_installed', True)

        if not self.is_in_progress('project_basics', 'ol_plugin_installed'):
            # if no project exists, create one first
            self.create_project_ifNotExists()
            self.project_path = QgsProject.instance().readPath('./')

            # if project was created stop execution
            if self.project_path != './':
                self.update_progress('project_basics', 'project_created', True)

        if not self.is_in_progress('project_basics','ol_plugin_installed','project_created'):
            self.enable_on_the_fly_projection()
            self.set_project_crs('EPSG:3857')

            if self.osm_layer_is_loaded():
                self.update_progress('project_basics', 'osm_layer_loaded', True)

            elif not self.osm_layer_is_loaded() and self.load_osm_layer(self.open_layer_type_id) is not None:
                self.update_progress('project_basics', 'osm_layer_loaded', True)
                self.zoom_to_default_extent()


        if not self.is_in_progress('project_basics'):
            print 'Continuing with second step'

        """
        self.create_new_shapefile('IA','Polygon')

        # start the process, if a project was created
        else:


                investigation_area = LayerInteraction.create_temporary_layer(self.investigation_shape_layer_name, 'Polygon', self.project_crs)
                LayerInteraction.add_style_to_layer(self.investigation_shape_layer_style, investigation_area)
                LayerInteraction.add_layer_to_registry(investigation_area)

                LayerInteraction.change_to_edit_mode(self.investigation_shape_layer_name)

                self.confirm_selection_of_investigation_area(self.investigation_shape_layer_name)
                #self.request_wms_layer_url()

                self.open_wms_as_raster()

                self.clip_zoom_to_layer_view_from_raster(self.investigation_shape_layer_name, self.clipping_raster_layer_name)
                LayerInteraction.hide_or_remove_layer(self.clipping_raster_layer_name, 'remove')
                LayerInteraction.hide_or_remove_layer("Google Streets", 'hide', self.iface)

                ### Interaction with point sampling tool
                pst_plugin = self.get_plugin_ifexists(self.pst_plugin_name)
                psti = PstInteraction(pst_plugin, iface)

                psti.set_input_layer(self.pst_input_layer_name)
                psti.select_files_for_sampling()

                pst_output_layer = psti.start_sampling(self.pst_output_layer_path, self.pst_output_layer_name)
                vlayer = QgsVectorLayer(pst_output_layer, unicode('pst_out'), "ogr")
                LayerInteraction.add_layer_to_registry(vlayer)
                ###

            else:
                print "OSM-plugin not found"
            """

