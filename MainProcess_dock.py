from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from ui_main_process_dock import Ui_MainProcess_dock, _fromUtf8
from ui_process_button import QProcessButton

class MainProcess_dock(QtGui.QDockWidget, Ui_MainProcess_dock):

    def __init__(self):
        QtGui.QDockWidget.__init__(self)

        self.setupUi(self)
        self._selection_to_page = {}
        self._check_mark = QtGui.QPixmap(_fromUtf8(":/Icons/Icons/checkmark.png"))
        self._open_mark = QtGui.QPixmap(_fromUtf8(":/Icons/Icons/openmark.png"))

        page_list = []
        for page_name in self.process_page.children():
            if isinstance(page_name, QtGui.QWidget):
                self._selection_to_page[page_name.accessibleName()] = page_name
                page_list.append(page_name.accessibleName())


        # add page-names to according position in dropdown-menu, so the user can navigate through the process
        # connect each QProcessButton, so _progress-steps can be triggered seperately
        for page_number, page_name in enumerate(reversed(page_list)):
            self.active_page_dropdown.addItem(page_name)
            self.active_page_dropdown.setItemData(page_number, self._open_mark, QtCore.Qt.DecorationRole)

            page = self._selection_to_page[page_name]
            for button in page.children():
                if isinstance(button, QProcessButton):
                    self.connect(button, SIGNAL('step_clicked'), self.print_received)


        self.active_page_dropdown.currentIndexChanged.connect(lambda: self.go_to_page(self.active_page_dropdown.currentText()))


    def go_to_page(self, selection_name):

        if selection_name is not None and not selection_name.isspace():

            for selection in self._selection_to_page:
                page = self._selection_to_page[selection]

                if (selection_name) == page.accessibleName():
                    self.process_page.setCurrentWidget(page)
                    break

    def print_received(self, *args):
        print 'Got signal from sender: ' + args[0]
        print '({})'.format(args[1])

    def set_checkbox_on_page(self, checkbox_name, page_name, check_yes_no):

        if not checkbox_name or checkbox_name.isspace():
            print "A checkbox with the given name " + checkbox_name + " was not found."

        elif not page_name or page_name.isspace():
            print "A page with the given name " + page_name + " was not found."

        elif isinstance(check_yes_no, bool):
            print "Received: {}, expected: bool".format(type(check_yes_no))

        else:
            page = self.findChild(QtGui.QWidget, page_name)
            checkbox = page.findChild(QtGui.QPushButton, checkbox_name)

            if checkbox:
                checkbox.setChecked(check_yes_no)

    def is_checkbox_on_page_checked(self, checkbox_name, page_name):

        if not checkbox_name or checkbox_name.isspace():
            print "A checkbox with the given name " + checkbox_name + " was not found."

        elif not page_name or page_name.isspace():
            print "A page with the given name " + page_name + " was not found."

        else:
            page = self.process_page.findChild(QtGui.QWidget, page_name)
            return page.findChild(QtGui.QPushButton, checkbox_name).isChecked()

    def set_page_done(self, value):

        if isinstance(value, bool):
            print "A boolean value has to be passed as a third parameter."

        else:
            page_name = self.active_page_dropdown.currentText()
            page = self._selection_to_page[page_name]

            if (page_name) == page.accessibleName():
                index = self.active_page_dropdown.currentIndex()
                self.active_page_dropdown.setItemData(index, self._check_mark, QtCore.Qt.DecorationRole)
                self.active_page_dropdown.setCurrentIndex((index+1) % len(self._selection_to_page))


