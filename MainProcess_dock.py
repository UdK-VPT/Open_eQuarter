from PyQt4 import QtCore, QtGui
from ui_main_process_dock import Ui_MainProcess_dock, _fromUtf8

class MainProcess_dock(QtGui.QDockWidget, Ui_MainProcess_dock):

    def __init__(self):
        QtGui.QDockWidget.__init__(self)

        self.setupUi(self)
        self.selection_to_page = {}
        self.check_mark = QtGui.QPixmap(_fromUtf8(":/Icons/Icons/checkmark.png"))
        self.open_mark = QtGui.QPixmap(_fromUtf8(":/Icons/Icons/openmark.png"))

        page_list = []
        for page in self.process_page.children():
            if type(page) is QtGui.QWidget:
                self.selection_to_page[page.accessibleName()] = page
                page_list.append(page.accessibleName())

        page_list.reverse()

        for i in range(0, len(page_list)):
            self.active_page_dropdown.addItem(page_list[i])
            self.active_page_dropdown.setItemData(i, self.open_mark, QtCore.Qt.DecorationRole)

        self.active_page_dropdown.currentIndexChanged.connect(lambda: self.go_to_page(self.active_page_dropdown.currentText()))

    def set_checkbox_on_page(self, checkbox_name, page_name, check_yes_no):

        if not checkbox_name or checkbox_name.isspace():
            print "A checkbox with the given name " + checkbox_name + " was not found."

        elif not page_name or page_name.isspace():
            print "A page with the given name " + page_name + " was not found."

        elif type(check_yes_no) is not bool:
            print "A boolean check_yes_no has to be passed as a third parameter."

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

        if type(value) is not bool:
            print "A boolean value has to be passed as a third parameter."

        else:
            page_name = self.active_page_dropdown.currentText()
            page = self.selection_to_page[page_name]

            if (page_name) == page.accessibleName():
                index = self.active_page_dropdown.currentIndex()
                self.active_page_dropdown.setItemData(index, self.check_mark, QtCore.Qt.DecorationRole)
                self.active_page_dropdown.setCurrentIndex((index+1) % len(self.selection_to_page))

    def go_to_page(self, selection_name):

        if selection_name is not None and not selection_name.isspace():

            for selection in self.selection_to_page:
                page = self.selection_to_page[selection]

                if (selection_name) == page.accessibleName():
                    self.process_page.setCurrentWidget(page)
                    break

