import unittest
import sys

from PyQt4.QtGui import QGridLayout, QWidget, QApplication, QLabel, QLineEdit

from Open_eQuarter.view.oeq_ui_classes import QResponsiveGridLayout


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.app = QApplication(sys.argv)
        except:
            cls.fail('It was not possible to instantiate a QApplication.')

    def setUp(self):
        self.widget = QWidget()

    def test_can_add_a_row_to_QResponsiveGrid(self):

        grid = QResponsiveGridLayout(self.widget, 1)
        self.assertIsInstance(grid, QGridLayout)

        table_heading0 = QLabel('')
        table_heading1 = QLabel('Table')
        table_heading2 = QLabel('Heading')
        grid.addWidget(table_heading0, 0, 0)
        grid.addWidget(table_heading1, 0, 1)
        grid.addWidget(table_heading2, 0, 2)
        self.assertEqual(grid.rowCount(), 1)

        row10 = QLabel('1')
        row11 = QLineEdit()
        row12 = QLineEdit()
        grid.add_row(row10, row11, row12)
        self.assertEqual(grid.rowCount(), 2)

        row20 = QLabel('2')
        row21 = QLineEdit()
        row22 = QLineEdit()
        grid.add_row(row20, row21, row22)
        self.assertEqual(grid.rowCount(), 3)

        self.assertEqual(grid.grid_matrix._size, 2)
        widgets1 = grid.grid_matrix._head.widgets
        self.assertEqual(widgets1, [row10, row11, row12])
        widgets2 = grid.grid_matrix._head.next.widgets
        self.assertEqual(widgets2, [row20, row21, row22])

    def test_to_remove_a_row_from_QResponsiveGrid(self):
        grid = QResponsiveGridLayout(self.widget, 1)
        table_heading0 = QLabel('')
        table_heading1 = QLabel('Table')
        table_heading2 = QLabel('Heading')
        grid.addWidget(table_heading0, 0, 0)
        grid.addWidget(table_heading1, 0, 1)
        grid.addWidget(table_heading2, 0, 2)

        row10 = QLabel('1')
        row11 = QLineEdit()
        row12 = QLineEdit()
        grid.add_row(row10, row11, row12)

        row20 = QLabel('2')
        row21 = QLineEdit()
        row22 = QLineEdit()
        grid.add_row(row20, row21, row22)
        self.assertIsNotNone(grid.itemAtPosition(2,0))
        self.assertIsNotNone(grid.itemAtPosition(2,1))
        self.assertIsNotNone(grid.itemAtPosition(2,2))
        grid.remove_row(1)
        self.assertIsNone(grid.itemAtPosition(2,0))
        self.assertIsNone(grid.itemAtPosition(2,1))
        self.assertIsNone(grid.itemAtPosition(2,2))
        self.assertEqual(grid.grid_matrix._size, 1)

    def test_to_repopulate_QResponsiveGrid_from_grid_matrix(self):

        grid = QResponsiveGridLayout(self.widget, 1)
        self.assertIsInstance(grid, QGridLayout)

        table_heading0 = QLabel('')
        table_heading1 = QLabel('Table')
        table_heading2 = QLabel('Heading')
        grid.addWidget(table_heading0, 0, 0)
        grid.addWidget(table_heading1, 0, 1)
        grid.addWidget(table_heading2, 0, 2)

        row10 = QLabel('1')
        row10.setAccessibleName('rownumber')
        row11 = QLineEdit()
        row12 = QLineEdit()
        grid.add_row(row10, row11, row12)

        row20 = QLabel('2')
        row20.setAccessibleName('rownumber')
        row21 = QLineEdit()
        row22 = QLineEdit()
        grid.add_row(row20, row21, row22)

        row30 = QLabel('3')
        row30.setAccessibleName('rownumber')
        row31 = QLineEdit()
        row32 = QLineEdit()
        grid.add_row(row30, row31, row32)

        row40 = QLabel('4')
        row40.setAccessibleName('rownumber')
        row41 = QLineEdit()
        row42 = QLineEdit()
        grid.add_row(row40, row41, row42)

        row50 = QLabel('5')
        row50.setAccessibleName('rownumber')
        row51 = QLineEdit()
        row52 = QLineEdit()
        grid.add_row(row50, row51, row52)

        row60 = QLabel('6')
        row60.setAccessibleName('rownumber')
        row61 = QLineEdit()
        row62 = QLineEdit()
        grid.add_row(row60, row61, row62)

        # remove widget 3
        grid.remove_row(2)
        self.assertIsNone(grid.itemAtPosition(3,0))
        self.assertIsNone(grid.itemAtPosition(3,1))
        self.assertIsNone(grid.itemAtPosition(3,2))
        self.assertIsNotNone(grid.itemAtPosition(6,0))
        self.assertIsNotNone(grid.itemAtPosition(6,1))
        self.assertIsNotNone(grid.itemAtPosition(6,2))
        grid.repopulate()
        self.assertIsNotNone(grid.itemAtPosition(3,0))
        self.assertIsNotNone(grid.itemAtPosition(3,1))
        self.assertIsNotNone(grid.itemAtPosition(3,2))
        self.assertIsNone(grid.itemAtPosition(6,0))
        self.assertIsNone(grid.itemAtPosition(6,1))
        self.assertIsNone(grid.itemAtPosition(6,2))



if __name__ == '__main__':
    unittest.main()
