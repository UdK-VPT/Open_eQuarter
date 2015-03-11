import unittest
import sys

from PyQt4.QtGui import QGridLayout, QWidget, QApplication, QLabel, QLineEdit

class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.app = QApplication(sys.argv)
        except:
            cls.fail('It was not possible to instantiate a QApplication.')

    def setUp(self):
        self.widget = QWidget()

if __name__ == '__main__':
    unittest.main()
