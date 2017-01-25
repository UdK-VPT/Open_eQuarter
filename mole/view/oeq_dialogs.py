# -*- coding: utf-8 -*-
'''
/***************************************************************************
 Open eQuarter Dialogs

                             -------------------
        begin                : 2014-10-07
        copyright            : (C) 2014 by Kim Gülle / UdK-Berlin
        email                : firstdayofjune@users.noreply.github.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
'''
import os
from functools import partial

from PyQt4 import QtGui, QtCore
from qgis.core import QgsMapLayerRegistry, QgsMapLayer
from qgis.utils import iface,plugins

from mole.model.file_manager import ColorEntryManager, MunicipalInformationTree
from mole.qgisinteraction import layer_interaction, legend
from mole import oeq_global
from mole.project import config
from mole.webinteraction import googlemaps
from oeq_ui_classes import QColorTableDelegate, QColorTableModel
from ui_color_picker_dialog import Ui_color_picker_dialog
from ui_main_process_dock import Ui_MainProcess_dock, _fromUtf8
from ui_project_does_not_exist_dialog import Ui_ProjectDoesNotExist_dialog
from ui_project_settings_form import Ui_project_settings_form
from ui_modular_info_dialog import Ui_ModularInfo_dialog
from ui_modular_dialog import Ui_Modular_dialog
from ui_request_wms_url_dialog import Ui_RequestWmsUrl_dialog
from ui_estimated_energy_demand_dialog import Ui_EstimatedEnergyDemand_dialog
from ui_information_source_dialog import Ui_InformationSource_dialog


# from mole.extensionActive.ui_extensions_active import Ui_Dialog



# import mole.extensions as extensions



