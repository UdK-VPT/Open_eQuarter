import unittest
import sys

from PyQt4.QtGui import QWidget, QApplication, qApp

from Open_eQuarter.model.grid_matrix import WidgetLinkedListNode, WidgetLinkedList


class GridMatrixModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.app = QApplication(sys.argv)
        except:
            cls.fail('It was not possible to instantiate a QApplication.')

    def test_if_row_of_widgets_can_be_created(self):
        row = WidgetLinkedListNode()
        self.assertEqual(len(row.widgets), 0)

    def test_if_widgets_can_be_added_and_removed(self):
        row = WidgetLinkedListNode()
        wid1 = QWidget()
        wid2 = QWidget()
        wid3 = QWidget()
        row.add_widget(wid1)
        row.add_widget(wid2)
        row.add_widget(wid3)
        self.assertEqual(len(row.widgets), 3)
        self.assertEqual(row.widgets, [wid1, wid2, wid3])

        row.remove_widget(wid2)
        self.assertEqual(len(row.widgets), 2)

    def test_if_list_of_widget_rows_can_be_created(self):
        row_list = WidgetLinkedList()
        self.assertIsInstance(row_list, WidgetLinkedList)

    def test_if_nodes_can_be_added_and_removed(self):
        row_list = WidgetLinkedList()

        row_list = WidgetLinkedList()

        row1 = WidgetLinkedListNode()
        wid1 = QWidget()
        row1.add_widget(wid1)
        row_list.add_node(row1)

        row2 = WidgetLinkedListNode()
        wid2 = QWidget()
        row2.add_widget(wid2)
        row_list.add_node(row2)

        row3 = WidgetLinkedListNode()
        wid3 = QWidget()
        row3.add_widget(wid3)
        row_list.add_node(row3)

        row4 = WidgetLinkedListNode()
        wid4 = QWidget()
        row4.add_widget(wid4)
        row_list.add_node(row4)

        row5 = WidgetLinkedListNode()
        wid5 = QWidget()
        row5.add_widget(wid5)

        row6 = WidgetLinkedListNode()
        wid6 = QWidget()
        row6.add_widget(wid6)

        self.assertEqual(row_list._head, row1)
        self.assertEqual(row_list._head.next, row2)
        self.assertEqual(row_list._head.next.next, row3)
        self.assertEqual(row_list._head.next.next.next, row4)
        self.assertEqual(row_list._size, 4)

        row_list.remove_node(row1)
        self.assertEqual(row_list._head, row2)
        self.assertEqual(row_list._head.next, row3)
        self.assertEqual(row_list._size, 3)

        row_list.remove_node(row4)
        self.assertEqual(row_list._head, row2)
        self.assertEqual(row_list._head.next, row3)
        self.assertIsNone(row_list._head.next.next)
        self.assertEqual(row_list._size, 2)

        row_list.add_node(row5)
        row_list.add_node(row6)
        self.assertEqual(row_list._head, row2)
        self.assertEqual(row_list._head.next, row3)
        self.assertEqual(row_list._head.next.next, row5)
        self.assertEqual(row_list._head.next.next.next, row6)
        self.assertEqual(row_list._size, 4)

        row_list.remove_node(row2)
        self.assertEqual(row_list._head, row3)
        self.assertEqual(row_list._head.next, row5)
        self.assertEqual(row_list._head.next.next, row6)
        self.assertIsNone(row_list._head.next.next.next)
        self.assertEqual(row_list._size, 3)

        row_list.remove_node(row6)
        self.assertEqual(row_list._head, row3)
        self.assertEqual(row_list._head.next, row5)
        self.assertIsNone(row_list._head.next.next)
        self.assertEqual(row_list._size, 2)

    def test_if_list_returns_correct_node_by_index(self):
        row_list = WidgetLinkedList()

        row1 = WidgetLinkedListNode()
        wid1 = QWidget()
        row1.add_widget(wid1)
        row_list.add_node(row1)

        row2 = WidgetLinkedListNode()
        wid2 = QWidget()
        row2.add_widget(wid2)
        row_list.add_node(row2)

        row3 = WidgetLinkedListNode()
        wid3 = QWidget()
        row3.add_widget(wid3)
        row_list.add_node(row3)

        row4 = WidgetLinkedListNode()
        wid4 = QWidget()
        row4.add_widget(wid4)
        row_list.add_node(row4)

        node = row_list.get_node_at_position(0)
        self.assertEqual(node, row1)

        node = row_list.get_node_at_position(1)
        self.assertEqual(node, row2)

        node = row_list.get_node_at_position(2)
        self.assertEqual(node, row3)

        row_list.remove_node(node)
        node = row_list.get_node_at_position(2)
        self.assertEqual(node, row4)

        row_list.remove_node(row1)
        node = row_list.get_node_at_position(1)
        self.assertEqual(node, row4)
        node = row_list.get_node_at_position(0)
        self.assertEqual(node, row2)
        node = row_list.get_node_at_position(2)
        self.assertIsNone(node)

if __name__ == '__main__':
    unittest.main()
