from unittest import TestCase
import atexit

from qgis.core import *
from qgis.gui import *
from qgis.utils import initInterface, iface
from PyQt4 import QtCore
from mole.open_equarter_main import OpenEQuarterMain

class OpenEQuarterMain_test(TestCase):

    def setUp(self):

        QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/MacOS', True)
        QgsApplication.initQgis()

        if len(QgsProviderRegistry.instance().providerList()) == 0:
            raise RuntimeError('No data providers available.')

        QtCore.QCoreApplication.setOrganizationName('QGIS')
        QtCore.QCoreApplication.setApplicationName('QGIS2')
        QgsApplication
        initInterface()
        self.iface = iface

    def test_init(self):
        OpenEQuarterMain(self.iface)