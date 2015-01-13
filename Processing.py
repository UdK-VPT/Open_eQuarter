
class Processing(object):

    def __init__(self, main_dialog):

        ### Information regarding the users progress
        # list that captures the progress of the oeq-process
        self.progress = {'project_basics': {'ol_plugin_installed': False, 'pst_plugin_installed': False, 'project_created': False, 'osm_layer_loaded': False},
                         'investigation_area': {'temp_shapefile_created': False, 'editing_temp_shapefile_started': False, 'investigation_area_selected': False, 'editing_temp_shapefile_stopped': False},
                         'building_shapes': {'raster_loaded': False, 'extent_clipped': False, 'pyramids_built': False},
                         'sampling_points': {'temp_pointlayer_created': False, 'editing_temp_pointlayer_started': False, 'points_of_interest_defined': False, 'editing_temp_pointlayer_stopped': False, 'information_sampled': False }}

        self.mainstay_process_dlg = main_dialog

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

    def calculate_progress(self):

        try:
            current_step = 0
            for group in self.progress:
                for step_completed in self.progress[group]:
                    current_step += self.progress[group][step_completed]

            return current_step
        except KeyError, error:
            print str(error)
            return -1