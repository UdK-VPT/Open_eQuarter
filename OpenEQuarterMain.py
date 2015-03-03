# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenEQuarterMain
                                 A QGIS plugin
 The plugin automates the setup for investigating an area.
                              -------------------
        begin                : 2014-10-07
        copyright            : (C) 2014 by Kim Gülle / UdK-Berlin
        email                : kimonline@posteo.de
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
from socket import gaierror
import httplib
import unittest

from qgis.core import *
from qgis.utils import iface

from PyQt4.QtGui import *
import numpy

from model.ProgressModel import ProgressModel
from view.InvestigationAreaSelected_dialog import InvestigationAreaSelected_dialog
from view.ProjectDoesNotEexist_dialog import ProjectDoesNotExist_dialog
from view.ProjectSettings_form import ProjectSettings_form
from view.MainProcess_dock import MainProcess_dock
from view.RequestWmsUrl_dialog import RequestWmsUrl_dialog
from view.qt.ui_process_button import QProcessButton
from qgisinteraction.PstInteraction import *
from qgisinteraction.OlInteraction import *
from qgisinteraction import LayerInteraction
from ExportWMSasTif import ExportWMSasTif
from tests.LayerInteraction_test import LayerInteraction_test


class OpenEQuarterMain:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        ### Plugin specific settings
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        ### UI specific settings
        # Create the dialogues (after translation) and keep references
        self.main_process_dock = MainProcess_dock()
        self.oeq_project_settings_form = ProjectSettings_form()

        self.project_does_not_exist_dlg = ProjectDoesNotExist_dialog()
        self.request_wms_url_dlg = RequestWmsUrl_dialog()
        self.wms_url = 'crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k5'
        self.confirm_selection_of_investigation_area_dlg = InvestigationAreaSelected_dialog()


        ### Project specific settings
        # the project path is './' as long as the project has not been saved
        self.project_path = QgsProject.instance().readPath('')
        self.project_crs = 'EPSG:3857'  # ToDo set crs back to 4326
        self.oeq_project = ''


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
        # default extent, after the OSM-layer was loaded (currently: extent of Berlin - Germany)
        self.default_extent = QgsRectangle(numpy.float64(1541791.863584674), numpy.float64(6929650.281509268),
                                           numpy.float64(1434669.8536058515), numpy.float64(6847465.188708487))
        self.default_extent_crs = 'EPSG:3857'
        self.default_scale = 4607478

        # name of the shapefile which will be created to define the investigation area
        self.investigation_shape_layer_name = 'Investigation Area'
        self.investigation_shape_layer_style = os.path.join(self.plugin_dir, 'Styles', 'oeq_ia_style.qml')

        # name of the wms-raster which will be loaded and is the basis for the clipping
        self.clipping_raster_layer_name = 'Investigation Area - raster'

        ### Monitor the users progress
        self.progress_model = ProgressModel()
        # ToDo have step_queue created from the process list in the Processing class
        self.step_queue = ['ol_plugin_installed', 'pst_plugin_installed', 'project_created', 'osm_layer_loaded',
                           'temp_shapefile_created', 'editing_temp_shapefile_started', 'investigation_area_selected',
                           'editing_temp_shapefile_stopped',
                           'raster_loaded', 'extent_clipped', 'pyramids_built',
                           'temp_pointlayer_created', 'editing_temp_pointlayer_started', 'points_of_interest_defined',
                           'editing_temp_pointlayer_stopped', 'information_sampled']

    def initGui(self):

        # Create action that will start plugin configuration
        plugin_icon = QIcon(os.path.join(':/Plugin/Icons/OeQ_plugin_icon.png'))
        self.main_action = QAction(plugin_icon, u"OpenEQuarter-Process", self.iface.mainWindow())
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

        self.main_process_dock.process_button_next.clicked.connect(self.continue_process)
        self.main_process_dock.process_button_auto.clicked.connect(self.auto_run)

        for page in self.main_process_dock.selection_to_page.values():
            for button in page.children():
                if isinstance(button, QProcessButton):
                    self.main_process_dock.connect(button, SIGNAL('process_button_click'), self.process_button_clicked)

        self.main_process_dock.dropdown_menu = QMenu()
        self.main_process_dock.dropdown_menu.addAction('Open project setup..', self.open_settings)
        self.main_process_dock.dropdown_menu.addAction('Save current progress', self.save_progress)
        self.main_process_dock.dropdown_menu.addAction('Save current progress as..', self.save_progress_as)
        self.main_process_dock.dropdown_menu.addAction('Open OeQ-Project..', self.open_progress)

        self.main_process_dock.settings_dropdown_btn.setMenu(self.main_process_dock.dropdown_menu)
        self.main_process_dock.settings_dropdown_btn.setPopupMode(QToolButton.InstantPopup)

    def open_settings(self):
        self.oeq_project_settings_form.show()

    def open_progress(self):
        print 'Open Project'

    def save_progress(self):
        print 'Save progress'

    def save_progress_as(self):
        print 'Save as'

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&OpenEQuarter", self.main_action)
        self.iface.removePluginMenu(u"&OpenEQuarter", self.clipping_action)
        self.iface.removePluginMenu(u"&OpenEQuarter", self.testing_action)
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

            extent = canvas.extent()  # save formerly viewed extent
            current_crs = self.get_project_crs()  # get project-crs
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

        try:
            # set the rasterlayer as active, since only the active layer will be clipped and start the export
            self.iface.setActiveLayer(raster_layer)
            pyramid_exporter = ExportWMSasTif(self.iface)
            return pyramid_exporter.export(raster_layer.name())

        except None as exception:
            print exception
            return None

    def clip_zoom_to_layer_view_from_raster(self, layer_name):
        """
        Zoom to a given vector-layer, containing shape files. Extract the currently viewed extent from an underlying raster-layer into a new .tif and open it.
        :param layer_name: Name of the vector-layer
        :type layer_name: str
        :return:
        :rtype:
        """
        try:
            investigation_shape = LayerInteraction.find_layer_by_name(layer_name)

            # an investigation shape is needed, to trigger the zoom to layer function
            if investigation_shape is not None and investigation_shape.featureCount() > 0:

                # zoom
                self.iface.setActiveLayer(investigation_shape)
                self.iface.actionZoomToLayer().trigger()

                # clip extent from visible raster layers
                # save visible layers and set them invisible afterwards, to prevent further from the wms-server
                raster_layers = LayerInteraction.get_wms_layer_list(self.iface, 'visible')
                for layer in raster_layers:
                    self.iface.legendInterface().setLayerVisible(layer, False)

                clipped_layers = []
                for clipping_raster in raster_layers:
                    clipped_layers.append(self.clip_from_raster(clipping_raster))

                return clipped_layers
        except None as exception:
            print exception
            return None

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
                        extent = QgsRectangle(extent_coordinates[0], extent_coordinates[1], extent_coordinates[2],
                                              extent_coordinates[3])
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
        # ToDo
        return

    def add_housing_coordinates(self):
        # ToDo
        return

    # step 0.0
    def handle_ol_plugin_installed(self):
        return self.get_plugin_ifexists(self.ol_plugin_name) is not None

    # step 0.1
    def handle_pst_plugin_installed(self):
        return self.get_plugin_ifexists(self.pst_plugin_name) is not None

    # step 0.2
    def handle_project_created(self):
        # if no project exists, create one first
        self.create_project_ifNotExists()
        self.project_path = QgsProject.instance().readPath('./')

        # if project was created stop execution
        if self.project_path != './':
            return True
        else:
            return False

    # step 0.3
    def handle_osm_layer_loaded(self):
        if self.osm_layer_is_loaded():
            return True

        else:
            ol_plugin = OlInteraction(self.ol_plugin_name)
        # self.enable_on_the_fly_projection()
        # self.set_project_crs(self.default_extent_crs)

            if ol_plugin.open_osm_layer(self.open_layer_type_id):
                self.zoom_to_default_extent()
                return True

            else:
                return False

    # step 1.0
    def handle_temp_shapefile_created(self):
        investigation_area = LayerInteraction.create_temporary_layer(self.investigation_shape_layer_name, 'Polygon',
                                                                     self.project_crs)

        if investigation_area is not None:
            LayerInteraction.add_style_to_layer(self.investigation_shape_layer_style, investigation_area)
            LayerInteraction.add_layer_to_registry(investigation_area)
            return True
        else:
            return False

    # step 1.1
    def handle_editing_temp_shapefile_started(self):
        LayerInteraction.trigger_edit_mode(self.iface, self.investigation_shape_layer_name)
        return True

    # step 1.2
    def handle_investigation_area_selected(self):
        self.confirm_selection_of_investigation_area_dlg.set_dialog_text(
            "Click 'OK' once the investigatoion area is selected.", "Define investigaion area")
        ia_covered = self.confirm_selection_of_investigation_area(self.investigation_shape_layer_name)
        return ia_covered

    # step 1.3
    def handle_editing_temp_shapefile_stopped(self):
        LayerInteraction.trigger_edit_mode(self.iface, self.investigation_shape_layer_name, 'off')
        return True

    # step 2.0
    def handle_raster_loaded(self):
        # self.request_wms_layer_url()
        investigation_raster_layer = LayerInteraction.open_wms_as_raster(self.iface, self.wms_url,
                                                                         self.clipping_raster_layer_name)

        if investigation_raster_layer is not None and investigation_raster_layer.isValid():
            LayerInteraction.add_layer_to_registry(investigation_raster_layer)
            self.iface.setActiveLayer(investigation_raster_layer)
            return True
        else:
            self.iface.actionAddWmsLayer().trigger()
            return True

    # step 2.1
    def handle_extent_clipped(self):
        extracted_layers = self.clip_zoom_to_layer_view_from_raster(self.investigation_shape_layer_name)
        LayerInteraction.hide_or_remove_layer('OpenStreetMap', 'hide', self.iface)

        for layer_name in extracted_layers:
            try:
                layer = LayerInteraction.find_layer_by_name(layer_name)
                LayerInteraction.gdal_warp_layer_list(layer, self.project_crs)
                path_geo = layer.publicSource()
                path_transformed = path_geo.replace('_geo.tif', '_transformed.tif')

                if os.path.exists(path_transformed):
                    # change validation to surpress missing-crs prompt
                    old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'useProject'))
                    QSettings().setValue('/Projections/defaultBehaviour', 'useProject')

                    LayerInteraction.hide_or_remove_layer(layer_name,'remove',self.iface)

                    rlayer = QgsRasterLayer(path_transformed, layer_name)
                    rlayer.setCrs(QgsCoordinateReferenceSystem(self.project_crs))
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer)
                    os.remove(path_geo)
                    self.iface.mapCanvas().refresh()
                    # restore former settings
                    QSettings().setValue('/Projections/defaultBehaviour', old_validation)
            except (OSError, AttributeError) as Clipping_Error:
                print(Clipping_Error)
                pass

        time.sleep(1.0)
        return True

    # step 2.2
    def handle_pyramids_built(self):
        return True

    # step 3.0
    def handle_temp_pointlayer_created(self):
        pst_input_layer = LayerInteraction.create_temporary_layer(self.pst_input_layer_name, 'Point',
                                                                  self.project_crs)
        LayerInteraction.add_layer_to_registry(pst_input_layer)
        return True

    # step 3.1
    def handle_editing_temp_pointlayer_started(self):
        LayerInteraction.trigger_edit_mode(self.iface, self.pst_input_layer_name)
        return True

    # step 3.2
    def handle_points_of_interest_defined(self):
        self.confirm_selection_of_investigation_area_dlg.set_dialog_text(
            "Click 'OK' once the sampling points are selected.", "Choose sample points")
        points_selected = self.confirm_selection_of_investigation_area(self.pst_input_layer_name)
        return points_selected

    # step 3.3
    def handle_editing_temp_pointlayer_stopped(self):
        LayerInteraction.trigger_edit_mode(self.iface, self.pst_input_layer_name, 'off')
        return True

    # step 3.4
    def handle_information_sampled(self):
        pst_plugin = self.get_plugin_ifexists(self.pst_plugin_name)
        psti = PstInteraction(pst_plugin, iface)

        psti.set_input_layer(self.pst_input_layer_name)
        psti.select_files_for_sampling()

        pst_output_layer = psti.start_sampling(self.project_path, self.pst_output_layer_name)
        vlayer = QgsVectorLayer(pst_output_layer, LayerInteraction.biuniquify_layer_name('pst_out'), "ogr")
        LayerInteraction.add_layer_to_registry(vlayer)
        return True

    def continue_process(self):
        """
        Call the appropriate handle-function, depending on the progress-step, that shall has to be executed next.
        :return:
        :rtype:
        """
        try:
            next_open_step_no = self.progress_model.last_step_executed + 1
            next_open_step = self.progress_model.get_step_list()[next_open_step_no]

            step_page = self.main_process_dock.findChild(QProcessButton, next_open_step + '_chckBox').parent()
            step_section = step_page.objectName()[0:-5]

            if self.progress_model.prerequisites_are_given(next_open_step):
                handler = 'handle_' + next_open_step
                next_call = getattr(self, handler)

                step_completed = next_call()
                self.progress_model.update_progress(step_section, next_open_step, step_completed)
                self.main_process_dock.set_checkbox_on_page(next_open_step + '_chckBox', step_section + '_page', step_completed)

                if self.progress_model.is_section_done(step_section):
                    self.main_process_dock.set_current_page_done(True)
        except IndexError, error:
            print error

    def process_button_clicked(self, *args):
        """
        Call the appropriate handle-function, depending on the objet which triggered the function call.
        :param args: The sender name and the sender object in a list
        :type args: list
        :return:
        :rtype:
        """
        sender_name = args[0]
        sender_object = args[1]
        next_step = sender_name[:-8]

        next_page = sender_object.parent()
        next_section = next_page.objectName()[0:-5]

        # for debugging uncomment the following line
        if True:
        #if self.progress_model.prerequisites_are_given(next_step) or True:
            handler = 'handle_' + next_step
            next_call = getattr(self, handler)

            is_done = next_call()
            self.progress_model.update_progress(next_section, next_step, is_done)
            self.main_process_dock.go_to_page(next_page.accessibleName())
            self.main_process_dock.set_checkbox_on_page(next_step + '_chckBox', next_section + '_page', is_done)

    def run(self):
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.main_process_dock)

        if self.oeq_project == '':
            self.oeq_project_settings_form.show()

        self.check_status()

    def run_tests(self):
        test_class = LayerInteraction_test
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(test_class)

        suite = unittest.TestSuite()
        for test_method in test_names:
            suite.addTest(test_class(test_method, self.iface))

        unittest.TextTestRunner(sys.stdout).run(suite)

    def check_status(self):

        self.continue_process() #OL-Plugin
        self.continue_process() #PST-Plugin
        self.continue_process() #Proje. saved

        investigation_layer = LayerInteraction.find_layer_by_name(self.investigation_shape_layer_name)

        if self.osm_layer_is_loaded() or investigation_layer:
            self.set_next_step_done() # open OL-map

            if investigation_layer:
                self.set_next_step_done() # create shapefile

                if investigation_layer.featureCount() > 0:
                    self.set_next_step_done() # activate edit mode
                    self.set_next_step_done() # confirm selection
                    self.set_next_step_done() # deactivate edit mode

    def set_next_step_done(self):
        try:
            next_open_step_no = self.progress_model.last_step_executed + 1
            next_open_step = self.progress_model.get_step_list()[next_open_step_no]

            step_page = self.main_process_dock.findChild(QProcessButton, next_open_step + '_chckBox').parent()
            step_section = step_page.objectName()[0:-5]

            self.progress_model.update_progress(step_section, next_open_step, True)
            self.main_process_dock.set_checkbox_on_page(next_open_step + '_chckBox', step_section + '_page', True)

            if self.progress_model.is_section_done(step_section):
                self.main_process_dock.set_current_page_done(True)

        except IndexError, error:
                print error




    def auto_run(self):
        steps = self.progress_model.get_step_list()
        next = self.progress_model.last_step_executed

        try:
            for i in range(len(steps)):
                if self.iface.mapCanvas().isDrawing():
                    i - 1
                else:
                    next = self.progress_model.last_step_executed + 1
                    time.sleep(1.5)
                    self.continue_process()
                    i = next

        except IndexError, error:
            print error




