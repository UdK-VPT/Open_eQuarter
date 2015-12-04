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
        print "Welcome to Open eQuarter. To support the messagebar it is necessary to open the console once..."
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
        print('Load wms')

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
        print oeq_global.OeQ_project_info['location_lon']
        print oeq_global.OeQ_project_info['location_lat']
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

        if legend.nodeExists(config.investigation_shape_layer_name):
             investigation_area_node=legend.nodeByName(config.investigation_shape_layer_name)
             if investigation_area_node:
                investigation_area_node=investigation_area_node[0]
                if investigation_area_node.layer().featureCount():
                    legend.nodeZoomTo(config.investigation_shape_layer_name)
                    loop_quit()
                    self.main_process_dock.investigationarea_defined.setChecked(True)
                    return self.main_process_dock.investigationarea_defined.isChecked()
        self.main_process_dock.investigationarea_defined.setChecked(False)
        return self.main_process_dock.investigationarea_defined.isChecked()




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


        '''
            shape_sources = extensions.by_type('shp', 'Import', True)
            # shape_sources = filter(lambda source: source.type == 'shp', oeq_global.OeQ_information_source)
            for shape in shape_sources:
                # extension =
                if shape.layer_name.startswith(config.housing_layer_name):

                    self.main_process_dock.handle_import_ext_selected.setChecked(True)
                    time.sleep(0.1)
                    #return True
        #self.handle_load_raster_maps()
        return True
        '''


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

    '''
        ext_info=extensions.by_layername(config.housing_layer_name)
        if not ext_info: return False
        ext_info = ext_info[0]

        building_outlines_path = os.path.normpath(ext_info.source)
        intersection_done = False

        # Check wether IA Layer exists and has polygons defined
        investigation_area = legend.nodeByName(config.investigation_shape_layer_name)
        ia_ok = bool(investigation_area)
        if ia_ok:
            investigation_area = investigation_area[0].layer()
            ia_ok &= (investigation_area.featureCount() > 0)

        if not ia_ok:
            self.handle_investigation_area_selected()
            #oeq_global.OeQ_init_error("Unable to create building outlines",
            #                          "Map 'Investigation Area' could not be found...")
            return intersection_done

        legend.nodeZoomTo(config.investigation_shape_layer_name)

        oeq_global.OeQ_init_info("Getting building outlines in the investigation area.", "This may take some time...")
        if os.path.exists(building_outlines_path):
            layer_interaction.fullRemove(ext_info.layer_name)
            layer_interaction.fullRemove(config.data_layer_name)

            intersection_layer_path = os.path.join(oeq_global.OeQ_project_path(), ext_info.layer_name + '.shp')
            #data_layer_path = os.path.join(oeq_global.OeQ_project_path(), config.data_layer_name + '.shp')

            housing_layer = layer_interaction.load_layer_from_disk(building_outlines_path, ext_info.layer_name)

            intersection_done = layer_interaction.intersect_shapefiles(housing_layer, investigation_area,
                                                                       intersection_layer_path)

            if intersection_done:
                from os import system
                new_path=os.path.join(os.path.basename(intersection_layer_path)+'_32633.shp')
                #define oldPath and newPath
                cmd = 'ogr2ogr -f ESRI Shapefile -s_srs '+housing_layer.crs().authid()+' -t_srs epsg:32633 '+new_path+' '+intersection_layer_path
                os.system(cmd)
                out_layer = layer_interaction.load_layer_from_disk(new_path, ext_info.layer_name)
                layer_interaction.add_layer_to_registry(out_layer)

                layer_interaction.edit_housing_layer_attributes(out_layer)

                layer_interaction.trigger_edit_mode(self.iface, out_layer.name(), 'off')
                inter_layer = self.iface.addVectorLayer(out_layer.source(), 'BLD Calculate', out_layer.providerType())
                layer_interaction.add_layer_to_registry(inter_layer)

                #QgsVectorFileWriter.writeAsVectorFormat(inter_layer, data_layer_path, "CP1250", None, "ESRI Shapefile")
                # layer_interaction.write_vector_layer_to_disk(inter_layer, data_layer_path)
                QgsMapLayerRegistry.instance().removeMapLayer(inter_layer.id())

                #data_layer = layer_interaction.load_layer_from_disk(data_layer_path, config.data_layer_name)
                #layer_interaction.add_layer_to_registry(data_layer)

                #move housing layer to position 2 in root & load colortable
                legend.nodeMove(ext_info.layer_name,2)
                ext_info.update_colortable()
                out_layer.loadNamedStyle(ext_info.colortable)

                #create group data at bottom of root (if necessary)

                self.reorder_layers()

                oeq_global.OeQ_kill_info()
                source_section = self.progress_items_model.section_views[1]
                section_model = source_section.model()
                project_item = section_model.findItems("Intersect building outlines (\"Hausumringe\") with your investigation area")[0]
                project_item.setCheckState(2)
                time.sleep(0.1)
                self.handle_building_coordinates_acquired()
                return True
        oeq_global.OeQ_kill_info()
        return 1


    '''




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



    '''
    def handle_load_raster_maps(self):
        """
        Load the wms-maps that were defined in the source-dialog
        :return:
        :rtype:
        """
        from mole import extensions
        raster_layers = []
        legend.nodesShow([config.investigation_shape_layer_name])
       #legend.nodeZoomTo(config.investigation_shape_layer_name)
        oeq_global.OeQ_unlockQgis()
        gtiff_sources = extensions.by_type('gtiff', 'Import', True)
        for info_source in gtiff_sources:
            pass
        shp_sources = extensions.by_type('shp', 'Import', True)
        for info_source in shp_sources:
            pass
        wfs_sources = extensions.by_type('wfs', 'Import', True)
        for info_source in wfs_sources:
            pass
        dxf_sources = extensions.by_type('dxf', 'Import', True)
        for info_source in dxf_sources:
            pass
        csv_sources = extensions.by_type('csv', 'Import', True)
        for info_source in csv_sources:
            pass
        wms_sources = extensions.by_type('wms', 'Import', True)

        progressbar = oeq_global.OeQ_init_progressbar(u"Loading WMS Layer",
                                                      u"WMS Servers are slow, this may take a while...",
                                                      maxcount=len(raster_layers) + 2)
        progress_counter = oeq_global.OeQ_push_progressbar(progressbar, 0)

        for importextension in wms_sources:
            if legend.nodeIsLayer(importextension.layer_name):
                continue
            layer_interaction.fullRemove(layer_id=info_source.layer_id)

            if not legend.nodeExists(importextension.category):
                cat=legend.nodeCreateGroup(importextension.category,'bottom')
            else:
                cat=legend.nodeByName(importextension.category)[0]
           #create group data at bottom of root (if necessary)
            if not legend.nodeExists(importextension.subcategory):
                subcat=legend.nodeCreateGroup(importextension.subcategory,'bottom',cat)
            else:
                subcat=legend.nodeByName(importextension.subcategory)[0]
            legend.nodeMove(config.open_layers_layer_name,'bottom')

            name = 'WMS_' + importextension.layer_name + '_RAW'
            url = importextension.source
            raster_layer = layer_interaction.open_wms_as_raster(self.iface, url, name)

            raster_loaded = False
            try:
                if raster_layer.isValid():
                    layer_interaction.add_layer_to_registry(raster_layer)
                    self.iface.setActiveLayer(raster_layer)
                    raster_loaded = True
            except AttributeError as NoneTypeError:
                print(self.__module__, NoneTypeError)

            if not raster_loaded:
                self.iface.actionAddWmsLayer().trigger()
            else:
                raster_layer = legend.nodeMove(raster_layer.name(),'bottom',subcat).layer()
                importextension.layer_id = raster_layer.id()
            progress_counter = oeq_global.OeQ_push_progressbar(progressbar, progress_counter)

        # Let's wait for the WMS loading
        progress_counter = oeq_global.OeQ_push_progressbar(progressbar, progress_counter)
        oeq_global.OeQ_kill_progressbar()
        source_section = self.progress_items_model.section_views[1]
        section_model = source_section.model()
        project_item = section_model.findItems("Load WMS maps")[0]
        project_item.setCheckState(2)
        time.sleep(0.1)
        self.handle_raster_loaded()
        return True
        #self.continue_process(True)

    # step 2.3
    def handle_raster_loaded(self):
        from mole import extensions
        #print 'Hallo'
        legend.nodesShow([config.investigation_shape_layer_name])
        #try:
        investigation_area = legend.nodeByName(config.investigation_shape_layer_name)
        if not investigation_area:
            oeq_global.OeQ_init_error("Unable to create building outlines",
                                  "Map 'Investigation Area' could not be found...")
            return False
        investigation_area = investigation_area[0].layer()

        if investigation_area.featureCount() < 0:
            oeq_global.OeQ_init_error("Unable to create building outlines",
                                  "No areas defined in map 'Investigation Area'...")
            return False

        # an investigation shape is needed, to trigger the zoom to layer function

        #if investigation_shape.featureCount() > 0:
        # zoom
        #self.iface.setActiveLayer(investigation_shape)
        #self.iface.actionZoomToLayer().trigger()
        legend.nodeZoomTo(config.investigation_shape_layer_name)
       # oeq_global.OeQ_unlockQgis()
        # clip extent from visible raster layers
        # save visible layers and set them invisible afterwards, to prevent further from the wms-server
        raster_layers = layer_interaction.get_raster_layer_list(self.iface, 'visible')
        print [l.name() for l in raster_layers]
        raster_layers = filter(lambda wms_layer: not wms_layer.source().endswith('.tif'), raster_layers)

        progressbar = oeq_global.OeQ_init_progressbar(u"Caching the WMS Section to GeoTIFF",
                                                      u"This may take some time...",
                                                      maxcount=len(raster_layers) + 2)
        progress_counter = oeq_global.OeQ_push_progressbar(progressbar, 0)

        print [i.name() for i in raster_layers]
        for layer in raster_layers:
            layernode=legend.nodeByLayer(layer)
            if not layernode: continue
            layernode = layernode[0]
            legend.nodeHide(layernode)
            #self.iface.legendInterface().setLayerVisible(layer, False)
        extracted_layers = []
        for clipping_raster in raster_layers:
            progress_counter = oeq_global.OeQ_push_progressbar(progressbar, progress_counter)
            clipped_layer = self.clip_from_raster(clipping_raster)
            print 'clipped'
            extracted_layers.append(clipped_layer)

            cLay = legend.nodeByName(clipped_layer)
            if not cLay: return False
            cLay=cLay[0].layer()
            print 'now get url'

            lUrl = wms_utils.getWmsLegendUrl(clipping_raster)
            print lUrl
            cLay.setLegendUrl(lUrl)

            # set new layer id in extension if available
            extension = extensions.by_layerid(clipping_raster.id())
            if extension is not None:
                extension[0].layer_id = cLay.id()

            # remove the wms source from the legend
            QgsMapLayerRegistry.instance().removeMapLayer(clipping_raster.id())
            #legend.nodeCollapse(subcat)
            #legend.nodeCollapse(cat)

        oeq_global.OeQ_kill_progressbar()
        #except AttributeError as NoneException:
        #    print(self.__module__, NoneException)
         #   return False

        progressbar = oeq_global.OeQ_init_progressbar(u"Reproject GeoTIFF to EPSG 3857 (WGS 84 / Pseodo-Mercator)",
                                                      u"This may take some time.",
                                                      maxcount=len(extracted_layers) + 2)
        progress_counter = oeq_global.OeQ_push_progressbar(progressbar, 0)

        for layer_name in extracted_layers:
            progress_counter = oeq_global.OeQ_push_progressbar(progressbar, progress_counter)
            try:
                layer = legend.nodeByName(layer_name)
                if not layer: return False
                layer = layer[0].layer()
                print 'url'
                # save legendUrl from source
                legUrl = layer.legendUrl()
                raster_layer_interaction.gdal_warp_layer(layer, config.project_crs)
                path_geo = layer.publicSource()
                path_transformed = path_geo.replace('_RAW.tif', '_transformed.tif')
                # print path_geo
                no_timeout = 50
                while not os.path.exists(path_transformed) and no_timeout:
                    time.sleep(0.1)
                    no_timeout -= 1

                if os.path.exists(path_transformed):
                    # change validation to surpress missing-crs prompt
                    old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'useProject'))
                    QSettings().setValue('/Projections/defaultBehaviour', 'useProject')

                    layer_interaction.unhide_or_remove_layer(layer_name, 'remove', self.iface)
                    rlayer = QgsRasterLayer(path_transformed, layer_name)
                    rlayer.setCrs(QgsCoordinateReferenceSystem(config.project_crs, QgsCoordinateReferenceSystem.EpsgCrsId))
                    # write legendUrl to the converted layer
                    rlayer.setLegendUrl(legUrl)
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer)

                    # set new layer id in appropriate extension if available
                    extension = extensions.by_layername(layer_name)
                    if extension is not None:
                        extension[0].layer_id = rlayer.id()
                    # os.remove(path_geo)
                    self.iface.mapCanvas().refresh()
                    # restore former settings
                    QSettings().setValue('/Projections/defaultBehaviour', old_validation)
                    # print rlayer.legendUrl()
            except (OSError, AttributeError) as Clipping_Error:
                print(self.__module__, Clipping_Error)
                pass
        oeq_global.OeQ_kill_progressbar()

        source_section = self.progress_items_model.section_views[1]
        section_model = source_section.model()
        project_item = section_model.findItems("Capture WMS maps")[0]
        project_item.setCheckState(2)
        time.sleep(0.1)
        return True
    def handle_legend_created(self):
        return self.prepare_color_picker()
    '''
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


    '''
        # ToDo Change to non default-values
        area = NULL
        perimeter = NULL
        building_height = NULL
        floors = NULL  # default_
        pop_dens = 3927  # default
        yoc = 1948  # default
        acc_heat_hours = 72000  # default

        yoc_fld = NULL
        pdens_fld = NULL
        area_fld = "AREA"
        peri_fld = "PERIMETER"
        floors_fld = NULL


        # dlg = EstimatedEnergyDemand_dialog()
        # dlg.show()
        start_calc = True  # dlg.exec_()
        if start_calc:
            # ToDo It has to be checked, if the in- and out-layer have the same amount of features
            # att_name = dlg.field_name.text()[:10]
            in_layer = layer_interaction.find_layer_by_name(config.pst_output_layer_name)
            in_provider = in_layer.dataProvider()
            out_layer = layer_interaction.find_layer_by_name(config.data_layer_name)
            out_provider = out_layer.dataProvider()
            data_layer_path = os.path.join(oeq_global.OeQ_project_path(), config.data_layer_name + '.shp')

            def join_layers(layer, tgt_layer, idx='BLD_ID', tgt_idx='BLD_ID', prefix='db_'):
                joinObject = QgsVectorJoinInfo()
                joinObject.joinLayerId = tgt_layer.id()
                joinObject.joinFieldName = tgt_idx
                joinObject.targetFieldName = idx
                joinObject.memoryCache = True
                joinObject.prefix = prefix
                layer.addJoin(joinObject)

            def create_evaluation_layer(layer_name='Evaluation Layer',
                                        template_layer=layer_interaction.find_layer_by_name(config.housing_layer_name),
                                        data_layer=layer_interaction.find_layer_by_name(config.data_layer_name),
                                        group=NULL,
                                        subgroup=NULL):
                root = QgsProject.instance().layerTreeRoot()
                new_layer = self.iface.addVectorLayer(template_layer.source(), layer_name,
                                                      template_layer.providerType())
                node_layer = QgsLayerTreeLayer(new_layer)
                if not isnull(group):
                    if not isnull(subgroup):
                        node_group = QgsLayerTreeGroup(subgroup)
                    else:
                        node_group = QgsLayerTreeGroup(subgroup)
                else:
                    node_group = root
                # node_group.insertChildNode(0, node_layer)
                return new_layer

            for attr in in_provider.fields().toList():
                if attr.name().endswith("YOC"): yoc_fld = attr.name()
                if attr.name().endswith("PDENS_M"): pdens_fld = attr.name()
                if attr.name().endswith("FLOORS"): floors_fld = attr.name()

            # pdens_fld = dlg.area.currentText()
            # area_fld = dlg.area.currentText()
            # peri_fld = dlg.perimeter.currentText()
            # yoc_fld = dlg.yoc.currentText()
            # floors_fld = dlg.floors.currentText()
            prefetched_attribute_names = evaluate_building(1000).keys()
            out_provider.deleteAttributes(out_provider.fieldNameIndex(i) for i in prefetched_attribute_names)

            str_attributes = []
            double_attributes = []
            for attrname in prefetched_attribute_names:
                if attrname in ["HTS_FLT", "HTS_BLD", "OWN_FLT", "OWN_BLD"]:
                    str_attributes.append(QgsField(attrname, QVariant.String))
                else:
                    double_attributes.append(QgsField(attrname, QVariant.Double))
            layer_interaction.add_attributes_if_not_exists(out_layer, str_attributes)
            layer_interaction.add_attributes_if_not_exists(out_layer, double_attributes)

            out_layer.startEditing()

            progressbar = oeq_global.OeQ_init_progressbar(u'Building Evaluation!', u'This might take 30 seconds...',
                                                          maxcount=in_layer.featureCount() + 1)
            progress_counter = oeq_global.OeQ_push_progressbar(progressbar, 0)
            for inFeat in in_provider.getFeatures():
                progress_counter = oeq_global.OeQ_push_progressbar(progressbar, progress_counter)
                outFeat = filter(lambda x: x.attribute('BLD_ID') == inFeat.attribute('BLD_ID'),
                                 out_provider.getFeatures())
                if len(outFeat) > 0:
                    outFeat = outFeat[0]
                    if not isnull(yoc_fld):
                        if not isnull(inFeat.attribute(yoc_fld)):
                            yoc = inFeat.attribute(yoc_fld)
                    if not isnull(floors_fld):
                        if not isnull(inFeat.attribute(floors_fld)):
                            floors = inFeat.attribute(floors_fld)

                    est_ed = evaluate_building(population_density=pop_dens,
                                               area=inFeat.attribute("AREA"),
                                               perimeter=inFeat.attribute("PERIMETER"),
                                               floors=floors,
                                               year_of_construction=yoc,
                                               accumulated_heating_hours=acc_heat_hours)
                    for i in est_ed.keys():
                        outFeat[i] = est_ed[i]
                    out_layer.updateFeature(outFeat)
            out_layer.commitChanges()

            QgsVectorFileWriter.writeAsVectorFormat(out_layer, data_layer_path, "CP1250", None, "ESRI Shapefile")

            root = QgsProject.instance().layerTreeRoot()

            # node_group = root.insertGroup(0, "Transmission Heat Loss")
            # node_subgroup1 = node_group.addGroup("Present")
            # node_subgroup2 = node_group.addGroup("Contemporary")

            layer_interaction.fullRemove('Transmission Heat Loss (Present)')
            new_layer = create_evaluation_layer(
                layer_name='Transmission Heat Loss (Present)')  # ,group="Transmission Heat Loss",subgroup="Present")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_epass_HLP.qml'))
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Transmission Heat Loss (Contemporary)')
            new_layer = create_evaluation_layer(
                layer_name='Transmission Heat Loss (Contemporary)')  # ,group="Transmission Heat Loss",subgroup="Contemporary")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_epass_HLC.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            # node_group = root.insertGroup(0, "Component Qualities")
            # node_subgroup1 = node_group.addGroup("Present")
            # node_subgroup2 = node_group.addGroup("Contemporary")

            layer_interaction.fullRemove('Base Quality (U_Value, Present)')
            new_layer = create_evaluation_layer(
                layer_name='Base Quality (U_Value, Present)')  # ,group="Component Qualities",subgroup="Present")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_UP_Base.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Base Quality (U_Value, Contemporary)')
            new_layer = create_evaluation_layer(
                layer_name='Base Quality (U_Value, Contemporary)')  # ,group="Component Qualities",subgroup="Contemporary")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_UC_Base.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Wall Quality (U_Value, Present)')
            new_layer = create_evaluation_layer(
                layer_name='Wall Quality (U_Value, Present)')  # ,group="Component Qualities",subgroup="Present")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_UP_Wall.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Wall Quality (U_Value, Contemporary)')
            new_layer = create_evaluation_layer(
                layer_name='Wall Quality (U_Value, Contemporary)')  # ,group="Component Qualities",subgroup="Contemporary")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_UC_Wall.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Window Quality (U_Value, Present)')
            new_layer = create_evaluation_layer(
                layer_name='Window Quality (U_Value, Present)')  # ,group="Component Qualities",subgroup="Present")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_UP_Window.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Window Quality (U_Value, Contemporary)')
            new_layer = create_evaluation_layer(
                layer_name='Window Quality (U_Value, Contemporary)')  # ,group="Component Qualities",subgroup="Contemporary")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_UC_Window.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Roof Quality (U_Value, Present)')
            new_layer = create_evaluation_layer(
                layer_name='Roof Quality (U_Value, Present)')  # ,group="Component Qualities",subgroup="Present")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_UP_Roof.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Roof Quality (U_Value, Contemporary)')
            new_layer = create_evaluation_layer(layer_name='Roof Quality (U_Value, Contemporary)')
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_UC_Roof.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            # node_group = root.insertGroup(0, "Solar Heat")

            layer_interaction.fullRemove('Solar Coverage Rate')
            new_layer = create_evaluation_layer(layer_name='Solar Coverage Rate')  # ,group="Solar Heat")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_RT_Sol.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Solar Earning')
            new_layer = create_evaluation_layer(layer_name='Solar Earning')  # ,group="Solar Heat")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_HE_Sol.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            # node_group = root.insertGroup(0, "Heating System")

            layer_interaction.fullRemove('Heatings System (by Building)')
            new_layer = create_evaluation_layer(layer_name='Heatings System (by Building)')  # ,group="Heating System")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_HTS_Building.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Heatings System (by Flat)')
            new_layer = create_evaluation_layer(layer_name='Heatings System (by Flat)')  # ,group="Heating System")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_HTS_Flat.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            # node_group = root.insertGroup(0, "Soft Facts")

            layer_interaction.fullRemove('Owners (by Building)')
            new_layer = create_evaluation_layer(layer_name='Owners (by Building)')  # ,group="Soft Facts")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_OWN_Building.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            layer_interaction.fullRemove('Owners (by Flat)')
            new_layer = create_evaluation_layer(layer_name='Owners (by Flat)')  # ,group="Soft Facts")
            join_layers(new_layer, out_layer)
            new_layer.loadNamedStyle(os.path.join(oeq_global.OeQ_plugin_path(), 'styles', 'oeq_OWN_Flat.qml'))
            self.iface.legendInterface().setLayerVisible(new_layer, False)
            self.iface.legendInterface().setLayerExpanded(new_layer, False)

            oeq_global.OeQ_kill_progressbar()
            return True
        else:
            return False

    def continue_process(self, autorun=False):
        """
        Call the appropriate handle-function, depending on the progress-step, that has to be executed next.
        :return:
        :rtype:
        """
        last_view = self.progress_items_model.section_views[-1]

        i = 0
        while last_view.model().item(i):
            i += 1

        last_step_name = last_view.model().item(i - 1).accessibleText()
        first_open_item = self.progress_items_model.check_prerequisites_for(last_step_name)
        if first_open_item.checkState() == 2:
            return
        first_open_item.setCheckState(1)

        handler = 'handle_{}'.format(first_open_item.accessibleText())
        next_call = getattr(self, handler)
        progress_state = next_call()

        QgsProject.instance().setDirty(True)
        first_open_item.setCheckState(progress_state)

    def XXX_process_button_clicked(self, model_index):
        """
        Call the appropriate handle-function, depending on the QStandardItem which triggered the function call.
        :param model_index: The senders model_index
        :type model_index: QModelIndex
        :return:
        :rtype:
        """
        model = model_index.model()
        row = model_index.row()
        item = model.item(row)
        clicked_step = item.accessibleText()

        # for debugging uncomment the following line
        if True:
            # if self.progress_items_model.check_prerequisites_for(clicked_step):
            #QgsProject.instance().setDirty(True)
            item.setCheckState(1)
            handler = 'handle_' + clicked_step
            step_call = getattr(self, handler)
            is_done = step_call()
            # Set the items state to 2 or 0, since its state is represented by a tristate checkmark
            if is_done:
                item.setCheckState(2)
            else:
                item.setCheckState(0)
    '''
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
        if self.main_process_dock.automode.isChecked():
            while not self.standard_workflow.is_done(): pass
        return
        if self.check_plugin_availability():
            self.main_process_dock.select_page('oeq_project_basics')
            if self.handle_project_created():
                if self.handle_project_saved():
                    self.handle_investigationarea_defined()
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
            print project
            oeq_global.OeQ_project_info = project['project_info']
            oeq_global.OeQ_ExtensionRegistry = project['extension_registry']
            self.reorder_layers()
            legend.nodeZoomTo(config.investigation_shape_layer_name)
            self.launch_oeq()
            #extensions.load()

    '''
        if not oeq_global.OeQ_project_saved():
            self.oeq_project_settings_form.show()
            save = self.oeq_project_settings_form.exec_()
            if save:
                self.handle_project_created()
                plugin_section = self.progress_items_model.section_views[0]
                section_model = plugin_section.model()
                project_item = section_model.findItems('Create a new project and save it')[0]
                if oeq_global.OeQ_project_saved():
                    project_item.setCheckState(2)
                else:
                    project_item.setCheckState(0)

        if oeq_global.OeQ_project_saved() and oeq_global.OeQ_project_info['project_name']:
            # municipal = self.oeq_project_settings_form.municipals[0]
            self.continue_process()
            # oeq_global.OeQ_init_info('Coordinates not defined',
            #'Zoom to your investigation area automatically, by setting lon and lat.')

    def set_next_step_done(self, is_done):
        """
        Find the next step in the progress model and change its status to is_done
        :param is_done: The status of the next step
        :type is_done: bool
        :return:
        :rtype:
        """
        last_view = self.progress_items_model.section_views[-1]

        i = 0
        while last_view.model().item(i):
            i += 1

        last_step_name = last_view.model().item(i - 1).accessibleText()
        next_open_item = self.progress_items_model.check_prerequisites_for(last_step_name)
        next_open_item.setCheckState(is_done)
    '''






