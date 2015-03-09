import unittest
import sys

from PyQt4.QtGui import QGridLayout, QWidget, QApplication, QLabel, QLineEdit

from Open_eQuarter.view.oeq_ui_classes import QResponsiveGridLayout


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
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

        grid.remove_roe(2)


if __name__ == '__main__':
    unittest.main()
