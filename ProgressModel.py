from collections import OrderedDict


class ProgressModel(object):
    def __init__(self, save_file='default'):

        if save_file == 'default':
            self._project_basics = OrderedDict([('ol_plugin_installed', False), ('pst_plugin_installed', False), ('project_created', False), ('osm_layer_loaded', False)])
            self._investigation_area = OrderedDict([('temp_shapefile_created', False), ('editing_temp_shapefile_started', False), ('investigation_area_selected', False), ('editing_temp_shapefile_stopped', False)])
            self._building_shapes = OrderedDict([('raster_loaded', False), ('extent_clipped', False), ('pyramids_built', False)])
            self._sampling_points = OrderedDict([('temp_pointlayer_created', False), ('editing_temp_pointlayer_started', False), ('points_of_interest_defined', False), ('editing_temp_pointlayer_stopped', False), ('information_sampled', False)])
            self._progress = OrderedDict([('project_basics', self._project_basics), ('investigation_area', self._investigation_area), ('building_shapes', self._building_shapes), ('sampling_points', self._sampling_points)])
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
        except KeyError, error:
            print error.message

    def prerequisites_are_given(self, step):
        position = self.get_position_of_step(step)

        if position == 0:
            return True

        prerequisite_boolean_list = self.get_progress_list()
        prerequisites_given = True

        while prerequisites_given and position > 0:
            position -= 1
            prerequisites_given = prerequisite_boolean_list[position]

        return prerequisites_given

    def get_position_of_step(self, step):
        position = 0
        pages = self._progress.values()

        for steps in pages:
            for current_step in steps.keys():
                if current_step == step:
                    return position
                else:
                    position += 1

    def get_progress_list(self):
        progress = []

        pages = self._progress.values()

        for steps in pages:
            for current_step in steps.values():
                progress.append(current_step)

        return progress

    def is_section_done(self, section_name):
        section = self._progress[section_name]
        section_last_ele = section.keys()[-1]
        section_end = self.get_position_of_step(section_last_ele)
        section_start = section_end - len(section) + 1

        step_done = self.get_progress_list()
        is_done = True

        for i in range(section_start, section_end):
            is_done = step_done[i] and is_done

        return is_done

    def is_step_done(self, step):
        return self.get_progress_list()[self.get_position_of_step(step)]
