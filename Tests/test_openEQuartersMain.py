from unittest import TestCase
import atexit

from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore

__author__ = 'VPTtutor'


class TestOpenEQuartersMain(TestCase):
    def test_initGui(self):
        QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/MacOS', True)
        QgsApplication.initQgis()

        if len(QgsProviderRegistry.instance().providerList()) == 0:
            raise RuntimeError('No data providers available.')

        QtCore.QCoreApplication.setOrganizationName('QGIS')
        QtCore.QCoreApplication.setApplicationName('QGIS2')

        atexit.register(QgsApplication.exitQgis)
        self.fail()


    """
    def test_create_project_ifNotExists(self):
        self.fail()

    def test_enable_on_the_fly_projection(self):
        self.fail()

    def test_load_osm_layer(self):
        self.fail()

    def test_zoom_to_default_extent(self):
        self.fail()

    def test_create_new_shapefile(self):
        self.fail()

    def test_change_to_edit_mode(self):
        self.fail()

    def test_confirm_selection_of_investigation_area(self):
        self.fail()

    def test_request_wms_layer_url(self):
        self.fail()

    def test_open_wms_as_raster(self):
        self.fail()

    def test_open_add_wms_dialog(self):
        self.fail()

    def test_set_project_crs(self):
        self.fail()

    def test_get_project_crs(self):
        self.fail()

    def test_clip_zoom_to_layer_view_from_raster(self):
        self.fail()

    def test_get_extent_per_feature(self):
        self.fail()

    def test_find_x_min_y_min_x_max_y_max(self):
        self.fail()

    def test_hide_or_remove_layer(self):
        self.fail()

    def test_find_layer_by_name(self):
        self.fail()

    def test_load_housing_layer(self):
        self.fail()

    def test_add_housing_coordinates(self):
        self.fail()

    def test_run(self):
        self.fail()
    """