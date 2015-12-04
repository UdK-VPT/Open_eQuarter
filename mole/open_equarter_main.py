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

from PyQt4.QtGui import *

from PyQt4.QtCore import SIGNAL, Qt, QSettings, QVariant

from qgis.gui import QgsMapToolEmitPoint, QgsMessageBar
from qgis.core import *
#from model.progress_model import ProgressItemsModel
from view.oeq_dialogs import (
    Modular_dialog, ProjectSettings_form, ProjectDoesNotExist_dialog,
    ColorPicker_dialog, MainProcess_dock, RequestWmsUrl_dialog, InformationSource_dialog)
from qgisinteraction import (
    plugin_interaction,
    layer_interaction,
    raster_layer_interaction,
    project_interaction,
    wms_utils,
    legend)
from mole.project import config
from mole.stat_util.building_evaluation import evaluate_building
from mole import oeq_global

def do_print():
    pass

def isnull(value):
    return type(value) is type(NULL)


class OpenEQuarterMain:
    def __init__(self, iface):
        #from mole.oeq_workflows import OeQ_Workflow
        # Save reference to the QGIS interface
        self.iface = iface
        ### Monitor the users progress
        #self.progress_items_model = ProgressItemsModel()
        self.initWorkflow()

        #enable on the fly projection
        self.iface.mapCanvas().mapSettings().setCrsTransformEnabled(True)
        #self.iface.mapCanvas().mapRenderer().setProjectionsEnabled(True)
        crsSrc = self.iface.mapCanvas().mapSettings().setDestinationCrs(QgsCoordinateReferenceSystem(int(config.project_crs.split(':')[1]), QgsCoordinateReferenceSystem.EpsgCrsId))
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

        ### Project specific settings
        self.oeq_project = ''

        # OpenStreetMap-plugin-layer
        self.open_layer = None

        # to work flawlessly on the messagebar it is necessary to initialize the Python console once
        self.iface.actionShowPythonDialog().trigger()
        #print "Welcome to Open eQuarter. To support the messagebar it is necessary to open the console once..."
        self.iface.actionShowPythonDialog().trigger()  # in fact it's not show but toggle

    def new_project(self):

        #self.progress_items_model.load_section_models(config.progress_model)
        #self.main_process_dock.process_button_next.clicked.connect(self.continue_process)
        #sections = self.progress_items_model.section_views

        #for list_view in sections:
        #    list_view.clicked.connect(self.process_button_clicked)

        import copy
        oeq_global.OeQ_project_info = copy.deepcopy(config.pinfo_default)
        self.update_workstep_states_in_Gui()


    def initGui(self):
        from qgis.core import QgsProject
        project =QgsProject.instance()
        plugin_icon = QIcon(os.path.join(':', oeq_global.OeQ_plugin_path(), 'icons', 'OeQ_plugin_icon.png'))
        self.main_action = QAction(plugin_icon, u"OpenEQuarter-Process", self.iface.mainWindow())
        self.main_action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.main_action)
        self.iface.addPluginToMenu(u"&OpenEQuarter", self.main_action)

        clipping_icon = QIcon(os.path.join(':', 'Plugin', 'icons', 'scissor.png'))
        self.clipping_action = QAction(clipping_icon, u"Extract extent from active WMS", self.iface.mainWindow())
        self.clipping_action.triggered.connect(lambda: self.clip_from_raster(self.iface.activeLayer()))
        self.iface.addToolBarIcon(self.clipping_action)
        self.iface.addPluginToMenu(u"&OpenEQuarter", self.clipping_action)
        self.iface.projectRead.connect(self.load_oeq_project)
        self.iface.newProjectCreated.connect(self.new_project)
        project.projectSaved.connect(self.save_oeq_project)

        #self.initGui_process_dock()

    def initMainProcessDock(self):
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
                                      lambda: wms_utils.save_wms_extent_as_image(self.iface.activeLayer().name()))
        #tools_dropdown_menu.addAction('Calculate Energy Demand', self.handle_building_calculations)

        self.main_process_dock.tools_dropdown_btn.setMenu(tools_dropdown_menu)
        self.main_process_dock.settings_dropdown_btn.setMenu(settings_dropdown_menu)


    def initWorkflow(self):
                #register worksteps
        from oeq_workflows import OeQ_Workflow,OeQ_WorkStep
        #init standard workflow
        self.standard_workflow=OeQ_Workflow('OeQ_standard','Standard Workflow of Open eQuarter')
        self.standard_workflow.register_workstep(OeQ_WorkStep('ol_plugin_installed', 'Check if the Openlayers Plugin exists', self.handle_ol_plugin_installed, self.check_if_ol_plugin_installed))
        self.standard_workflow.register_workstep(OeQ_WorkStep('pst_plugin_installed', 'Check if the Pointsampling Tool Plugin exists', self.handle_pst_plugin_installed, self.check_if_pst_plugin_installed))
        self.standard_workflow.register_workstep(OeQ_WorkStep('real_centroid_plugin_installed', 'Check if the Reacentroid Plugin exists', self.handle_real_centroid_plugin_installed, self.check_if_real_centroid_plugin_installed))
        self.standard_workflow.register_workstep(OeQ_WorkStep('project_created', 'Create a Project', self.handle_project_created, self.check_if_project_created))
        self.standard_workflow.register_workstep(OeQ_WorkStep('project_saved', 'Save the Project', self.handle_project_saved, self.check_if_project_saved))
        self.standard_workflow.register_workstep(OeQ_WorkStep('investigationarea_defined', 'Define Investigation Area', self.handle_investigationarea_defined, self.check_if_investigationarea_defined))
        self.standard_workflow.register_workstep(OeQ_WorkStep('building_outlines_acquired', 'Get building outlines', self.handle_building_outlines_acquired, self.check_if_building_outlines_acquired))
        self.standard_workflow.register_workstep(OeQ_WorkStep('building_coordinates_acquired', 'Get building coordinates', self.handle_building_coordinates_acquired, self.check_if_building_coordinates_acquired))
        self.standard_workflow.register_workstep(OeQ_WorkStep('information_layers_loaded', 'Load information layers', self.handle_information_layers_loaded, self.check_if_information_layers_loaded))
        self.standard_workflow.register_workstep(OeQ_WorkStep('needle_request_done', 'Perform Needle Request', self.handle_needle_request_done, self.check_if_needle_request_done))
        self.standard_workflow.register_workstep(OeQ_WorkStep('database_created', 'Create Building Database', self.handle_database_created, self.check_if_database_created))
        self.standard_workflow.register_workstep(OeQ_WorkStep('buildings_evaluated', 'Do all Building Evaluations', self.handle_buildings_evaluated, self.check_if_buildings_evaluated))
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
        legend.nodeMove(config.investigation_shape_layer_name,'top')
        legend.nodeMove(config.housing_coordinate_layer_name,1)
        legend.nodeMove(config.housing_layer_name,2)
        legend.nodeMove(config.open_layers_layer_name,'bottom')



    def open_settings(self):
        self.oeq_project_settings_form.show()
        save = self.oeq_project_settings_form.exec_()
        if save:
            self.handle_project_created()
        #self.run()
        #self.oeq_project_settings_form.show()

    def launch_oeq(self):
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
        from qgis.core import QgsProject
        project =QgsProject.instance()
        self.iface.removePluginMenu(u"&OpenEQuarter", self.main_action)
        self.iface.removePluginMenu(u"&OpenEQuarter", self.clipping_action)
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
        from PyQt4.QtCore import QFileInfo
        from PyQt4.QtGui import QFileDialog,QMessageBox
        import shutil
        if not project_interaction.project_exists():
            # prompt the user to save the project
            self.project_does_not_exist_dlg.show()
            yes_to_save = self.project_does_not_exist_dlg.exec_()

            if yes_to_save:
                dialog=QFileDialog()
                path=dialog.getExistingDirectory(None,'Navigate to the directory you want project \"'+ oeq_global.OeQ_project_info['project_name'] + '\" to be stored in:')
                if path:
                    project_dir = os.path.join(path,oeq_global.OeQ_project_info['project_name'].replace (" ", "_"))
                    project_file = oeq_global.OeQ_project_info['project_name'].replace (" ", "_")+'.qgs'
                    project_file =  project_file
                    if os.path.exists(project_dir):
                        if [i.endswith('.qgs') for i in os.listdir(project_dir)]:
                            ask=QMessageBox()
                            reply = ask.question(ask, 'Open eQuarter Alert', "Project exists! Do you want to overwrite?", ask.Yes | ask.No, ask.No)
                            if reply == ask.No: return False
                        else:
                            ask=QMessageBox()
                            ask.question(ask, 'Open eQuarter Alert', "Directory exists, but does not contain a QGIS project! \n Rename your project!", ask.Ok, ask.Ok)
                            return False
                        shutil.rmtree(project_dir, ignore_errors=True)
                    os.makedirs(project_dir)
                    QgsProject.instance().setFileName(os.path.join(project_dir,project_file))
                    self.iface.actionSaveProject().trigger()
                    return True
        return False



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
        Set the extent of the open layer to the default extent and scale specified as in config.default_extent and self.default_scale
        :return:
        :rtype:
        """
        # try:
        canvas = self.iface.mapCanvas()
        #print oeq_global.OeQ_project_info['location_lon']
        #print oeq_global.OeQ_project_info['location_lat']
        if (not oeq_global.OeQ_project_info['location_lon']) | (not  oeq_global.OeQ_project_info['location_lat']):
            x = config.x
            y=config.y
            scale = config.scale
        else:
            x = float(oeq_global.OeQ_project_info['location_lon'])
            y = float(oeq_global.OeQ_project_info['location_lat'])
            scale = 0.01
        extent = QgsRectangle(x - scale, y - scale, x + scale, y + scale)
        map_crs = canvas.mapSettings().destinationCrs()
        source_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        transformer = QgsCoordinateTransform(source_crs, map_crs)
        extent = transformer.transform(extent)

        canvas.setExtent(extent)
        canvas.refresh()

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

        canvas = self.iface.mapCanvas()
        crs = canvas.mapSettings().destinationCrs()

        return crs

    def clip_from_raster(self, raster_layer):
        """
        Clip the current extent from the given raster-layer
        :param raster_layer: The raster-layer which will be clipped
        :type raster_layer: QgsRasterLayer
        :return:
        :rtype:
        """
        try:
            # set the rasterlayer as active, since only the active layer will be clipped and start the exp
            self.iface.setActiveLayer(raster_layer)
            geo_export_path = wms_utils.save_wms_extent_as_image(raster_layer.name())
            pyramids_built = raster_layer_interaction.gdal_addo_layerfile(geo_export_path, 'gauss', 6)
            if pyramids_built != 0:
                print 'Error number {} occured, while building pyramids.'.format(pyramids_built)
        except AttributeError as NoneException:
            print(self.__module__, NoneException)
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
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.ol_plugin_name)
        if plugin_exists:
            self.main_process_dock.ol_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.ol_plugin_installed.setChecked(False)
            return False

    def check_if_ol_plugin_installed(self):
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.ol_plugin_name)
        if plugin_exists:
            self.main_process_dock.ol_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.ol_plugin_installed.setChecked(False)
            return False

    # step 0.1
    def handle_pst_plugin_installed(self):
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.pst_plugin_name)
        if plugin_exists:
            self.main_process_dock.pst_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.pst_plugin_installed.setChecked(False)
            return False

    def check_if_pst_plugin_installed(self):
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.pst_plugin_name)
        if plugin_exists:
            self.main_process_dock.pst_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.pst_plugin_installed.setChecked(False)
            return False

    # step 0.2
    def handle_real_centroid_plugin_installed(self):
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.real_centroid_plugin_name)
        if plugin_exists:
            self.main_process_dock.real_centroid_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.real_centroid_plugin_installed.setChecked(False)
            return False

    def check_if_real_centroid_plugin_installed(self):
        plugin_exists = plugin_interaction.get_plugin_ifexists(config.real_centroid_plugin_name)
        if plugin_exists:
            self.main_process_dock.real_centroid_plugin_installed.setChecked(True)
            return True
        else:
            self.main_process_dock.real_centroid_plugin_installed.setChecked(False)
            return False

    # step 0.3
    def handle_project_created(self):
        self.oeq_project_settings_form.show()
        save = self.oeq_project_settings_form.exec_()
        if save:
            self.main_process_dock.project_created.setChecked(True)
            #self.handle_project_saved()
        else:
            self.main_process_dock.project_created.setChecked(False)

        return self.main_process_dock.project_created.isChecked()
            #self.handle_project_saved()
            #return self.create_project_ifNotExists()

    def check_if_project_created(self):
        if bool(oeq_global.OeQ_project_info['location_city']) & bool(oeq_global.OeQ_project_info['location_lon']):
            self.main_process_dock.project_created.setChecked(True)
        else:
            self.main_process_dock.project_created.setChecked(False)
        return self.main_process_dock.project_created.isChecked()



    def handle_project_saved(self):
        from mole import extensions
        extensions.load_defaults()
        self.create_project_ifNotExists()
        if oeq_global.OeQ_project_saved():
            extensions.update_all_colortables()
            self.main_process_dock.project_saved.setChecked(True)
        else:
            self.main_process_dock.project_saved.setChecked(False)
        return self.main_process_dock.project_saved.isChecked()

    def check_if_project_saved(self):
        if oeq_global.OeQ_project_saved():
            self.main_process_dock.project_saved.setChecked(True)
        else:
            self.main_process_dock.project_saved.setChecked(False)
        return self.main_process_dock.project_saved.isChecked()



    # step 1.0
    def handle_investigationarea_defined(self):
        from PyQt4.QtCore import QEventLoop
        from qgis.gui import QgsMessageBar
        if not self.standard_workflow.all_mandatory_worksteps_done('investigationarea_defined'):
            self.main_process_dock.investigationarea_defined.setChecked(False)
            return False
        loop = QEventLoop()
        confirmed = [False]
        try:
            from PyQt4.QtCore import QString
        except ImportError:
            # we are using Python3 so QString is not defined
            QString = type("")

        if not self.osm_layer_is_loaded():
            ol_plugin = plugin_interaction.OlInteraction(config.ol_plugin_name)

            if ol_plugin.open_osm_layer(config.open_layer_type_id):
                layer_dict = QgsMapLayerRegistry.instance().mapLayers()
                for layer_name, layer in layer_dict.iteritems():
                    if 'OpenLayers_plugin_layer' in layer_name:
                        self.open_layer = layer
                        break


        #enable on the fly projection
        #self.iface.mapCanvas().mapRenderer().setProjectionsEnabled(True)
        #self.iface.mapCanvas().mapRenderer().setDestinationCrs(QgsCoordinateReferenceSystem(int(config.project_crs.split(':')[1])))

        self.zoom_to_default_extent()
        # remove if necessary
        layer_interaction.trigger_edit_mode(self.iface, config.investigation_shape_layer_name, 'off')
        layer_interaction.fullRemove(config.investigation_shape_layer_name)
       # p_path = os.path.join(oeq_global.OeQ_project_path(), config.investigation_shape_layer_name + '.shp').decode('utf-8')
        oeq_global.QeQ_disableDialogAfterAddingFeature()

        investigation_area = layer_interaction.create_temporary_layer(config.investigation_shape_layer_name, 'Polygon',
                                                                      config.project_crs)
        if investigation_area is not None:
            investigation_area.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', config.investigation_shape_layer_style))
            oeq_global.OeQ_wait(5)
            layer_interaction.trigger_edit_mode(self.iface, config.investigation_shape_layer_name)
            legend.nodeSetActive(config.investigation_shape_layer_name)

            widget = self.iface.messageBar().createMessage('Cover Investigation Area',
                                                           'Click "Done" once the investigation area is completely covered.')
            button = QPushButton(widget)
            button.setText('Done')
            button.released.connect(lambda: self.confirm_selection_of_investigation_area(loop.quit,confirmed))
            button.destroyed.connect(loop.quit)
            widget.layout().addWidget(button)

            self.iface.messageBar().pushWidget(widget, QgsMessageBar.WARNING,duration = 3600)

            loop.exec_()
            layer_interaction.trigger_edit_mode(self.iface, config.investigation_shape_layer_name, 'off')
            oeq_global.QeQ_enableDialogAfterAddingFeature()
            oeq_global.OeQ_kill_warning()
            if confirmed[0]:
                if legend.nodeExists(config.investigation_shape_layer_name):
                    investigation_area_node=legend.nodeByName(config.investigation_shape_layer_name)
                    if investigation_area_node:
                        investigation_area_node=investigation_area_node[0]
                        if investigation_area_node.layer().featureCount():
                            legend.nodeZoomTo(config.investigation_shape_layer_name)
                            self.main_process_dock.investigationarea_defined.setChecked(True)
                            return self.main_process_dock.investigationarea_defined.isChecked()
            layer_interaction.fullRemove(config.investigation_shape_layer_name)
            self.main_process_dock.investigationarea_defined.setChecked(False)
            return self.main_process_dock.investigationarea_defined.isChecked()


    def confirm_selection_of_investigation_area(self,loop_quit,confirmed):
        #from mole import oeq_global
        #from mole.qgisinteraction import legend
        confirmed[0]=True
        loop_quit()
        return True






    def check_if_investigationarea_defined(self):
        from mole.project import config
        if legend.nodeExists(config.investigation_shape_layer_name):
            self.main_process_dock.investigationarea_defined.setChecked(True)
        else:
            self.main_process_dock.investigationarea_defined.setChecked(False)
        return self.main_process_dock.investigationarea_defined.isChecked()


    # step 2.0
    def handle_import_ext_selected(self):
        if not self.standard_workflow.all_mandatory_worksteps_done('import_ext_selected'):
            self.main_process_dock.import_ext_selected.setChecked(False)
            return False
        done = self.information_source_dlg.exec_()
        if done:
            self.main_process_dock.import_ext_selected.setChecked(True)
        else:
            self.main_process_dock.import_ext_selected.setChecked(False)
        return self.main_process_dock.import_ext_selected.isChecked()

    def check_if_import_ext_selected(self):
        from mole.project import config
        return self.main_process_dock.import_ext_selected.isChecked()



    # step 2.1
    def handle_building_outlines_acquired(self):
        from mole import extensions
        from mole import oeq_global
        from mole.qgisinteraction import legend
        from mole.project import config
        if not self.standard_workflow.all_mandatory_worksteps_done('building_outlines_acquired'):
            self.main_process_dock.building_outlines_acquired.setChecked(False)
            return False
        self.iface.mapCanvas().freeze()
        legend.nodeZoomTo(config.investigation_shape_layer_name)
        building_outline_ext=extensions.by_layername(config.housing_layer_name,active=True)
        if not building_outline_ext:
            oeq_global.OeQ_init_warning("No import extension for Building Outlines", "Load geometries or define them on a new Vectorlayer named '"+config.housing_layer_name+"' !")
            self.main_process_dock.building_outlines_acquired.setChecked(False)
            return False
        building_outline_ext = building_outline_ext[0]
        oeq_global.OeQ_wait(5)
        building_outline_ext.load_wfs()
        oeq_global.OeQ_wait(5)
        oeq_global.OeQ_init_info("Clipping Building Outlines:", "'"+config.housing_layer_name+"'")
        building_outlines=legend.nodeClipByShapenode(config.housing_layer_name,config.investigation_shape_layer_name)
        original_crs=building_outlines.layer().crs().authid()
        self.iface.mapCanvas().freeze(False)
        self.iface.mapCanvas().refresh()

        #oeq_global.OeQ_init_info("Converting Building Outlines:", "'"+config.measurement_projection+"'")
        #print "convert"
        #oeq_global.OeQ_wait(5)
        #building_outlines=legend.nodeConvertCRS(building_outlines,config.measurement_projection)
        oeq_global.OeQ_kill_info()

        #oeq_global.OeQ_init_info("Calculating basic geometries of Building Outlines:", "'"+config.housing_layer_name+"'")
        if not building_outlines:
            self.main_process_dock.building_outlines_acquired.setChecked(False)
            return False
        #layer_interaction.edit_housing_layer_attributes(building_outlines.layer())
        #building_outlines=legend.nodeConvertCRS(building_outlines,original_crs)
        #oeq_global.OeQ_wait(5)

        legend.nodeCreateBuildingIDs(building_outlines)
        #return building_outlines.layer()
        self.reorder_layers()
        self.main_process_dock.building_outlines_acquired.setChecked(True)
        return True

    def check_if_building_outlines_acquired(self):
            from mole.project import config
            if legend.nodeExists(config.housing_layer_name):
                self.main_process_dock.building_outlines_acquired.setChecked(True)
            else:
                self.main_process_dock.building_outlines_acquired.setChecked(False)
            return self.main_process_dock.building_outlines_acquired.isChecked()


    # step 2.2
    def handle_building_coordinates_acquired(self):
        from qgis.core import QgsCoordinateReferenceSystem
        window = self.iface.mainWindow()
        #legend.nodeZoomTo(config.investigation_shape_layer_name)
        #oeq_global.OeQ_unlockQgis()

        if self.standard_workflow.all_mandatory_worksteps_done('building_coordinates_acquired'):
            centroid_layer=None
            original_crs=None
            layer_interaction.fullRemove(config.pst_input_layer_name)

            #get building outlines
            building_outlines = legend.nodeByName(config.housing_layer_name)
            if building_outlines:
                building_outlines = building_outlines[0]

                original_crs=building_outlines.layer().crs().authid()

                load_message = "Calculate building coordinates from building outlines?"
                ask=QMessageBox()
                reply = ask.question(ask, 'Building Coordinates', "Calculate building coordinates from building outlines?", ask.Yes | ask.No, ask.Yes)
                if reply == ask.No:
                    dialog=QFileDialog()
                    filepath=dialog.getOpenFileName(None,'Select a shape file that holds the bulding coordinates (.shp):',selectedFilter='*.shp')
                    if filepath:
                        centroid_layer=layer_interaction.load_layer_from_disk(filepath)
                        if centroid_layer:
                            centroid_layer.setName(config.pst_input_layer_name)

                else:
                    rci = plugin_interaction.RealCentroidInteraction(config.real_centroid_plugin_name)
                    polygon = config.housing_layer_name
                    output = os.path.join(oeq_global.OeQ_project_path(), config.pst_input_layer_name + '.shp')
                    centroid_layer = rci.create_centroids(polygon, output)

                    if centroid_layer.isValid():
                        layer_interaction.add_layer_to_registry(centroid_layer)
                        centroid_layer.setCrs(QgsCoordinateReferenceSystem(int(original_crs.split(':')[1]), QgsCoordinateReferenceSystem.EpsgCrsId))
                        rci.calculate_accuracy(building_outlines.layer(), centroid_layer)
                        layer_interaction.add_style_to_layer(config.valid_centroids_style, centroid_layer)

            if centroid_layer:
                legend.nodeByName(centroid_layer.name())[0].setExpanded(False)
                self.reorder_layers()
                self.main_process_dock.building_coordinates_acquired.setChecked(True)
                return self.main_process_dock.building_coordinates_acquired.isChecked()

        self.main_process_dock.building_coordinates_acquired.setChecked(False)
        return self.main_process_dock.building_coordinates_acquired.isChecked()



    def check_if_building_coordinates_acquired(self):
        from mole.project import config
        if legend.nodeExists(config.pst_input_layer_name):
            self.main_process_dock.building_coordinates_acquired.setChecked(True)
        else:
            self.main_process_dock.building_coordinates_acquired.setChecked(False)
        return self.main_process_dock.building_coordinates_acquired.isChecked()

    def handle_information_layers_loaded(self):
        from mole import extensions
        from mole.project import config
        from mole.qgisinteraction import legend
        if not self.standard_workflow.all_mandatory_worksteps_done('information_layers_loaded'):
            self.main_process_dock.information_layers_loaded.setChecked(False)
            return False
        legend.nodeZoomTo(config.investigation_shape_layer_name)

        for i in extensions.by_type('wms',category='Import',active=True):
            i.load_wms()
            #return True
        if all([legend.nodeExists(i.layer_name) for i in extensions.by_type('wms',category='Import',active=True)]):
            self.main_process_dock.information_layers_loaded.setChecked(True)
        else:
            self.main_process_dock.information_layers_loaded.setChecked(False)
        self.reorder_layers()
        return self.main_process_dock.information_layers_loaded.isChecked()


    def check_if_information_layers_loaded(self):
        from mole import extensions
        from mole.qgisinteraction import legend
        if all([legend.nodeExists(i.layer_name) for i in extensions.by_type('wms',category='Import',active=True)]):
            self.main_process_dock.information_layers_loaded.setChecked(True)
        else:
            self.main_process_dock.information_layers_loaded.setChecked(False)

        return self.main_process_dock.information_layers_loaded.isChecked()



    def pick_color(self):
        self.coordinate_tracker.canvasClicked.connect(self.handle_canvas_click)
        self.iface.mapCanvas().setMapTool(self.coordinate_tracker)

    def prepare_color_picker(self):
        self.pick_color()
        self.color_picker_dlg.start_colorpicking.clicked.connect(self.pick_color)
        save_or_abort = self.color_picker_dlg.exec_()

        success = True
        lvm = self.color_picker_dlg.color_entry_manager.layer_values_map
        for legend in lvm.values():
            legend_available = legend is not None
            success = success and legend_available

        self.iface.actionPan().trigger()
        if success:

            return True
        else:
            self.reorder_layers()
            return 1



    # step 4.1
    def handle_needle_request_done(self):
        from mole import extensions
        from mole.project import config
        # create data node
        if not legend.nodeExists('Data'):
            cat=legend.nodeCreateGroup('Data')
        else:
            cat=legend.nodeByName('Data')[0]
        #create_database
        #self.create_database(True,'Data')
        oeq_global.OeQ_init_info('Needle Request:', 'Collecting data... be patient!')

        # show import layers
        layerstoshow = [config.investigation_shape_layer_name,config.pst_input_layer_name]
        layerstoshow += ([i.layer_name for i in extensions.by_category('Import',extensions.by_state(True))])
        legend.nodesShow(layerstoshow)
        input_node=legend.nodeByName(config.pst_input_layer_name)
        if input_node:
            #get original crs (necessary because qgis does not deal with epsg:3857 very well, but sets it to epsg:54004)
            source_crs=input_node[0].layer().crs()

            #remove point sampling layer
            layer_interaction.fullRemove(layer_name=config.pst_output_layer_name)


            #run point sampling tool
            psti = plugin_interaction.PstInteraction(self.iface, config.pst_plugin_name)
            psti.set_input_layer(config.pst_input_layer_name)
            abbreviations = psti.select_and_rename_files_for_sampling()
            pst_output_layer = psti.start_sampling(oeq_global.OeQ_project_path(), config.pst_output_layer_name)
            vlayer = QgsVectorLayer(pst_output_layer, config.pst_output_layer_name,"ogr")
            layer_interaction.add_layer_to_registry(vlayer)
            #set original crs (necessary because qgis does not deal with epsg:3857 very well, but sets it to epsg:54004)
            vlayer.setCrs(source_crs)
            #resultnode=legend.nodeConvertCRS(config.pst_output_layer_name,config.default_extent_crs)
            resultnode=legend.nodeByName(vlayer.name())
            if resultnode:
                resultnode = resultnode[0]
                #move to data
                legend.nodeMove(resultnode,'bottom','Data')

                #run import extensions

                # collapse and hide
                legend.nodeCollapse('Import')
                legend.nodeHide('Import')

        if legend.nodeExists(config.pst_output_layer_name):
            self.reorder_layers()
            self.main_process_dock.needle_request_done.setChecked(True)
        else:
            self.main_process_dock.needle_request_done.setChecked(False)
        oeq_global.OeQ_kill_info()
        return self.main_process_dock.needle_request_done.isChecked()



    def check_if_needle_request_done(self):
        from mole.project import config
        if legend.nodeExists(config.pst_output_layer_name):
            self.main_process_dock.needle_request_done.setChecked(True)
        else:
            self.main_process_dock.needle_request_done.setChecked(False)
        return self.main_process_dock.needle_request_done.isChecked()


    def handle_database_created(self):
        from mole.qgisinteraction import legend
        oeq_global.OeQ_init_info('Create Database:', 'Generating building records... be patient!')

        result= bool(legend.nodeCreateDatabase(config.housing_layer_name,config.data_layer_name,config.measurement_projection,True,"Data"))
        self.reorder_layers()
        oeq_global.OeQ_kill_info()
        return result

    def check_if_database_created(self):
        from mole.project import config
        if legend.nodeExists(config.data_layer_name):
            self.main_process_dock.database_created.setChecked(True)
        else:
            self.main_process_dock.database_created.setChecked(False)
        return self.main_process_dock.database_created.isChecked()

    # step 4.2
        # step 4.1
    def handle_buildings_evaluated(self):
        from mole import extensions
        oeq_global.OeQ_init_info('Building Evaluation:', 'Checking dependencies... be patient!')
        for i in extensions.by_state(True,'Import'):
            i.calculate()
        #extensions.run_active_extensions('Import')
        success = all([legend.nodeExists(i.layer_name) for i in extensions.by_state(True,'Import')])
        for i in extensions.by_state(True,'Evaluation'):
            i.calculate()
        #extensions.run_active_extensions('Evaluation')
        success = success & all([legend.nodeExists(i.layer_name) for i in extensions.by_state(True,'Evaluation')])
        legend.nodeHide(config.pst_input_layer_name)
        self.reorder_layers()
        oeq_global.OeQ_kill_info()
        return success

    def check_if_buildings_evaluated(self):
        from mole import extensions
        if (all([legend.nodeExists(i.layer_name) for i in extensions.by_state(True,'Import')]) &
                all([legend.nodeExists(i.layer_name) for i in extensions.by_state(True,'Evaluation')])):
            self.main_process_dock.buildings_evaluated.setChecked(True)
        else:
            self.main_process_dock.buildings_evaluated.setChecked(False)
        return self.main_process_dock.buildings_evaluated.isChecked()



    def check_plugin_availability(self):
        return self.handle_pst_plugin_installed() & self.handle_ol_plugin_installed() & self.handle_real_centroid_plugin_installed()

    def update_workstep_states_in_Gui(self):
        from PyQt4 import QtGui
        for i in self.standard_workflow.worksteps:
            object=self.main_process_dock.findChild(QtGui.QWidget, i)
            object.setChecked(self.standard_workflow.workstep_is_done(i))


    def run(self):
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.main_process_dock)
        self.check_plugin_availability()
        if not self.main_process_dock.automode.isChecked():
            self.standard_workflow.do_workstep('project_created')
            self.standard_workflow.do_workstep('project_saved')
            self.standard_workflow.do_workstep('investigationarea_defined')
        else:
            while not self.standard_workflow.is_done():
                self.main_process_dock.call_next_workstep(self)
        return True


    def save_oeq_project(self):
        import os,pickle
        from mole.oeq_global import OeQ_project_info,OeQ_ExtensionRegistry
        project = {'project_info':OeQ_project_info,
                   'extension_registry':OeQ_ExtensionRegistry}
        project_path = oeq_global.OeQ_project_path()
        project_name = oeq_global.OeQ_project_name()
        project_file = os.path.join(project_path, project_name + '.oeq')
        if os.path.exists(project_file):
             os.remove(project_file)
        pickle.dump(project, open(project_file, 'wb'),protocol=2)

    def load_oeq_project(self):
        import os,pickle
        from mole import oeq_global
        from mole import extensions
        project_path = oeq_global.OeQ_project_path()
        project_name = oeq_global.OeQ_project_name()
        project_file = os.path.join(project_path, project_name + '.oeq')
        if os.path.exists(project_file):
            project=pickle.load(open(project_file, 'rb'))
            #print project
            oeq_global.OeQ_project_info = project['project_info']
            oeq_global.OeQ_ExtensionRegistry = project['extension_registry']
            self.reorder_layers()
            legend.nodeZoomTo(config.investigation_shape_layer_name)
            self.launch_oeq()
            #extensions.load()