class InformationSource_dialog(QtGui.QDialog, Ui_InformationSource_dialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        #self.refresh_dropdown()
        self.extension_dropdown.currentIndexChanged.connect(self.complete_information)
        role = QtGui.QDialogButtonBox.AcceptRole
        self.buttonBox.addButton('Done', role)
        role = QtGui.QDialogButtonBox.ActionRole
        next_button = self.buttonBox.addButton('Save source...', role)
        next_button.clicked.connect(self.register_information)
        self.open_geotiff_btn.clicked.connect(lambda: self.load_source_from_disk(self.geotiff))
        self.open_shapefile_btn.clicked.connect(lambda: self.load_source_from_disk(self.shapefile))
        self.open_csv_btn.clicked.connect(lambda: self.load_source_from_disk(self.csv))
        self.open_dxf_btn.clicked.connect(lambda: self.load_source_from_disk(self.dxf))
        self.stateBox.clicked.connect(self.toggle_state)
        self.complete_information()

    def refresh_dropdown(self):
        import mole.extensions as extensions
        self.extension_dropdown.clear()
        self.placeholder = '<Select information type>'
        self.extension_dropdown.addItem(self.placeholder)
        for importextension in extensions.by_category('Import'):
            self.extension_dropdown.addItem(importextension.extension_name)



    def complete_information(self):
        """
        Check if the selected extension has some defaults and if so insert the default info in the text fields.
        :return:
        :rtype:
        """
        # clear all line-edits first
        import mole.extensions as extensions
        line_edits = self.gridWidget.findChildren(QtGui.QLineEdit)
        for line_edit in line_edits:
            line_edit.clear()

        extension = self.extension_dropdown.currentText()
        for importextension in extensions.by_category('Import'):
            if extension == importextension.extension_name:
                self.layer_name.setText(importextension.layer_name)
                self.field_id.setText(importextension.field_id)
                field = getattr(self, importextension.source_type)
                field.setText(importextension.source)
                self.stateBox.setChecked(importextension.active)

    def toggle_state(self):
        import mole.extensions as extensions
        extension_name = self.extension_dropdown.currentText()
        if extension_name in [i.extension_name for i in extensions.by_category('Import')]:
            extension = extensions.by_name(self.extension_dropdown.currentText())[0]
            extension.active = not extension.active
            self.stateBox.setChecked(extension.active)

    def register_information(self):
        import mole.extensions as extensions
        extension_name = self.extension_dropdown.currentText()
        layer_name = self.layer_name.text()
        field_id = self.field_id.text()
        source_path = ''
        type = ''
        line_edits = self.gridWidget.findChildren(QtGui.QLineEdit)
        for line_edit in line_edits:
            if line_edit is not self.layer_name and line_edit.text():
                type = line_edit.objectName()
                source_path = line_edit.text()
                break
        ##print "register information"

        if extension_name != self.placeholder:
            #print "update information"
            if extension_name in [i.extension_name for i in extensions.by_category('Import')]:
                #print "found"
                extensions.by_name(extension_name)[0].update(
                    field_id=field_id,
                    source_type=type,
                    layer_name=layer_name,
                    source=source_path,
                    active=self.stateBox.isChecked())

        else:
            #print "new information"
            extension = extensions.OeQExtension(
                category='Import',
                field_id=field_id,
                source_type=type,
                layer_name=layer_name,
                description=u'Generic extension for ' + layer_name,
                source=source_path,
                active=self.stateBox.isChecked())
            extension.registerExtension()
        self.refresh_dropdown()

        # if type == 'wms':
        #     if not layer_name.startswith('WMS_'):
        #         layer_name = 'WMS_' + str(layer_name)
        #    if not layer_name.endswith('_RAW'):
        #         layer_name = str(layer_name) + '_RAW'

        # info_source = InformationSource(extension, type, field_id, layer_name, source_path)
        #  oeq_global.OeQ_information_source.append(info_source)

        # for line_edit in line_edits:
        #    line_edit.clear()

    def load_source_from_disk(self, field):
        """
        Load a source-file according to the field which was passed.
        :param field:
        :type field:
        :return:
        :rtype:
        """
        source = self.extension_dropdown.currentText()
        if source != self.placeholder:
            file_extension = ''
            if field == self.geotiff:
                file_extension = '.tif'
            elif field == self.shapefile:
                file_extension = '.shp'
            elif field == self.csv:
                file_extension = '.csv'
            elif field == self.dxf:
                file_extension = '.dxf'

            caption = 'Chose a {} file for the "{}" source...'.format(file_extension, source)
            ext_filter = '*' + file_extension
            filename = QtGui.QFileDialog.getOpenFileName(iface.mainWindow(), caption=caption, filter=ext_filter)
            field.setText(filename)

    def exec_(self):
        """
        Call the super exec_ method
        :return:
        :rtype:
        """
        self.refresh_dropdown()
        QtGui.QDialog.exec_(self)
        self.refresh_dropdown()





class ColorPicker_dialog(QtGui.QDialog, Ui_color_picker_dialog):

    def __init__(self):
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.color_entry_manager = ColorEntryManager()
        self.recent_layer = ''
        self.layers_dropdown.currentIndexChanged.connect(self.update_color_values)
        self.destroyed.connect(legend.nodeExitSolo)
        # set the table model
        self.header = ['Color value', 'Parameter Name', 'From', 'To', '']
        self.color_entry_manager.add_layer('dummy')
        self.color_entry_manager.add_color_value_quadruple_to_layer(('RGBa(0, 0, 0, 0)', ' ', 0, 0), 'dummy')
        self.dummy_model = QColorTableModel(self.color_entry_manager.layer_values_map['dummy'], self.header, self)
        self.color_table_view.setModel(self.dummy_model)
        self.setup_table()

        # connect the signals
        self.color_table_view.clicked.connect(self.remove_entry)
        self.refresh_layers_dropdown.clicked.connect(self.refresh_layer_list)
        self.layers_dropdown.currentIndexChanged.connect(self.setup_legend)

        role = QtGui.QDialogButtonBox.ActionRole
        load_button = self.buttonBox.addButton('Load legend...', role)
        load_button.clicked.connect(self.load_color_map)
        save_button = self.buttonBox.addButton('Save legend', role)
        save_button.clicked.connect(self.save_color_map)

    def setup_table(self):
        """
        Set the basic attributes for the color-table view
        :return:
        :rtype:
        """
        for i in range(len(self.header)):
            self.color_table_view.setItemDelegateForColumn(i, QColorTableDelegate(self))

        self.color_table_view.setColumnWidth(0, 205)
        self.color_table_view.setColumnWidth(1, 205)
        self.color_table_view.setColumnWidth(2, 75)
        self.color_table_view.setColumnWidth(3, 75)
        self.color_table_view.setColumnWidth(4, 35)
        self.color_table_view.setShowGrid(False)
        self.color_table_view.setSortingEnabled(True)
        self.color_table_view.sortByColumn(2)

        # set horizontal header properties
        hor_header = self.color_table_view.horizontalHeader()
        hor_header.setStretchLastSection(True)
        hor_header.setStyleSheet('QHeaderView::section { '
                         ' border: None;'
                         ' padding: 3px;'
                         ' font-size: 13px;'
                         ' font-weight: bold;'
                         ' margin: 5px;'
                         ' background-color: rgb(237, 237, 237);'
                         '}'
                         )
        self.color_table_view.setHorizontalHeader(hor_header)

        # set row height
        ver_header = self.color_table_view.verticalHeader()
        ver_header.setDefaultSectionSize(34)
        ver_header.setStyleSheet('QHeaderView::section { '
                         ' border: None;'
                         ' padding: 3px;'
                         ' font-size: 13px;'
                         ' margin: 5px;'
                         ' margin-right: 12px;'
                         ' background-color: rgb(237, 237, 237);'
                         '}'
                         )
        self.color_table_view.setVerticalHeader(ver_header)

    def remove_entry(self, model_index):
        """
        Remove the entry from the color-entry-manager
        :param model_index: The QModelIndex of the clicked element
        :type model_index: QModelIndex
        :return:
        :rtype:
        """
        column = model_index.column()
        if column == 4:
            row = model_index.row()
            model = model_index.model()
            color_key = model.in_data.keys()[row]
            layer = self.layers_dropdown.currentText()
            self.color_entry_manager.remove_color_entry_from_layer(color_key, layer)
            color_map = self.color_entry_manager.layer_values_map[layer]
            if not color_map:
                color_map = self.color_entry_manager.layer_values_map['dummy']
            tm = QColorTableModel(color_map, self.header, self)
            self.color_table_view.setModel(tm)

    def add_color(self, color):
        """
        Insert a new color (and the values associated to it, if any), into the color-table.
        :param color: The color in RGBa
        :type color: QColor
        :return:
        :rtype:
        """
        from mole import extensions

        layer = self.layers_dropdown.currentText()
        self.recent_layer = layer
        color_map = self.color_entry_manager.layer_values_map[layer]
        model = QColorTableModel(color_map, self.header, self)
        self.color_table_view.setModel(model)

        color_key = 'RGBa({}, {}, {}, {})'.format(color.red(), color.green(), color.blue(), color.alpha())
        if color_map.has_key(color_key):
            self.message_label.setStyleSheet(_fromUtf8("color: red;"))
            self.message_label.setText('Attention: Color {} is defined already.'.format(color_key))

        else:
            self.message_label.clear()
            #ToDo change to use the correct para-name instead
            #parameter_name = str(self.layers_dropdown.currentText())[:10]
            parameter_name = extensions.by_layername(layer)
            if not parameter_name: return None
            parameter_name = parameter_name[0].field_id
            self.color_entry_manager.add_color_value_quadruple_to_layer([color_key, parameter_name, 0, 0], layer)
            color_map = self.color_entry_manager.layer_values_map[layer]
            model = QColorTableModel(color_map, self.header, self)
            self.color_table_view.setModel(model)
        self.raise_()

    def update_color_values(self):
        """
        Change the color-table view to display the color-map of the currently selected layer.
        :return:
        :rtype:
        """
        layer = self.layers_dropdown.currentText()
        color_map = {}
        if layer in self.color_entry_manager.layer_values_map:
            color_map = self.color_entry_manager.layer_values_map[layer]
            table_model = QColorTableModel(color_map, self.header, self)
        if not color_map:
            table_model = self.dummy_model
        self.color_table_view.setModel(table_model)
        self.recent_layer = layer

        try:
            wms_layer = legend.nodeByName(layer)[0].layer()
            url = wms_layer.legendUrl()
            self.legend_view.load(QtCore.QUrl(url))
        except (TypeError, AttributeError) as NoneTypeError:
            pass

    def check_character_constraint(self, parameter_name):
        """
        Check if the parameter-name has a length of ten characters at most,
        since layer-attributes are limited to 10 characters.
        :param parameter_name:
        :type parameter_name:
        :return:
        :rtype:
        """
        if len(parameter_name) == 10 and parameter_name != 'Parameter ':
            self.message_label.setStyleSheet(_fromUtf8("color: red;"))
            self.message_label.setText('Warning: A maximum of 10 characters is allowed as a parameter name!')
        else:
            self.message_label.clear()

    def load_color_map(self):
        """
        Load a color-map for the currently opened layer.
        :return:
        :rtype:
        """
        from mole import extensions

        layer = self.layers_dropdown.currentText()
        caption = 'Chose a .qml-legend file for the "{}"-layer...'.format(layer)
        filename = QtGui.QFileDialog.getOpenFileName(iface.mainWindow(), caption=caption, filter='*.qml')
        self.color_entry_manager.read_color_map_from_qml(filename)
        self.update_color_values()
        activeextensions = extensions.by_name(layer)
        try:
            activeextensions[0].colortable = filename
        except:
            pass

    def save_color_map(self):
        """
        Save the currently open color-map as a qml-file into the project folder.
        :return:
        :rtype:
        """
        from mole import extensions

        layer = iface.activeLayer()
        selected_layer = self.layers_dropdown.currentText()
        if layer.name() != selected_layer:
            layer = layer_interaction.find_layer_by_name(selected_layer)

        out_path = os.path.dirname(layer.publicSource())
        out_path = os.path.join(out_path, layer.name() + '.qml')
        self.update_color_values()
        entry_written = self.color_entry_manager.write_color_map_as_qml(layer.name(), out_path)
        if entry_written:
            self.message_label.setStyleSheet(_fromUtf8("color: green;"))
            self.message_label.setText('Success - Legend was successfully written to \n\t"{}".'.format(out_path))
        else:
            self.message_label.setStyleSheet(_fromUtf8("color: red;"))
            self.message_label.setText('Failure - Could not write legend to to \n\t"{}".'.format(out_path))
        activeextensions = extensions.by_layername(layer.name())
        try:
            activeextensions[0].colortable = out_path
        except:
            pass

    def refresh_layer_list(self):
        from mole import extensions
        """
        Update the color-pickers layer-dropdown with a list of the currently visible .tif-files
        :return:
        :rtype:
        """
        legend.nodeExitSolo()
        dropdown = self.layers_dropdown
        dropdown.clear()
        raster_list = layer_interaction.get_raster_layer_list(iface, visibility='visible')
        layer = None
        for layer in raster_list:
            source = layer.publicSource()
            dropdown.addItem(layer.name())
            self.color_entry_manager.add_layer(layer.name())
            ext = extensions.by_layername(layer.name())
            if ext == []:
                ltu_file = os.path.dirname(layer.publicSource())
                ltu_file = os.path.join(ltu_file, layer.name() + '.qml')
            else:
                ext = ext[0]
                ltu_file = ext.colortable
                #print ext.colortable
            #print ltu_file
            if ltu_file != None:
                if os.path.isfile(os.path.join(ltu_file)):
                    self.color_entry_manager.read_color_map_from_qml(os.path.join(ltu_file))
        oeq_global.QeQ_current_work_layer = layer_interaction.find_layer_by_name(self.layers_dropdown.currentText())
        if oeq_global.QeQ_current_work_layer != None:
            #print config.open_layers_layer_name
            legend.nodeInitSolo([config.investigation_shape_layer_name, config.building_outline_layer_name, oeq_global.QeQ_current_work_layer.name(), config.open_layers_layer_name])
        #oeq_global.QeQ_current_work_layer = layer
        #layer_interaction.move_layer_to_position(iface, layer, 0)

    def setup_legend(self):
        legend.nodeExitSolo()
        oeq_global.QeQ_current_work_layer = layer_interaction.find_layer_by_name(self.layers_dropdown.currentText())
        if oeq_global.QeQ_current_work_layer != None:
            #print config.open_layers_layer_name
            legend.nodeInitSolo([config.investigation_shape_layer_name, config.building_outline_layer_name, oeq_global.QeQ_current_work_layer.name(), config.open_layers_layer_name])



    def show(self):
        """
        Update the dropdown menu and hide all .tif-layers except for the one which is currently selected.
        :return:
        :rtype:
        """
        self.refresh_layer_list()
        QtGui.QDialog.show(self)
        self.update_color_values()

    def exec_(self):
        """
        Call the super exec_ method and make the .tif-layers visible again,
        which were hidden during the color-picking-process.
        :return:
        :rtype:
        """
        self.show()
        QtGui.QDialog.exec_(self)
        for i in range(self.layers_dropdown.count()):
            layer_name = self.layers_dropdown.itemText(i)
            layer_interaction.unhide_or_remove_layer(layer_name, 'unhide', iface)


class MainProcess_dock(QtGui.QDockWidget, Ui_MainProcess_dock):

    def __init__(self,mole): #, progress_model):
        #from qgis import utils
        #standard_workflow = utils.plugins['mole'].standard_workflow
        QtGui.QDockWidget.__init__(self)
        self.setupUi(self)
        self._check_mark = QtGui.QPixmap(_fromUtf8(":/Controls/icons/checkmark.png"))
        self._open_mark = QtGui.QPixmap(_fromUtf8(":/Controls/icons/openmark.png"))
        self._semiopen_mark = QtGui.QPixmap(_fromUtf8(":/Controls/icons/semiopenmark.png"))
        #self.progress_model = progress_model
        self.ol_plugin_installed.pressed.connect(lambda: mole.standard_workflow.do_workstep('ol_plugin_installed'))
        self.pst_plugin_installed.pressed.connect(lambda: mole.standard_workflow.do_workstep('pst_plugin_installed'))
        self.real_centroid_plugin_installed.pressed.connect(lambda: mole.standard_workflow.do_workstep('real_centroid_plugin_installed'))
        self.project_created.pressed.connect(lambda: mole.standard_workflow.do_workstep('project_created'))
        self.project_saved.pressed.connect(lambda: mole.standard_workflow.do_workstep('project_saved'))
        self.investigationarea_defined.pressed.connect(lambda: mole.standard_workflow.do_workstep('investigationarea_defined'))
        self.building_outlines_acquired.pressed.connect(lambda: mole.standard_workflow.do_workstep('building_outlines_acquired'))
        self.building_coordinates_acquired.pressed.connect(lambda: mole.standard_workflow.do_workstep('building_coordinates_acquired'))
        self.import_ext_selected.pressed.connect(lambda: mole.standard_workflow.do_workstep('import_ext_selected'))
        self.information_layers_loaded.pressed.connect(lambda: mole.standard_workflow.do_workstep('information_layers_loaded'))
        self.needle_request_done.pressed.connect(lambda: mole.standard_workflow.do_workstep('needle_request_done'))
        self.database_created.pressed.connect(lambda: mole.standard_workflow.do_workstep('database_created'))
        self.buildings_evaluated.pressed.connect(lambda: mole.standard_workflow.do_workstep('buildings_evaluated'))
        self.json_export_done.pressed.connect(mole.export_database_to_json)
        self.sqlite_export_done.pressed.connect(mole.export_database_to_sqlite)
        self.csv_export_done.pressed.connect(mole.export_database_to_csv)

        self.process_button_next.clicked.connect(lambda: self.call_next_workstep(mole))
        self.run_button.clicked.connect(lambda: self.run_automode(mole))
       # for dropdown_index, list_view in enumerate(self.progress_model.section_views):
       #     self.process_page.addWidget(list_view)
       #     self.active_page_dropdown.addItem(list_view.accessibleName())
       #     self.active_page_dropdown.setItemData(dropdown_index, self._open_mark, QtCore.Qt.DecorationRole)
       #     list_view.model().itemChanged.connect(self.check_progress_status)

       # self.active_page_dropdown.currentIndexChanged.connect(lambda: self.go_to_page(self.active_page_dropdown.currentText()))

       # # Remove once the ui_main_process_dock was adopted to the new model
       # self.active_page_dropdown.setCurrentIndex(2)
       # self.active_page_dropdown.setCurrentIndex(0)
    '''
    def check_progress_status(self, changed_item):
        # explicitly check the state, since otherwise the next section gets changed, too
        if changed_item.checkState() == 1:
            current_index = self.active_page_dropdown.currentIndex()
            self.active_page_dropdown.setItemData(current_index, self._semiopen_mark, QtCore.Qt.DecorationRole)

        elif changed_item.checkState() == 2:
            model = changed_item.model()
            section_done = True
            index = 0
            while model.item(index) and section_done:
                item_done = model.item(index).checkState()
                section_done = section_done and item_done
                index += 1

            if section_done:
                current_index = self.active_page_dropdown.currentIndex()
                self.active_page_dropdown.setItemData(current_index, self._check_mark, QtCore.Qt.DecorationRole)
                self.active_page_dropdown.setCurrentIndex(current_index+1)

    '''
    def go_to_page(self, selection_name):
        for child in self.process_page.children():
            if isinstance(child, QtGui.QListView) and child.accessibleName() == selection_name:
                self.process_page.setCurrentWidget(child)
                break

    def select_page(self,section_name):
        pages = self.process_page.children()
        itemindex = [i.objectName() for i in pages].index(section_name)
        dropdownentry = pages[itemindex].accessibleName()
        allitems = [self.active_page_dropdown.itemText(i) for i in range(self.active_page_dropdown.count())]
        itemindex = allitems.index(dropdownentry)
        self.active_page_dropdown.setCurrentIndex(itemindex)


    def set_checkbox_on_page(self, checkbox_name, page_name, check_yes_no):
        if isinstance(check_yes_no, bool):
            page = self.findChild(QtGui.QWidget, page_name)
            checkbox = page.findChild(QtGui.QPushButton, checkbox_name)

            if checkbox:
                checkbox.setChecked(check_yes_no)

    def is_checkbox_on_page_checked(self, checkbox_name, page_name):
        page = self.process_page.findChild(QtGui.QWidget, page_name)
        return page.findChild(QtGui.QPushButton, checkbox_name).isChecked()

    def set_current_page_done(self, value):
        if isinstance(value, bool):
            page_name = self.active_page_dropdown.currentText()
            page = self.selection_to_page[page_name]

            if (page_name) == page.accessibleName():
                index = self.active_page_dropdown.currentIndex()
                self.active_page_dropdown.setItemData(index, self._check_mark, QtCore.Qt.DecorationRole)
                self.active_page_dropdown.setCurrentIndex((index+1) % len(self.selection_to_page))

    def switch_to_objects_parent_page(self,object):
        self.select_page(self.project_created.parent().objectName())

    def switch_to_next_worksteps_page(self,mole):
        from PyQt4 import QtGui
        nextname = mole.standard_workflow.next_workstep_name()
        if bool(nextname):
            pagename = self.process_page.findChild(QtGui.QWidget, nextname).parent().objectName()
            self.select_page(pagename)

    def call_next_workstep(self,mole):
        from PyQt4 import QtGui
        if mole.standard_workflow.is_done():
            return False
        self.switch_to_next_worksteps_page(mole)
        return mole.standard_workflow.do_next_workstep()



    def run_automode(self,mole):
        from qgis import utils
        while (not mole.standard_workflow.is_done()) & self.automode.isChecked():
            self.call_next_workstep(mole)
        self.automode.setChecked(False)

class ProjectDoesNotExist_dialog(QtGui.QDialog, Ui_ProjectDoesNotExist_dialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


class ProjectSettings_form(QtGui.QDialog, Ui_project_settings_form):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.defaults = {}
        self.municipals = [{}]
        self.found_locations = [{}]
        self.municipal_information = MunicipalInformationTree()
        self.municipal_information.read_municipals()
        for field in self.form.findChildren(QtGui.QLineEdit)[:]:
            self.defaults[field.objectName()] = field.text()
            field.textChanged.connect(partial(self.text_changed, field))
        self.location_country.setText(config.country)
        self.lookup_by_address.clicked.connect(self.location_by_address)
        self.lookup_by_coords.clicked.connect(self.location_by_coordinates)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.apply)


    def apply(self):
        if not issubclass(type(self.location_city), QtGui.QLineEdit):
             self.update_form(1)
        for key in oeq_global.OeQ_project_info:
            field = getattr(self, key)
            if (key == 'project_name') & (not field): continue
            if key == 'description':
                oeq_global.OeQ_project_info[key] = field.toPlainText()
            else:
                oeq_global.OeQ_project_info[key] = field.text()

    def show(self):
        #print oeq_global.OeQ_project_info
        for key in oeq_global.OeQ_project_info:
            field = getattr(self, key)
            if key == 'description':
                field.setPlainText(unicode(oeq_global.OeQ_project_info[key]))
            else:
                field.setText(unicode(oeq_global.OeQ_project_info[key]))
        QtGui.QDialog.show(self)

    def reset(self):
        for key in oeq_global.OeQ_project_info:
            field = getattr(self, key)
            field.setText(unicode(u''))
        #print 'resetted'

    def text_changed(self, input_field):
        if input_field.text() != self.defaults[input_field.objectName()]:
            input_field.setStyleSheet('color: rgb(0,0,0)')
            # print self.location_by_address()

    def update_form(self, index):
        index = index - 1
        self.lineedit_city_layout()
        if self.found_locations != []:
            location_info = self.found_locations[index]
            #print location_info
            self.location_country.setText(location_info['country'])
            self.location_city.setText(location_info['locality'])
            self.location_street.setText(location_info['route'])
            if not oeq_global.isEmpty(location_info['street_number']):
                self.location_street.setText(self.location_street.text() + u' ' + location_info['street_number'])
            if not oeq_global.isEmpty(self.location_postal.setText(location_info['postal_code'])):
                self.location_postal.setText(location_info['postal_code'])
            self.location_lon.setText(str(location_info['longitude']))
            self.location_lat.setText(str(location_info['latitude']))
            self.location_crs.setText('EPSG:4326')
            self.set_municipal_data()


    def set_municipal_data(self):
        self.municipals = filter(lambda x :  str(x['POSTCODE']).startswith(self.location_postal.text().encode('utf8')) , self.municipal_information.municipal_db)
        self.municipals = filter(lambda x :  x['NAME'].split()[0].split(',')[0].encode('utf8') == self.location_city.text().split()[0].encode('utf8') , self.municipal_information.municipal_db)

        if len(self.municipals) > 0:
            pop_dens = int('{}'.format(self.municipals[0]['POP_DENS']))
            avg_yoc = '{}'.format(self.municipals[0]['AVG_YOC'])
        else:
            pop_dens = config.default_population_density
            avg_yoc = config.default_construction_year
        self.average_build_year.setText(str(avg_yoc))
        self.population_density.setText(str(pop_dens))


    def get_location_from_web(self,index):
         index -= 1
         self.lineedit_city_layout()
         self.location_city.setText(self.municipals[index]['NAME'])
         self.location_postal.setText(str(self.municipals[index]['POSTCODE']))
         pop_dens = '{}'.format(self.municipals[index]['POP_DENS'])
         self.population_density.setText(pop_dens)
         avg_yoc = '{}'.format(self.municipals[index]['AVG_YOC'])
         self.average_build_year.setText(avg_yoc)
         citystring = ' '.join([self.location_postal.text(),self.location_city.text()])
         address = ', '.join([config.country, citystring, self.location_street.text()])
         self.found_locations = googlemaps.getCoordinatesByAddress(address, crs=4326)
         if len(self.found_locations) == 1:
            self.update_form(1)
         elif len(self.found_locations) > 1:
            self.combobox_city_layout()
            self.location_city.clear()
            self.location_city.addItem(_fromUtf8(u'< Select Location >'))
            for loc in self.found_locations:
                self.location_city.addItem(_fromUtf8(loc['formatted_location']))
            self.location_city.currentIndexChanged.connect(self.update_form)

    def location_by_address(self):
         #if not issubclass(type(self.location_city), QtGui.QLineEdit): return None
         #if not issubclass(type(self.location_postal), QtGui.QLineEdit): return None

         if oeq_global.isEmpty(self.location_city.text()) & oeq_global.isEmpty(self.location_street.text()) & (not oeq_global.isEmpty(self.location_postal.text())):
            postal = self.location_postal.text()
            self.municipals = filter(lambda x :  str(x['POSTCODE']).startswith(postal) , self.municipal_information.municipal_db)
            if len(self.municipals) > 0:
                if len(self.municipals) ==  1:
                    self.lineedit_city_layout()
                    self.location_city.setText(self.municipals[0]['NAME'])
                    self.location_postal.setText(str(self.municipals[0]['POSTCODE']))
                    self.get_location_from_web(1)
                else:
                    self.combobox_city_layout()
                    self.location_city.addItem(_fromUtf8(u'< Select Location >'))
                    for i in [ str(i['POSTCODE']) + u' ' + i['NAME'] for i in self.municipals]:
                        self.location_city.addItem(_fromUtf8(i))
                    self.location_city.currentIndexChanged.connect(self.get_location_from_web)
         elif oeq_global.isEmpty(self.location_postal.text()) & oeq_global.isEmpty(self.location_street.text()) & (not oeq_global.isEmpty(self.location_city.text())):
            city = self.location_city.text()
            self.municipals = filter(lambda x :  x['NAME'].split()[0].split(',')[0] == city.split()[0].split(',')[0] , self.municipal_information.municipal_db)
            if len(self.municipals) > 0:
                if len(self.municipals) ==  1:
                    self.lineedit_city_layout()
                    self.location_city.setText(self.municipals[0]['NAME'])
                    self.location_postal.setText(str(self.municipals[0]['POSTCODE']))
                    self.get_location_from_web(1)
                else:
                    self.combobox_city_layout()
                    self.location_city.addItem(_fromUtf8(u'< Select Location >'))
                    for i in [ str(i['POSTCODE']) + u' ' + i['NAME'] for i in self.municipals]:
                        self.location_city.addItem(_fromUtf8(i))
                    self.location_city.currentIndexChanged.connect(self.get_location_from_web)
         else:
              #self.lineedit_city_layout()
              #self.lineedit_postal_layout()
             citystring = ' '.join([self.location_postal.text(),self.location_city.text()])
             address = ', '.join([config.country, citystring, self.location_street.text()])
             self.found_locations = googlemaps.getCoordinatesByAddress(address, crs=4326)
             if len(self.found_locations) == 1:
                self.update_form(1)
             elif len(self.found_locations) > 1:
                self.combobox_city_layout()
                self.location_city.clear()
                self.location_city.addItem(_fromUtf8(u'< Select Location >'))
                for loc in self.found_locations:
                    self.location_city.addItem(_fromUtf8(loc['formatted_location']))
                self.location_city.currentIndexChanged.connect(self.update_form)


    def location_by_coordinates(self):
        #if not issubclass(type(self.location_city), QtGui.QLineEdit): return None
        #if not issubclass(type(self.location_postal), QtGui.QLineEdit): return None
        lat = float(self.location_lat.text())
        lon = float(self.location_lon.text())
        crs = self.location_crs.text()
        if crs:
            crs=int(crs[5:])
        self.found_locations = googlemaps.getBuildingLocationDataByCoordinates(lon, lat, crs)
        if len(self.found_locations) == 1:
            self.update_form(1)
        elif len(self.found_locations) > 1:
            self.combobox_city_layout()
            self.location_city.clear()
            self.location_city.addItem(_fromUtf8(u'< Select Project Location >'))
            for loc in self.found_locations:
                self.location_city.addItem(_fromUtf8(loc['formatted_location']))
            self.location_city.currentIndexChanged.connect(self.update_form)


    def find_municipal_information(self):
        city = self.location_city.text()
        postal = self.location_postal.text()
        if ((city == '') | (city == u'')):
            if ((postal != '') & (postal != u'')):
                self.municipals = filter(lambda x :  str(x['POSTCODE']).startswith(postal) , self.municipal_information.municipal_db)
                if len(self.municipals) > 0:
                    if len(self.municipals) ==  1:
                        self.lineedit_city_layout(self.municipals[0]['NAME'])
                        self.location_city.setText(self.municipals[0]['NAME'])
                        self.location_city.editingFinished.connect(self.location_by_address, True)
                        pop_dens = '{}'.format(self.municipals[0]['POP_DENS'])
                        self.population_density.setText(pop_dens)
                        avg_yoc = '{}'.format(self.municipals[0]['AVG_YOC'])
                        self.average_build_year.setText(avg_yoc)
                    else:
                        self.combobox_city_layout()
                        for i in [i['POSTCODE']+' '+i['NAME'] for i in self.municipals]:
                            self.location_city.addItem(_fromUtf8(i))
                        self.location_city.currentIndexChanged.connect(self.set_city)
        else:
            if ((city != '') & (city != u'')):
                self.municipals = filter(lambda x : ((x['NAME'] == city) | x['NAME'].startswith(city+',') | x['NAME'].startswith(city+' ')) , self.municipal_information.municipal_db)
                if len(self.municipals) > 0:
                    if len(self.municipals) ==  1:
                        self.lineedit_postal_layout()
                        self.location_postal.setText(str(self.municipals[0]['POSTCODE']))
                        pop_dens = '{}'.format(self.municipals[0]['POP_DENS'])
                        self.population_density.setText(pop_dens)
                        avg_yoc = '{}'.format(self.municipals[0]['AVG_YOC'])
                        self.average_build_year.setText(avg_yoc)
                    else:
                        self.combobox_postal_layout()
                        for i in [i['POSTCODE']+' '+i['NAME'] for i in self.municipals]:
                            self.location_postal.addItem(_fromUtf8(i))
                        self.location_postal.currentIndexChanged.connect(self.set_postal)



    def combobox_city_layout(self, entries=[]):
        location_box = self.gridLayout.findChild(QtGui.QHBoxLayout, 'location_city_layout')
        city_edit = location_box.itemAt(0).widget()

        if isinstance(city_edit, QtGui.QLineEdit):
            location_box.removeWidget(city_edit)
            width = city_edit.minimumWidth()
            city_edit.deleteLater()
            self.location_city = QtGui.QComboBox(self.form)
            self.location_city.setObjectName(_fromUtf8("location_city"))
            self.location_city.setMinimumWidth(width)
            location_box.insertWidget(0, self.location_city)


    def lineedit_city_layout(self, text=''):
        location_box = self.gridLayout.findChild(QtGui.QHBoxLayout, 'location_city_layout')
        city_edit = location_box.itemAt(0).widget()

        if isinstance(city_edit, QtGui.QComboBox):
            location_box.removeWidget(city_edit)
            city_edit.deleteLater()
            self.location_city = QtGui.QLineEdit(self.form)
            self.location_city.setMinimumWidth(228)
            self.location_city.setObjectName(_fromUtf8("location_city"))
            self.location_city.setStyleSheet('color: rgb(0,0,0)')
            location_box.insertWidget(0, self.location_city)



    def set_postal(self, index):
        municipal = self.municipals[index]
        self.lineedit_postal_layout()
        self.location_postal.setText(str(municipal['POSTCODE']))
        pop_dens = '{}'.format(municipal['POP_DENS'])
        self.population_density.setText(pop_dens)
        avg_yoc = '{}'.format(municipal['AVG_YOC'])
        self.average_build_year.setText(avg_yoc)

    def combobox_postal_layout(self, entries=[]):
        location_box = self.gridLayout.findChild(QtGui.QHBoxLayout, 'location_postal_layout')
        location_edit = location_box.itemAt(0).widget()

        if isinstance(location_edit, QtGui.QLineEdit):
            location_box.removeWidget(location_edit)
            width = location_edit.minimumWidth()
            location_edit.deleteLater()
            self.location_postal = QtGui.QComboBox()
            self.location_postal.setObjectName('location_postal')
            self.location_postal.setMinimumWidth(width)
            location_box.insertWidget(0, self.location_postal)

    def lineedit_postal_layout(self, text=''):
        location_box = self.gridLayout.findChild(QtGui.QHBoxLayout, 'location_postal_layout')
        location_edit = location_box.itemAt(0).widget()

        if isinstance(location_edit, QtGui.QComboBox):
            location_box.removeWidget(location_edit)
            location_edit.deleteLater()
            self.location_postal = QtGui.QLineEdit(self.form)
            self.location_postal.setMinimumWidth(228)
            self.location_postal.setObjectName(_fromUtf8("location_postal"))
            self.location_postal.setStyleSheet('color: rgb(0,0,0)')
            location_box.insertWidget(0, self.location_postal)



class ModularInfo_dialog(QtGui.QDialog, Ui_ModularInfo_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


class Modular_dialog(QtGui.QDialog, Ui_Modular_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setContentsMargins(500, 500, 0, 0)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.help_dialog = ModularInfo_dialog()
        self.buttonBox.button(QtGui.QDialogButtonBox.Help).clicked.connect(self.help_dialog.show)

    def set_dialog_text(self, text, title=""):

        if not title.isspace():
            self.setWindowTitle(title)

        if text is not None and not text.isspace():

            html_prefix = ('<p align="center" style=" margin-top:0px; margin-bottom:0px; '
                           'margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">')

            html_postfix = "</p>"
            browser_text = html_prefix + text + html_postfix
            self.textBrowser.setHtml(QtGui.QApplication.translate('InvestigationAreaSelected_dialog', browser_text, None))


class RequestWmsUrl_dialog(QtGui.QDialog, Ui_RequestWmsUrl_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)


class EstimatedEnergyDemand_dialog(QtGui.QDialog, Ui_EstimatedEnergyDemand_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        layer_dict = QgsMapLayerRegistry.instance().mapLayers()
        vector_layers = filter(lambda x: x.type() == QgsMapLayer.VectorLayer, layer_dict.values())
        for layer in vector_layers:
            self.input_layer.addItem(layer.name())
            self.output_layer.addItem(layer.name())

        self.input_layer.currentIndexChanged.connect(self.update_field_dropdowns)

    def update_field_dropdowns(self, index):
        layer = layer_interaction.find_layer_by_name(self.input_layer.currentText())
        provider = layer.dataProvider()
        fields = provider.fieldNameMap().keys()
        self.area.clear()
        self.perimeter.clear()
        self.height.clear()
        self.floors.clear()
        self.yoc.clear()

        for field in fields:
            self.area.addItem(field)
            self.perimeter.addItem(field)
            self.height.addItem(field)
            self.floors.addItem(field)
            self.yoc.addItem(field)
