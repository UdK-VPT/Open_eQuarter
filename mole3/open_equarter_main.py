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
import time
import os

from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QMenu, QAction, QPushButton, QMessageBox

from qgis.PyQt.QtCore import pyqtSignal, Qt, QSettings, QVariant, QTimer

from qgis.gui import QgsMapToolEmitPoint, QgsMessageBar
from qgis.core import *
#from model.progress_model import ProgressItemsModel
from mole3.view.oeq_dialogs import (
    Modular_dialog, ProjectSettings_form, ProjectDoesNotExist_dialog,
    ColorPicker_dialog, MainProcess_dock, RequestWmsUrl_dialog, InformationSource_dialog)
from mole3.qgisinteraction import (
    plugin_interaction,
    layer_interaction,
    raster_layer_interaction,
    project_interaction,
    wms_utils,
    legend)
from mole3.project import config
from mole3 import workflow as oeq_workflows
from mole3 import oeq_global
                #OeQ_Workflow,OeQ_WorkStep
#print(oeq_workflows)

import inspect
DEBUG_MODE = True



def do_print():
    pass

def isnull(value):
    return type(value) is type(NULL)


class OpenEQuarterMain:
    def __init__(self, iface):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        #from mole3.oeq_workflows import OeQ_Workflow
        # Save reference to the QGIS interface
        self.iface = iface
        ### Monitor the users progress
        #self.progress_items_model = ProgressItemsModel()
        self.initWorkflow()

        #enable on the fly projection
        ##self.iface.mapCanvas().setCrsTransformEnabled(True)
        #self.iface.mapCanvas().mapRenderer().setProjectionsEnabled(True)
        #crsSrc = self.iface.mapCanvas().setDestinationCrs(QgsCoordinateReferenceSystem(config.project_crs))
        #self.iface.mapCanvas().mapRenderer().setDestinationCrs(QgsCoordinateReferenceSystem(int(config.project_crs.split(':')[1]), QgsCoordinateReferenceSystem.EpsgCrsId))

        ### UI specific settings
        # Create the dialogues (after translation) and keep references
        self.oeq_project_settings_form = ProjectSettings_form()
        self.color_picker_dlg = ColorPicker_dialog()
        self.information_source_dlg = InformationSource_dialog()
        self.project_does_not_exist_dlg = ProjectDoesNotExist_dialog()
        self.request_wms_url_dlg = RequestWmsUrl_dialog()
        self.initMainProcessDock()
        self.load_oeq_project()
        self.coordinate_tracker = QgsMapToolEmitPoint(self.iface.mapCanvas())
        #self.wms_url = 'crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k5'
        self.confirm_selection_of_investigation_area_dlg = Modular_dialog()
        #set default coordinate system
        ### Project specific settings
        self.oeq_project = ''

        # OpenStreetMap-plugin-layer
        self.open_layer = None

        # to work flawlessly on the messagebar it is necessary to initialize the Python console once
        self.iface.actionShowPythonDialog().trigger()
        #print "Welcome to Open eQuarter. To support the messagebar it is necessary to open the console once..."
        self.iface.actionShowPythonDialog().trigger()  # in fact it's not show but toggle
        print("Hello this is Open eQuarter")

    def new_project(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        #self.progress_items_model.load_section_models(config.progress_model)
        #self.main_process_dock.process_button_next.clicked.connect(self.continue_process)
        #sections = self.progress_items_model.section_views

        #for list_view in sections:
        #    list_view.clicked.connect(self.process_button_clicked)

        import copy

        oeq_global.OeQ_project_info = copy.deepcopy(config.pinfo_default)
        self.update_workstep_states_in_Gui()


    def initGui(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from qgis.core import QgsProject
        project =QgsProject.instance()
        plugin_icon = QIcon(os.path.join(':', oeq_global.OeQ_plugin_path(), 'icons', 'OeQ_plugin_icon.png'))
        self.main_action = QAction(plugin_icon, "OpenEQuarter-Process", self.iface.mainWindow())
        self.main_action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.main_action)
        self.iface.addPluginToMenu("&OpenEQuarter", self.main_action)

        clipping_icon = QIcon(os.path.join(':', 'Plugin', 'icons', 'scissor.png'))
        self.clipping_action = QAction(clipping_icon, "Extract extent from active WMS", self.iface.mainWindow())
        self.clipping_action.triggered.connect(lambda: self.clip_from_raster(self.iface.activeLayer()))
        self.iface.addToolBarIcon(self.clipping_action)
        self.iface.addPluginToMenu("&OpenEQuarter", self.clipping_action)
        self.iface.projectRead.connect(self.load_oeq_project)
        self.iface.newProjectCreated.connect(self.new_project)
        project.projectSaved.connect(self.save_oeq_project)

        #self.initGui_process_dock()

    def initMainProcessDock(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        self.main_process_dock = MainProcess_dock(self) #self.progress_items_model)
        #self.main_process_dock.process_button_next.clicked.connect(self.continue_process)
        #sections = self.progress_items_model.section_views
        #for list_view in sections:
        #    list_view.clicked.connect(self.process_button_clicked)

        settings_dropdown_menu = QMenu()
        config_icon = QIcon(os.path.join(':', 'Controls', 'icons', 'config.png'))
        open_icon = QIcon(os.path.join(':', 'Controls', 'icons', 'open.png'))
        sources_icon = QIcon(os.path.join(':', 'Controls', 'icons', 'sources.png'))
        settings_dropdown_menu.addAction(config_icon, 'Project configuration..', self.open_settings)
        settings_dropdown_menu.addAction(open_icon, 'Open OeQ-Project..', self.launch_oeq)
        settings_dropdown_menu.addAction(sources_icon, 'Open source configuration..', self.information_source_dlg.exec_)

        tools_dropdown_menu = QMenu()
        tools_dropdown_menu.addAction('Color Picker', self.prepare_color_picker)
        tools_dropdown_menu.addAction('Load layer from WMS', self.load_wms)
        tools_dropdown_menu.addAction('Save extent as image',
                                      #lambda: wms_utils.save_wms_extent_as_image(self.iface.activeLayer().name()))
                                      lambda: wms_utils.wms_saveCanvasExtent(self.iface.activeLayer().name()))
        #tools_dropdown_menu.addAction('Calculate Energy Demand', self.handle_building_calculations)

        self.main_process_dock.tools_dropdown_btn.setMenu(tools_dropdown_menu)
        self.main_process_dock.settings_dropdown_btn.setMenu(settings_dropdown_menu)

    def initWorkflow(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import workflow as wf

        self.standard_workflow=wf.OeQ_Workflow('OeQ_standard','Standard Workflow of Open eQuarter')
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('ol_plugin_installed', 'Check if the Openlayers Plugin exists', self.handle_ol_plugin_installed, self.check_if_ol_plugin_installed))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('pst_plugin_installed', 'Check if the Pointsampling Tool Plugin exists', self.handle_pst_plugin_installed, self.check_if_pst_plugin_installed))

        #self.standard_workflow.register_workstep(oeq_workflows.OeQ_WorkStep('real_centroid_plugin_installed', 'Check if the Reacentroid Plugin exists', self.handle_real_centroid_plugin_installed, self.check_if_real_centroid_plugin_installed))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('project_created', 'Create a Project', self.handle_project_created, self.check_if_project_created))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('project_saved', 'Save the Project', self.handle_project_saved, self.check_if_project_saved))
        self.standard_workflow.register_workstep(
            wf.OeQ_WorkStep('osm_opened', 'Open the OSM-Layer', self.handle_open_osm_layer_loaded,
                                       self.check_if_osm_layer_is_loaded))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('investigationarea_defined', 'Define Investigation Area', self.define_investigationarea, self.investigationarea_defined))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('building_outlines_acquired', 'Get building outlines', self.acquire_building_outlines, self.building_outlines_acquired))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('building_coordinates_acquired', 'Get building coordinates', self.acquire_building_coordinates, self.building_coordinates_acquired))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('information_layers_loaded', 'Load information layers', self.acquire_information_layers, self.information_layers_acquired))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('needle_request_done', 'Perform Needle Request', self.perform_needle_request, self.needle_request_performed))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('database_created', 'Create Building Database', self.create_database, self.database_created))
        self.standard_workflow.register_workstep(wf.OeQ_WorkStep('buildings_evaluated', 'Do all Building Evaluations', self.evaluate_buildings, self.buildings_evaluated))
        self.standard_workflow.append_workstep('ol_plugin_installed')
        self.standard_workflow.append_workstep('pst_plugin_installed')
        self.standard_workflow.append_workstep('real_centroid_plugin_installed')
        self.standard_workflow.append_workstep('project_created')
        self.standard_workflow.append_workstep('project_saved')
        self.standard_workflow.append_workstep('investigationarea_defined')
        self.standard_workflow.append_workstep('building_outlines_acquired')
        self.standard_workflow.append_workstep('building_coordinates_acquired')
        self.standard_workflow.append_workstep('information_layers_loaded')
        self.standard_workflow.append_workstep('needle_request_done')
        self.standard_workflow.append_workstep('database_created')
        self.standard_workflow.append_workstep('buildings_evaluated')
        #OeQ_Init_Workflows(self)



    def reorder_layers(self):
        """
        Reorder the layers so that they are ordered (from top to bottom) as follows:
            1. investigation_area
            2. housing_coordinate_layer
            3. housing_layer
        :return:
        :rtype:
        """
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        root_node = QgsProject.instance().layerTreeRoot()
        legend.nodeMove(config.investigation_shape_layer_name,'top',root_node)
        legend.nodeMove(config.building_coordinate_layer_name, 1, root_node)
        legend.nodeMove(config.building_outline_layer_name, 2, root_node)
        legend.nodeMove(config.open_layers_layer_name,'bottom',root_node)



    def open_settings(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        self.oeq_project_settings_form.show()
        save = self.oeq_project_settings_form.exec_()
        if save:
            self.handle_project_created()
        #self.run()
        #self.oeq_project_settings_form.show()

    def launch_oeq(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        progress = os.path.join(oeq_global.OeQ_project_path(), oeq_global.OeQ_project_name() + '.oeq')
        #if os.path.isfile(progress):
        #    self.progress_items_model.load_section_models(progress)
        #else:
        #    self.progress_items_model.load_section_models(config.progress_model)
        if self.main_process_dock.isVisible():
            self.main_process_dock.setVisible(False)
        self.initMainProcessDock()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.main_process_dock)
        self.update_workstep_states_in_Gui()
        self.main_process_dock.switch_to_next_worksteps_page(self)


    def load_wms(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        #print('Load wms')
        pass

    def handle_canvas_click(self, point, button):
        """
        Handle a user's click on the map-canvas.
        :param point: Coordinates of the point which was clicked
        :type point: QgsPoint
        :param button: The (mouse-)button which triggered the signal
        :type button: Qt::MouseButton
        :return:
        :rtype:
        """
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        canvas = self.iface.mapCanvas()
        crs = canvas.mapRenderer().destinationCrs()
        raster = oeq_global.QeQ_current_work_layer

        if raster is not None:
            color = raster_layer_interaction.extract_color_at_point(raster, point, crs)

            if isinstance(color, QColor):
                self.color_picker_dlg.add_color(color)

    def unload(self):
        """
        Called, when the plugin is uninstalled to remove the plugin menu item and icons
        :return:
        :rtype:
        """
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from qgis.core import QgsProject
        project =QgsProject.instance()
        self.iface.removePluginMenu("&OpenEQuarter", self.main_action)
        self.iface.removePluginMenu("&OpenEQuarter", self.clipping_action)
        self.iface.removeToolBarIcon(self.main_action)
        self.iface.removeToolBarIcon(self.clipping_action)
        self.iface.projectRead.disconnect(self.load_oeq_project)
        self.iface.newProjectCreated.disconnect(self.new_project)
        project.projectSaved.disconnect(self.save_oeq_project)

    def create_project_ifNotExists(self):
        """
        If the current workspace has not been saved as a project, prompt the user to "Save As..." project
        :return:
        :rtype:
        """

        from mole3 import oeq_global
        from qgis.PyQt.QtWidgets import QFileDialog,QMessageBox
        import shutil
        import os
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        #QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(config.project_crs))
        print("###Marke -2")
        if not project_interaction.project_exists():

            # prompt the user to save the project
            self.project_does_not_exist_dlg.show()


            # check if a custom project name is defined, otherwise use adress informnation as name
            if oeq_global.OeQ_project_info['project_name'] == config.pinfo_default['project_name']:
                oeq_global.OeQ_project_info['project_name'] = ' '.join([oeq_global.OeQ_project_info['location_city'],oeq_global.OeQ_project_info['location_postal'],oeq_global.OeQ_project_info['location_street']])
                oeq_global.OeQ_project_info['project_name'] = oeq_global.fix_german_umlauts('_'.join(oeq_global.OeQ_project_info['project_name'].split(' ')))
            print("###Marke -1")
            yes_to_save = self.project_does_not_exist_dlg.exec_()
            if yes_to_save:
                print("###Marke 0")
                project_dir = QFileDialog.getSaveFileName(None, "Save project'" + oeq_global.OeQ_project_info['project_name'] + "' as:",
                                                          os.path.join(os.path.expanduser(oeq_global.OeQ_project_path()), oeq_global.OeQ_project_info['project_name'].replace(" ", "_")),
                                                          oeq_global.OeQ_project_info['project_name'])[0]

                print("###Marke 1",project_dir)
                if project_dir:
                    print("###Marke 2")
                    #print(project_dir)
                    oeq_global.OeQ_project_info['project_name'] = os.path.basename(project_dir).replace (" ", "_")
                    project_file = oeq_global.OeQ_project_info['project_name']+'.qgs'
                    print("###Marke 3")
                    if os.path.exists(project_dir):
                        if [i.endswith('.qgs') for i in os.listdir(project_dir)]:
                            ask=QMessageBox()
                            reply = ask.question(ask, 'Open eQuarter Alert', "Project seems to exist! Do you want to overwrite?", ask.Yes | ask.No, ask.No)
                            if reply == ask.No: return False
                        else:
                            ask=QMessageBox()
                            ask.question(ask, 'Open eQuarter Alert', "Directory exists, but does not contain a QGIS project! \n Do you want to overwrite?", ask.Yes | ask.No, ask.No)
                            reply = ask.question(ask, 'Open eQuarter Alert',
                                                 "Project Directory seems to exist! Do you want to overwrite?", ask.Yes | ask.No,
                                                 ask.No)
                            if reply == ask.No: return False
                        shutil.rmtree(project_dir, ignore_errors=True)
                    print("###Marke 4")
                    os.makedirs(project_dir)
                    print("###Marke 5")
                    print(os.path.join(project_dir,project_file))

                    QgsProject.instance().setFileName(os.path.join(project_dir,project_file))
                    print("###Marke 6")
                    #print (QgsProject.instance().fileName())
                    self.iface.actionSaveProject().trigger()
                    print("###Marke 7")
                    return True
        return False

    def handle_open_osm_layer_loaded(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        if not self.check_if_osm_layer_is_loaded():
            ol_plugin = plugin_interaction.OlInteraction(config.ol_plugin_name)

            ol_plugin.open_osm_layer(config.open_layer_type_id)
        self.iface.mapCanvas().renderComplete.connect(self.zoom_to_default_extent)
        return True

    def check_if_osm_layer_is_loaded(self):
        """
        Iterate over all layers and check if an osm plugin-layer exists.
        :return True if the layer is available:
        :rtype bool:
        """
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3.qgisinteraction.legend import nodeExists
        if nodeExists(config.open_layers_layer_name):
            return True
        return False

    def zoom_to_default_extent(self):
        """
        Set the extent of the open layer to the default extent and scale specified as in config.default_extent and self.default_scale
        :return:
        :rtype:
        """
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        canvas = self.iface.mapCanvas()
        if (not oeq_global.OeQ_project_info['location_lon']) | (not  oeq_global.OeQ_project_info['location_lat']):
            x = config.default_latitude
            y=config.default_longitude
            scale = config.default_offset
            source_crs = QgsCoordinateReferenceSystem(config.default_crs)
        else:
            x = float(oeq_global.OeQ_project_info['location_lon'])
            y = float(oeq_global.OeQ_project_info['location_lat'])
            scale = config.default_offset
            source_crs = QgsCoordinateReferenceSystem(oeq_global.OeQ_project_info['location_crs'])
        extent = QgsRectangle(x - scale, y - scale, x + scale, y + scale)
        map_crs = QgsProject.instance().crs()
        transformer = QgsCoordinateTransform(source_crs, map_crs, QgsProject.instance()).transform
        extent = transformer(extent)
        if (canvas.extent().xMinimum() == extent.xMinimum()) & (canvas.extent().width() == extent.width()) | (canvas.extent().yMinimum() == extent.yMinimum()) & (canvas.extent().height() == extent.height()):
            canvas.renderComplete.disconnect(self.zoom_to_default_extent)
        canvas.setExtent(extent)
        canvas.refresh()
        return(True)
    '''
    def set_project_crsx(self, crs):
        """
        Set the project crs to the given crs and do a re-projection to keep the currently viewed extent focused
        :param crs: The new crs to set the project to
        :type crs: str
        :return:
        :rtype:
        """
        # if the given crs is valid
        if not crs.isspace() and QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.EpsgCrsId):

            canvas = self.iface.mapCanvas()

            extent = canvas.extent()  # save formerly viewed extent
            current_crs = self.get_project_crs()  # get project-crs
            current_scale = canvas.scale()

            renderer = canvas.mapRenderer()
            new_crs = QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.EpsgCrsId)
            renderer.setDestinationCrs(new_crs)

            canvas.zoomScale(current_scale)

            if not current_crs == new_crs:
                # set extent, by transforming the formerly saved extent to new Projection
                coord_transformer = QgsCoordinateTransform(current_crs, new_crs, QgsProject.instance())
                extent = coord_transformer.transform(extent)

            canvas.setExtent(extent)
            canvas.refresh()
    '''

    def get_project_crs(self):
        """
        Return the project crs
        :return: The project crs
        :rtype: QgsCoordinateReferenceSystem
        """
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        canvas = self.iface.mapCanvas()
        crs = canvas.destinationCrs()

        return crs

    def clip_from_raster(self, raster_layer):
        """
        Clip the current extent from the given raster-layer
        :param raster_layer: The raster-layer which will be clipped
        :type raster_layer: QgsRasterLayer
        :return:
        :rtype:
        """
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        try:
            # set the rasterlayer as active, since only the active layer will be clipped and start the exp
            self.iface.setActiveLayer(raster_layer)
            #geo_export_path = wms_utils.save_wms_extent_as_image(raster_layer.name())
            geo_export_path = wms_utils.wms_saveCanvasExtent(raster_layer.name())
            pyramids_built = raster_layer_interaction.gdal_addo_layerfile(geo_export_path, 'gauss', 6)
            if pyramids_built != 0:
                print(('Error number {} occured, while building pyramids.'.format(pyramids_built)))
        except AttributeError as NoneException:
            print((inspect.currentframe().f_code.co_name, NoneException))
            return None

        filename = geo_export_path.split(os.path.sep)[-1]
        filename = os.path.splitext(filename)[0]
        no_timeout = 50
        while not os.path.exists(geo_export_path) and no_timeout:
            time.sleep(0.1)
            no_timeout -= 1

        raster_layer = QgsRasterLayer(geo_export_path, filename)

        # if the crs is invalid, prompt the user to define an CRS
        if not raster_layer.crs().authid():
            old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'prompt'))
            QSettings().setValue('/Projections/defaultBehaviour', 'prompt')
            layer_interaction.add_layer_to_registry(raster_layer)
            QSettings().setValue('/Projections/defaultBehaviour', old_validation)
        else:
            old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'useProject'))
            QSettings().setValue('/Projections/defaultBehaviour', 'useProject')
            layer_interaction.add_layer_to_registry(raster_layer)
            QSettings().setValue('/Projections/defaultBehaviour', old_validation)

        return raster_layer.name()

    # step 0.0
    def handle_ol_plugin_installed(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.ol_plugin_name)
        if plugin_exists:
            self.main_process_dock.ol_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.ol_plugin_installed.setChecked(False)
            return False

    def check_if_ol_plugin_installed(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.ol_plugin_name)
        if plugin_exists:
            self.main_process_dock.ol_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.ol_plugin_installed.setChecked(False)
            return False

    # step 0.1
    def handle_pst_plugin_installed(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.pst_plugin_name)
        if plugin_exists:
            self.main_process_dock.pst_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.pst_plugin_installed.setChecked(False)
            return False

    def check_if_pst_plugin_installed(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.pst_plugin_name)
        if plugin_exists:
            self.main_process_dock.pst_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.pst_plugin_installed.setChecked(False)
            return False

    # step 0.2
    def handle_real_centroid_plugin_installed(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.real_centroid_plugin_name)
        if plugin_exists:
            self.main_process_dock.real_centroid_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.real_centroid_plugin_installed.setChecked(False)
            return False

    def check_if_real_centroid_plugin_installed(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.real_centroid_plugin_name)
        if plugin_exists:
            self.main_process_dock.real_centroid_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.real_centroid_plugin_installed.setChecked(False)
            return False

    # step 0.3
    def handle_project_created(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        #set project crs to default
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(config.project_crs))
        self.iface.mapCanvas().refresh()
        oeq_global.OeQ_pop_status()
        self.oeq_project_settings_form.show()
        save = self.oeq_project_settings_form.exec_()
        if save:
            self.main_process_dock.project_created.setChecked(True)
            #self.handle_project_saved()
        else:
            self.main_process_dock.project_created.setChecked(False)
        result = self.main_process_dock.project_created.isChecked()
        if result:
            oeq_global.OeQ_push_status(message="Project was succesfully created!")
        else:
            oeq_global.OeQ_push_status(message="Could not create Project!")
        return result


    def check_if_project_created(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        if bool(oeq_global.OeQ_project_info['location_city']) & bool(oeq_global.OeQ_project_info['location_lon']):
            self.main_process_dock.project_created.setChecked(True)
        else:
            self.main_process_dock.project_created.setChecked(False)
        return self.main_process_dock.project_created.isChecked()



    def handle_project_saved(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import extensions
        #extensions.load_defaults()
        #print((oeq_global.OeQ_project_info))
        oeq_global.OeQ_pop_status()
        self.create_project_ifNotExists()
        if oeq_global.OeQ_project_saved():
            extensions.copy_extensions_to_project()
            self.main_process_dock.project_saved.setChecked(True)
        else:
            self.main_process_dock.project_saved.setChecked(False)
        result = self.main_process_dock.project_saved.isChecked()
        if result:
            oeq_global.OeQ_push_status(message="Project was succesfully saved!")
        else:
            oeq_global.OeQ_push_status(message="Could not save Project!")
        return result


    def check_if_project_saved(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        if oeq_global.OeQ_project_saved():
            self.main_process_dock.project_saved.setChecked(True)
        else:
            self.main_process_dock.project_saved.setChecked(False)
        return self.main_process_dock.project_saved.isChecked()




    # step 1.0
    def define_investigationarea(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from qgis.PyQt.QtCore import QEventLoop
        from qgis.gui import QgsMessageBar
        oeq_global.OeQ_pop_status()
        result = False
        self.handle_open_osm_layer_loaded()
        if not self.standard_workflow.all_mandatory_worksteps_done('investigationarea_defined'):
            self.main_process_dock.investigationarea_defined.setChecked(False)
            return False
        loop = QEventLoop()
        confirmed = [False]
        try:
            from qgis.PyQt.QtCore import QString
        except ImportError:
            # we are using Python3 so QString is not defined
            QString = type("")
        # remove if necessary
        legend.nodeCommit(config.investigation_shape_layer_name)
        #layer_interaction.trigger_edit_mode(self.iface, config.investigation_shape_layer_name, 'off')
        legend.nodeRemove(config.investigation_shape_layer_name,True)
        #layer_interaction.fullRemove(config.investigation_shape_layer_name)
        oeq_global.QeQ_disableDialogAfterAddingFeature()
        investigation_area = layer_interaction.create_temporary_layer(config.investigation_shape_layer_name, 'Polygon', config.project_crs)
        if investigation_area is not None:
            investigation_area.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', config.investigation_shape_layer_style))
            layer_interaction.trigger_edit_mode(self.iface, config.investigation_shape_layer_name)
            legend.nodeSetActive(config.investigation_shape_layer_name)
            widget = self.iface.messageBar().createMessage('Cover Investigation Area',
                                                           'Click "Done" once the investigation area is completely covered.')
            button = QPushButton(widget)
            button.setText('Done')
            button.released.connect(lambda: self.confirm_selection_of_investigation_area(loop.quit,confirmed))
            button.destroyed.connect(loop.quit)
            widget.layout().addWidget(button)
            baritem=self.iface.messageBar().pushWidget(widget, Qgis.Warning,duration = 3600)
            legend.nodeByName(config.investigation_shape_layer_name)[0].layer().triggerRepaint()
            self.zoom_to_default_extent()
            legend.nodeByName(config.investigation_shape_layer_name)[0].layer().triggerRepaint()
            loop.exec_()
            legend.nodeCommit(config.investigation_shape_layer_name)
            #layer_interaction.trigger_edit_mode(self.iface, config.investigation_shape_layer_name, 'off')
            oeq_global.QeQ_enableDialogAfterAddingFeature()
            oeq_global.OeQ_pop_warning(baritem)
            if confirmed[0]:
                if legend.nodeExists(config.investigation_shape_layer_name):
                    investigation_area_node=legend.nodeByName(config.investigation_shape_layer_name)
                    if investigation_area_node:
                        investigation_area_node=investigation_area_node[0]
                        if investigation_area_node.layer().featureCount():
                            legend.nodeZoomTo(config.investigation_shape_layer_name)
                            legend.nodeHide(config.open_layers_layer_name)
                            self.main_process_dock.investigationarea_defined.setChecked(True)
                            result = self.main_process_dock.investigationarea_defined.isChecked()
            else:
                legend.nodeRemove(config.investigation_shape_layer_name, True)
                #layer_interaction.fullRemove(config.investigation_shape_layer_name)
                self.main_process_dock.investigationarea_defined.setChecked(False)

            result = self.main_process_dock.investigationarea_defined.isChecked()

            if result:
                oeq_global.OeQ_push_status(message="Investigation Area was succesfully defined!")
            else:
                oeq_global.OeQ_push_status(message="Investigation Area definition failed!")
            return result



    def confirm_selection_of_investigation_area(self,loop_quit,confirmed):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        #from mole3 import oeq_global
        #from mole3.qgisinteraction import legend
        confirmed[0]=True
        loop_quit()
        return True






    def investigationarea_defined(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3.project import config
        if legend.nodeExists(config.investigation_shape_layer_name):
            self.main_process_dock.investigationarea_defined.setChecked(True)
        else:
            self.main_process_dock.investigationarea_defined.setChecked(False)
        return self.main_process_dock.investigationarea_defined.isChecked()


    # step 2.0
    def handle_import_ext_selected(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        if not self.standard_workflow.all_mandatory_worksteps_done('import_ext_selected'):
            self.main_process_dock.import_ext_selected.setChecked(False)
            return False
        done = self.information_source_dlg.exec_()
        if done:
            self.main_process_dock.import_ext_selected.setChecked(True)
            self.iface.actionSaveProject().trigger()
        else:
            self.main_process_dock.import_ext_selected.setChecked(False)
        return self.main_process_dock.import_ext_selected.isChecked()

    def check_if_import_ext_selected(self):
        from mole3.project import config
        return self.main_process_dock.import_ext_selected.isChecked()



    # step 2.1
    def acquire_building_outlines(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import extensions
        from mole3 import oeq_global
        from mole3.qgisinteraction import legend
        from mole3.project import config
        oeq_global.OeQ_pop_status()
        if not self.standard_workflow.all_mandatory_worksteps_done('building_outlines_acquired'):
            self.main_process_dock.building_outlines_acquired.setChecked(False)
            return False
        #self.iface.mapCanvas().freeze()
        legend.nodeHide(config.open_layers_layer_name)
        legend.nodeZoomTo(config.investigation_shape_layer_name)
        building_outline_ext=extensions.by_layername(config.building_outline_layer_name, active=True)
        if not building_outline_ext:
            oeq_global.OeQ_push_warning("No import extension for Building Outlines", "Load geometries or define them on a new Vectorlayer named '" + config.building_outline_layer_name + "' !")
            self.main_process_dock.building_outlines_acquired.setChecked(False)
            return False

        building_outline_ext = building_outline_ext[0]
        building_outline_ext.process()

        building_outlines=legend.nodeByName(config.building_outline_layer_name)
        if not building_outlines:
            self.main_process_dock.building_outlines_acquired.setChecked(False)
            return False

        self.reorder_layers()
        self.main_process_dock.building_outlines_acquired.setChecked(True)
        self.standard_workflow.do_workstep('building_coordinates_acquired')
        result = self.main_process_dock.building_outlines_acquired.isChecked()
        if result:
            oeq_global.OeQ_push_status(message="Building Outlines succesfully aquired!")
            self.iface.actionSaveProject().trigger()
        else:
            oeq_global.OeQ_push_status(message="Could not aquire Building Outlines!")
        return result

    def building_outlines_acquired(self):
            if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
            from mole3.project import config
            if legend.nodeExists(config.building_outline_layer_name):
                self.main_process_dock.building_outlines_acquired.setChecked(True)
            else:
                self.main_process_dock.building_outlines_acquired.setChecked(False)
            return self.main_process_dock.building_outlines_acquired.isChecked()


    # step 2.2
    def handle_building_coordinates_acquired(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import extensions
        from mole3 import oeq_global
        from mole3.qgisinteraction import legend
        from qgis.core import QgsCoordinateReferenceSystem
        window = self.iface.mainWindow()
        #legend.nodeZoomTo(config.investigation_shape_layer_name)
        #oeq_global.OeQ_unlockQgis()
        oeq_global.OeQ_pop_status()
        if not self.standard_workflow.all_mandatory_worksteps_done('building_coordinates_acquired'):
            self.main_process_dock.building_coordinates_acquired.setChecked(False)
            return False
        building_coordinate_ext = extensions.by_layername(config.building_coordinate_layer_name, active=True)
        if not building_coordinate_ext:
            oeq_global.OeQ_push_warning("No import extension for Building Outlines",
                                        "Load geometries or define them on a new Vectorlayer named '" + config.building_coordinate_layer_name + "' !")
            self.main_process_dock.building_coordinates_acquired.setChecked(False)
            return False
        building_coordinate_ext[0].process()

        building_coordinates = legend.nodeByName(config.building_coordinate_layer_name)
        if not building_coordinates:
            self.main_process_dock.building_coordinates_acquired.setChecked(False)
            return False


        self.reorder_layers()
        self.main_process_dock.building_coordinates_acquired.setChecked(True)
        result = self.main_process_dock.building_coordinates_acquired.isChecked()
        if result:
            oeq_global.OeQ_push_status(message="Building Coordinates succesfully aquired!")
            self.iface.actionSaveProject().trigger()
        else:
            oeq_global.OeQ_push_status(message="Could not aquire Building Coordinates!")
        return result



    def building_coordinates_acquired(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3.project import config
        if legend.nodeExists(config.building_coordinate_layer_name):
            self.main_process_dock.building_coordinates_acquired.setChecked(True)
        else:
            self.main_process_dock.building_coordinates_acquired.setChecked(False)
        return self.main_process_dock.building_coordinates_acquired.isChecked()

    def acquire_information_layers(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import extensions
        from mole3.project import config
        from mole3.qgisinteraction import legend
        oeq_global.OeQ_pop_status()
        if not self.standard_workflow.all_mandatory_worksteps_done('information_layers_loaded'):
            self.main_process_dock.information_layers_loaded.setChecked(False)
            return False
        legend.nodeZoomTo(config.investigation_shape_layer_name)

        for i in extensions.by_extension_type("information",active=True):
            i.load()
            i.preflight()
            legend.nodeHide(i.layer_name)
            #return True
        #for i in extensions.by_type('wfs',category='Import',active=True):
        #    i.load_wfs()
        #    #return True
        if all([legend.nodeExists(i.layer_name) for i in extensions.by_state(True,'Import')]):
            self.main_process_dock.information_layers_loaded.setChecked(True)
        else:
            self.main_process_dock.information_layers_loaded.setChecked(False)
        self.reorder_layers()
        self.standard_workflow.do_workstep('needle_request_done')
        self.standard_workflow.do_workstep('database_created')

        result = self.main_process_dock.information_layers_loaded.isChecked()
        if result:
            oeq_global.OeQ_push_status(message="All Information Layers succesfully aquired!")
            self.iface.actionSaveProject().trigger()
        else:
            oeq_global.OeQ_push_status(message="Could not aquire all Information Layers!")
        return result


    def information_layers_acquired(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import extensions
        from mole3.qgisinteraction import legend

        infolayernames = extensions.by_state(True,'Import')
        if (len(infolayernames) > 0) & all([legend.nodeExists(i.layer_name) for i in infolayernames]):
            self.main_process_dock.information_layers_loaded.setChecked(True)
            self.iface.actionSaveProject().trigger()
        else:
            self.main_process_dock.information_layers_loaded.setChecked(False)

        return self.main_process_dock.information_layers_loaded.isChecked()



    def pick_color(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        self.coordinate_tracker.canvasClicked.connect(self.handle_canvas_click)
        self.iface.mapCanvas().setMapTool(self.coordinate_tracker)

    def prepare_color_picker(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        self.pick_color()
        self.color_picker_dlg.start_colorpicking.clicked.connect(self.pick_color)
        save_or_abort = self.color_picker_dlg.exec_()

        success = True
        lvm = self.color_picker_dlg.color_entry_manager.layer_values_map
        for legend in list(lvm.values()):
            legend_available = legend is not None
            success = success and legend_available

        self.iface.actionPan().trigger()
        if success:

            return True
        else:
            self.reorder_layers()
            return 1

    # step
    def acquire_building_coordinates(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        """ generate points on surface """
        vlayer = legend.nodeByName(config.building_outline_layer_name)[0].layer()
        #print('Layer',vlayer.name())
        vprovider = vlayer.dataProvider()
        writer = QgsVectorFileWriter(os.path.join(oeq_global.OeQ_project_path(),config.building_coordinate_layer_name), "CP1250", vprovider.fields(), QgsWkbTypes.Point, vlayer.crs(),"ESRI Shapefile")
        outFeat = QgsFeature()
        features = vlayer.getFeatures()
        nElement = 0
        nError = 0
        for inFeat in features:
            nElement += 1
            inGeom = inFeat.geometry()
            if inGeom is None or not inFeat.hasGeometry() or \
               not inGeom.isGeosValid():
                QgsMessageLog.logMessage("Feature %d skipped (empty or invalid geometry)" % nElement, 'realcentroid')
                nError += 1
                continue
            if inGeom.isMultipart():
                # find largest part in case of multipart
                maxarea = 0
                #tmpGeom = QgsGeometry()
                for part in inGeom.asGeometryCollection():
                    area = part.area()
                    if area > maxarea:
                        tmpGeom = part
                        maxarea = area
                inGeom = tmpGeom
            atMap = inFeat.attributes()
            outGeom = inGeom.pointOnSurface()
            outFeat.setAttributes(atMap)
            outFeat.setGeometry(outGeom)
            writer.addFeature(outFeat)
        del writer
        if nError > 0:
            QMessageBox.warning(None, "RealCentroid", "Invalid or empty geometries found, see log messages")
        # add centroid shape to canvas

        w = QgsVectorLayer(os.path.join(oeq_global.OeQ_project_path(),config.building_coordinate_layer_name+'.shp'), config.building_coordinate_layer_name, 'ogr')
        if w.isValid():
            QgsProject.instance().addMapLayer(w)
        else:
            QMessageBox.warning(None, "RealCentroid", "Error loading shapefile\n" + config.building_coordinate_layer_name)
        return(True)

    # step 4.1
    def perform_needle_request(self):                #DOES NOT CAPTURE WFS!
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        self.main_process_dock.needle_request_done.setChecked(True)
        return self.main_process_dock.needle_request_done.isChecked()

    def needle_request_performed(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        self.main_process_dock.needle_request_done.setChecked(True)
        return self.main_process_dock.needle_request_done.isChecked()

    def create_database(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import extensions
        from mole3.qgisinteraction import legend
        baritem=oeq_global.OeQ_push_info('Create Database:', 'Generating building records... be patient!')
        #extensions.by_layername(config.building_outline_layer_name)[0].createDatabase()
        #result= bool(legend.nodeCreateDatabase(config.building_outline_layer_name, config.data_layer_name, config.project_crs, True, "Data"))
        #if result:
         #   for i in extensions.by_state(True,'Evaluation'):
         #       i.reset_calculation_state()
        self.reorder_layers()
        oeq_global.OeQ_pop_info(baritem)
        return True

    def database_created(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3.project import config
        if legend.nodeExists(config.data_layer_name):
            self.main_process_dock.database_created.setChecked(True)
        else:
            self.main_process_dock.database_created.setChecked(False)
        return self.main_process_dock.database_created.isChecked()

    # step 4.2
        # step 4.1
    def evaluate_buildings(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import extensions
        oeq_global.OeQ_pop_status()
        #oeq_global.OeQ_wait_for_renderer()
        baritem=oeq_global.OeQ_push_info('Extension "Building Evaluation":', 'Checking dependencies... be patient!')
        for i in extensions.by_type('information',active=True,):
            i.process()
            self.iface.actionSaveProject().trigger()
        for i in extensions.by_state(True,'Import'):
            i.process()
            self.iface.actionSaveProject().trigger()
        #extensions.run_active_extensions('Import')
        for i in extensions.by_state(True,'Evaluation'):
            i.process()
            self.iface.actionSaveProject().trigger()
        #extensions.run_active_extensions('Evaluation')
        #import_layer_names = filter(lambda x: bool(x.layer_name), extensions.by_state(True, 'Import'))
        #evaluation_layer_names = filter(lambda x: bool(x.layer_name) & bool(x.show_results), extensions.by_state(True, 'Evaluation'))
        #if all([legend.nodeExists(i.layer_name) for i in import_layer_names]) & all([legend.nodeExists(i.layer_name) for i in evaluation_layer_names]):
        if all([not i.needs_evaluation() for i in extensions.by_state(True, 'Evaluation')]) & all([not i.needs_evaluation() for i in extensions.by_state(True,'Import')]):
            self.main_process_dock.buildings_evaluated.setChecked(True)
        else:
            self.main_process_dock.buildings_evaluated.setChecked(False)
        legend.nodeHide(config.building_coordinate_layer_name)
        self.reorder_layers()
        oeq_global.OeQ_pop_info(baritem)

        result = self.main_process_dock.buildings_evaluated.isChecked()
        if result:
            oeq_global.OeQ_push_status(message="All buildings succesfully evaluated!")
        else:
            oeq_global.OeQ_push_status(message="Could not evaluate all buildings!")
        return result


    def buildings_evaluated(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3 import extensions
        #import_layer_names = filter(lambda x: bool(x.layer_name), extensions.by_state(True, 'Import'))
        #evaluation_layer_names = filter(lambda x: bool(x.layer_name) & bool(x.show_results), extensions.by_state(True, 'Evaluation'))
        #if all([legend.nodeExists(i.layer_name) for i in import_layer_names]) & all([legend.nodeExists(i.layer_name) for i in evaluation_layer_names]):
        if all([not i.needs_evaluation() for i in extensions.by_state(True, 'Evaluation')]) & all([not i.needs_evaluation() for i in extensions.by_state(True, 'Import')]):
            self.main_process_dock.buildings_evaluated.setChecked(True)
        else:
            self.main_process_dock.buildings_evaluated.setChecked(False)
        self.main_process_dock.buildings_evaluated.setChecked(False)
        return self.main_process_dock.buildings_evaluated.isChecked()



    def check_plugin_availability(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        return self.handle_pst_plugin_installed() & self.handle_ol_plugin_installed() & self.handle_real_centroid_plugin_installed()

    def update_workstep_states_in_Gui(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from qgis.PyQt import QtWidgets
        for i in self.standard_workflow.worksteps:
            object=self.main_process_dock.findChild(QtWidgets.QWidget, i)
            object.setChecked(self.standard_workflow.workstep_is_done(i))


    def run(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        import time
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.main_process_dock)
        self.check_plugin_availability()
        if not self.main_process_dock.automode.isChecked():
            self.standard_workflow.do_workstep('project_created')
            self.standard_workflow.do_workstep('project_saved')
            self.standard_workflow.do_workstep('investigationarea_defined')

        else:
            while not self.standard_workflow.is_done():
                self.main_process_dock.call_next_workstep(self)
                time.sleep(0.5)
        return True


    def save_oeq_project(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        print("#kkklll")
        import os,pickle
        from mole3.oeq_global import OeQ_project_info,OeQ_ExtensionRegistry
        project = {'project_info':OeQ_project_info,
                   'extension_registry':OeQ_ExtensionRegistry}
        project_path = oeq_global.OeQ_project_path()
        project_name = oeq_global.OeQ_project_name()
        project_file = os.path.join(project_path, project_name + '.oeq')
        #print("PATH",project_path)
        #print("NAME",project_name)
        #print("FILE",project_file)
        if os.path.exists(project_file):
             os.remove(project_file)
        with open(project_file, 'wb') as f:
            pickle.dump(project, f,protocol=2)

    def load_oeq_project(self):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        import os,pickle
        from mole3 import oeq_global
        from mole3 import extensions
        project_path = oeq_global.OeQ_project_path()
        project_name = oeq_global.OeQ_project_name()
        project_file = os.path.join(project_path, project_name + '.oeq')
        if os.path.exists(project_file):
            with open(project_file, 'rb') as f:
                project=pickle.load(f)
            #print project
            oeq_global.OeQ_project_info = project['project_info']
            #oeq_global.OeQ_ExtensionRegistry = project['extension_registry']
            #for ext in oeq_global.OeQ_ExtensionRegistry:
            #    ext.copy_default_colortable_to_project(True)
            extensions.copy_extensions_to_project()
            oeq_global.OeQ_ExtensionsLoaded = True
            self.reorder_layers()
            legend.nodeZoomTo(config.investigation_shape_layer_name)
            self.launch_oeq()
            #extensions.load()

    def export_database_to_json(self,fileName=None):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3.qgisinteraction import legend
        from mole3.project import config
        from mole3 import oeq_global
        from qgis.core import QgsVectorFileWriter
        import os
        database= legend.nodeByName(config.data_layer_name)
        if  database:
            database = database[0]
            if not fileName:
                fileName = QFileDialog.getSaveFileName(None,"Save Database as GeoJSON:",os.path.join(oeq_global.OeQ_project_path(),oeq_global.OeQ_project_name()+"_db.geojson"),"*.geojson")
            if fileName:
                QgsVectorFileWriter.writeAsVectorFormat(database.layer(),fileName, 'utf-8',database.layer().crs(), 'GeoJson')
                return fileName
        else:
            print("No Database available!")
        return None


    #QgsVectorLayer, QString, QString, QgsCoordinateReferenceSystem, QString driverName="ESRI Shapefile", bool onlySelected=False, QString errorMessage=None, QStringList datasourceOptions=QStringList(), QStringList layerOptions=QStringList(), bool skipAttributeCreation=False, QString newFilename=None, QgsVectorFileWriter.SymbologyExport symbologyExport=QgsVectorFileWriter.NoSymbology, float symbologyScale=1, QgsRectangle filterExtent=None)


    def export_database_to_csv(self,fileName=None):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3.qgisinteraction import legend
        from mole3.project import config
        from mole3 import oeq_global
        from qgis.core import QgsVectorFileWriter
        import os
        database= legend.nodeByName(config.data_layer_name)
        if  database:
            database = database[0]
            if not fileName:
                fileName = QFileDialog.getSaveFileName(None,"Save Database as TAB-delimited CSV-File:",os.path.join(oeq_global.OeQ_project_path(),oeq_global.OeQ_project_name()+"_db.csv"),"*.csv")
            if fileName:
                QgsVectorFileWriter.writeAsVectorFormat(database.layer(),fileName, 'utf-8',database.layer().crs(), 'CSV', False, "", "", ["SEPARATOR=SEMICOLON"])
                return fileName
        else:
            print("No Database available!")
        return None

    def export_database_to_sqlite(self,fileName=None):
        if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
        from mole3.qgisinteraction import legend
        from mole3.project import config
        from mole3 import oeq_global
        from qgis.core import QgsVectorFileWriter
        import os
        database= legend.nodeByName(config.data_layer_name)
        if  database:
            database = database[0]
            if not fileName:
                fileName = QFileDialog.getSaveFileName(None,"Save Database as SQLite:",os.path.join(oeq_global.OeQ_project_path(),oeq_global.OeQ_project_name()+"_db.sqlite"),"*.sqlite")
            if fileName:
                QgsVectorFileWriter.writeAsVectorFormat(database.layer(),fileName, 'utf-8',database.layer().crs(), 'SQLite')
                return fileName
        else:
            print("No Database available!")
        return None

