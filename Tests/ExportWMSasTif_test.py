from unittest import TestCase
from qgis.core import *
from PyQt4 import QtCore
from QgisTestInterface import QgisTestInterface


class ExportWMSasTif_test(TestCase):

    def __init__(self, testName, iface = QgisTestInterface()):
        super(ExportWMSasTif_test, self).__init__(testName)
        self.iface = iface
        self.layer_list = []

    def setUp(self):
        QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/MacOS', True)
        QgsApplication.initQgis()

        if len(QgsProviderRegistry.instance().providerList()) == 0:
            raise RuntimeError('No data providers available.')

        self.layer_list = []

        QtCore.QCoreApplication.setOrganizationName('QGIS')
        QtCore.QCoreApplication.setApplicationName('QGIS2')

    def tearDown(self):
        for layer_name in self.layer_list:
            layer = QgsMapLayerRegistry.instance().mapLayersByName(layer_name)
            if( len(layer) == 1):
                QgsMapLayerRegistry.instance().removeMapLayer(layer[0].id())
        QgsApplication.exitQgis

    def test_export(self):
        self.fail()


    #ToDo
    def test_get_geo_data(self):
        self.fail()

    def test_create_multiple_rasters(self):
        self.fail()

    def test_save_image(self):
        self.fail()

    def test_add_geo_reference(self):
        self.fail()

    def test_build_pyramids(self):
        self.fail()