from collections import OrderedDict

from PyQt4 import QtCore, QtGui

from Open_eQuarter.view.qt.ui_main_process_dock import Ui_MainProcess_dock, _fromUtf8


class MainProcess_dock(QtGui.QDockWidget, Ui_MainProcess_dock):

    def __init__(self):
        QtGui.QDockWidget.__init__(self)
        self.setupUi(self)
        self.selection_to_page = OrderedDict([])
        self._check_mark = QtGui.QPixmap(_fromUtf8(":/Icons/Icons/checkmark.png"))
        self._open_mark = QtGui.QPixmap(_fromUtf8(":/Icons/Icons/openmark.png"))

        page_triples = []

        # put each page-widget in a list of triples, as they are not sorted properly
        for page in self.process_page.children():
            if isinstance(page, QtGui.QWidget):
                index = self.process_page.indexOf(page)
                page_triples.append((index, page.accessibleName(), page))

        page_triples_sorted = sorted(page_triples, key=lambda tup: tup[0])
        self.selection_to_page = OrderedDict(map(lambda trip: trip[1:], page_triples_sorted))


        # add page-names to according position in dropdown-menu, so the user can navigate through the process
        for page_number, page in enumerate(self.selection_to_page.keys()):
            self.active_page_dropdown.addItem(page)
            self.active_page_dropdown.setItemData(page_number, self._open_mark, QtCore.Qt.DecorationRole)

        self.active_page_dropdown.currentIndexChanged.connect(lambda: self.go_to_page(self.active_page_dropdown.currentText()))

        # set the currently displayed widget to the first process-page, otherwise the correct display is not guaranteed
        self.process_page.setCurrentWidget(self.selection_to_page.values()[0])

    def go_to_page(self, selection_name):
        [self.process_page.setCurrentWidget(page)
         for page in self.selection_to_page.values() if selection_name == page.accessibleName()]

    def set_checkbox_on_page(self, checkbox_name, page_name, check_yes_no):
        if isinstance(check_yes_no, bool):
            page = self.findChild(QtGui.QWidget, page_name)
            checkbox = page.findChild(QtGui.QPushButton, checkbox_name)

            if checkbox:
                checkbox.setChecked(check_yes_no)

    def is_checkbox_on_page_checked(self, checkbox_name, page_name):
        page = self.process_page.findChild(QtGui.QWidget, page_name)
        return page.findChild(QtGui.QPushButton, checkbox_name).isChecked()

    def set_current_page_done(self, value):
        if isinstance(value, bool):
            page_name = self.active_page_dropdown.currentText()
            page = self.selection_to_page[page_name]

            if (page_name) == page.accessibleName():
                index = self.active_page_dropdown.currentIndex()
                self.active_page_dropdown.setItemData(index, self._check_mark, QtCore.Qt.DecorationRole)
                self.active_page_dropdown.setCurrentIndex((index+1) % len(self.selection_to_page))


