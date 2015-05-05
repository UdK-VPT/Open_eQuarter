import io
import os
import json

from collections import OrderedDict
from PyQt4.QtGui import QListView, QStandardItemModel, QStandardItem
from PyQt4.QtCore import QSize

from mole.project import config
from mole.view.oeq_ui_classes import QProcessViewDelegate

class ProgressModel(object):
    def __init__(self, save_file='default'):

        # has to be -1, so the first step (counting from 0) is executed first
        self.last_step_executed = -1

        if save_file == 'default':
            self._project_basics = OrderedDict([('ol_plugin_installed', False), ('pst_plugin_installed', False), ('project_created', False), ('osm_layer_loaded', False)])
            self._investigation_area = OrderedDict([('temp_shapefile_created', False), ('editing_temp_shapefile_started', False), ('investigation_area_selected', False), ('editing_temp_shapefile_stopped', False)])
            self._building_shapes = OrderedDict([('housing_layer_loaded', False), ('building_coordinates_loaded', False)])
            self._real_estate_cadaster = OrderedDict([('raster_loaded', False), ('extent_clipped', False), ('legend_created', False)])
            self._sampling_points = OrderedDict([('temp_pointlayer_created', False), ('editing_temp_pointlayer_started', False), ('points_of_interest_defined', False), ('editing_temp_pointlayer_stopped', False), ('information_sampled', False)])
            self._progress = OrderedDict([('project_basics', self._project_basics), ('investigation_area', self._investigation_area), ('building_shapes', self._building_shapes), ('real_estate_cadaster', self._real_estate_cadaster), ('sampling_points', self._sampling_points)])
        # else:
            # check if the given config-file exists

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
            self._progress[section][step] = is_done
            self.last_step_executed = self.get_position_of_step(step)

        except KeyError, Error:
            print(Error)

    def prerequisites_are_given(self, step):
        """
        Check if each predecessor within the section of the given step was set to 'True'
        :param step: The name of the step whose prerequisites/predecessors shall be checked
        :type step: str
        :return: If all steps prior to the given step are set to True
        :rtype: bool
        """
        position = self.get_position_of_step(step)

        # since the first step (at position 0) has no prerequisites, True can be returned
        if position == 0:
            return True

        prerequisite_boolean_list = self.get_progress_list()
        prerequisites_given = True

        while prerequisites_given and position > 0:
            position -= 1
            prerequisites_given = prerequisite_boolean_list[position]

        return prerequisites_given

    def get_position_of_step(self, step):
        """
        Returns the position of the step within the progress. The position refers to the order in which the steps shall be executed.
        :param step: Name of the step
        :type step: str
        :return: The order number of the step
        :rtype: int
        """
        position = 0
        pages = self._progress.values()

        for steps in pages:
            for current_step in steps.keys():
                if current_step == step:
                    return position
                else:
                    position += 1

    def get_progress_list(self):
        """
        Resolve the separation into sections and return a list of the booleans corresponding to each step.
        :return: A list containing the booleans related to every step
        :rtype: list
        """
        progress = []

        sections = self._progress.values()

        for steps in sections:
            progress += steps.values()

        return progress

    def get_step_list(self):
        """
        Resolve the separation into sections and return a list containing each step.
        :return: A list containing every step
        :rtype: list
        """

        steps = []
        sections = self._progress.values()

        for step_list in sections:
            steps += step_list
        
        return steps

    def is_section_done(self, section_name):
        """
        Check if all steps within a section are set to True.
        :param section_name: The name of the section
        :type section_name: str
        :return: If all steps in the given section are done.
        :rtype: bool
        """
        section = self._progress[section_name]
        section_last_ele = section.keys()[-1]
        section_end = self.get_position_of_step(section_last_ele)
        section_start = section_end - len(section) + 1

        step_done = self.get_progress_list()
        is_done = True

        # initially compare with True, if one step is set to False, is_done will be set to false as well and won't be set back to True again
        for i in range(section_start, section_end+1):
            is_done = step_done[i] and is_done

        return is_done

    def is_step_done(self, step):
        """
        Check if the given step is set to true.
        :param step:
        :type step:
        :return:
        :rtype:
        """
        return self.get_progress_list()[self.get_position_of_step(step)]


class ProgressItemsModel():
    def __init__(self):
        self.section_views = []
        self.load_section_models(config.progress_model)

    def load_section_models(self, path):
        try:
            dir_entries = map(lambda entry: os.path.join(path, entry), os.listdir(path))
            files = filter(lambda entry: os.path.isfile(entry) and entry.endswith('.json'), dir_entries)

            for json_section in files:
                data = io.open(json_section)
                json_data = json.load(data)

                step_items = QListView()
                step_items.setItemDelegate(QProcessViewDelegate(step_items))
                step_items.setAccessibleName(json_data['description'])
                step_items.setGridSize(QSize(320,40))
                step_items.setSpacing(5)
                section_model = QStandardItemModel(step_items)

                for step in json_data['steplist']:
                    item = QStandardItem(step['description'])
                    item.setCheckable(True)
                    item.setTristate(True)
                    item.setEditable(False)
                    item.setAccessibleText(step['step_name'])
                    item.setCheckState(step['state'])
                    section_model.appendRow(item)

                step_items.setModel(section_model)
                self.section_views.append(step_items)

                data.close()

        except IOError, FileNotFoundError:
            print(self.__module__, FileNotFoundError)

    def check_prerequisites_of(self, step_name):
        """
        Check whether every previous step has a checkState of 2 (including steps in previous models)
        :param step_name: Name of the step to which the process is checked
        :type step_name: str
        :return: Whether the predecessing steps have a checkState of 2
        :rtype: bool
        """
        first_section = self.section_views[0].model()
        if step_name == first_section.item(0).accessibleText():
            return True

        prereq_given = True
        for view in self.section_views:
            section = view.model()

            i = 0
            while section.item(i) and prereq_given:
                item = section.item(i)
                if step_name == item.accessibleText():
                    return prereq_given
                else:
                    item_done = True if item.checkState() == 2 else False
                    prereq_given = prereq_given and item_done
                    i += 1

            if not prereq_given:
                return False