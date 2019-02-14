from qgis.core import QgsProject
from qgis.PyQt.QtCore import QFileInfo, QFile

import unittest
import os

from mole3.qgisinteraction import project_interaction
from .qgis_models import set_up_interface

class QgisProjectTest(unittest.TestCase):

    def setUp(self):
        self.qgis_app, self.canvas, self.iface = set_up_interface()
        self.project_path = 'test.qgs'

    def tearDown(self):
        QgsProject.instance().clear()
        if self.qgis_app:
            del(self.qgis_app)

        try:
            os.remove(self.project_path)
        except OSError:
            pass

    def test_if_nonexisting_project_is_recognised(self):
        self.assertFalse(project_interaction.project_exists())

    def test_if_existing_project_is_recognised(self):
        project_file = open(self.project_path, 'w')
        project_file.close()

        QgsProject.instance().setFileName(self.project_path)
        QgsProject.instance().write()
        self.assertTrue(project_interaction.project_exists())

if __name__ == '__main__':
    unittest.main()
