from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, SIGNAL


class ProgressModel(QObject):

    def __init__(self, save_file='default'):
        QObject.__init__(self)

        if save_file == 'default':
            self.progress = {'project_basics': {'ol_plugin_installed': False, 'pst_plugin_installed': False, 'project_created': False, 'osm_layer_loaded': False},
                             'investigation_area': {'temp_shapefile_created': False, 'editing_temp_shapefile_started': False, 'investigation_area_selected': False, 'editing_temp_shapefile_stopped': False},
                             'building_shapes': {'raster_loaded': False, 'extent_clipped': False, 'pyramids_built': False},
                             'sampling_points': {'temp_pointlayer_created': False, 'editing_temp_pointlayer_started': False, 'points_of_interest_defined': False, 'editing_temp_pointlayer_stopped': False, 'information_sampled': False }}
        #else:
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
            self.progress[section][step] = is_done
            self.emit(SIGNAL('progress_changed'))
        except KeyError, error:
            print str(error)



