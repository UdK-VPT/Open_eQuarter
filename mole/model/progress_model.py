import io
import os
import json

from PyQt4.QtGui import QListView, QStandardItemModel, QStandardItem
from PyQt4.QtCore import QSize

from mole.project import config
from mole.view.oeq_ui_classes import QProcessViewDelegate


class ProgressItemsModel():
    def __init__(self):
        self.section_views = []
        self.load_section_models(config.progress_model)

    def load_section_models(self, path):
        try:
            dir_entries = map(lambda entry: os.path.join(path, entry), os.listdir(path))
            files = filter(lambda entry: os.path.isfile(entry) and entry.endswith('.json'), dir_entries)

            for json_section in files:
                data = io.open(json_section)
                json_data = json.load(data)

                step_items = QListView()
                step_items.setItemDelegate(QProcessViewDelegate(step_items))
                step_items.setAccessibleName(json_data['description'])
                step_items.setGridSize(QSize(320,40))
                step_items.setSpacing(5)
                section_model = QStandardItemModel(step_items)

                for step in json_data['steplist']:
                    item = QStandardItem(step['description'])
                    item.setCheckable(True)
                    item.setTristate(True)
                    item.setEditable(False)
                    item.setAccessibleText(step['step_name'])
                    item.setCheckState(step['state'])
                    section_model.appendRow(item)

                step_items.setModel(section_model)
                self.section_views.append(step_items)

                data.close()

        except IOError, FileNotFoundError:
            print(self.__module__, FileNotFoundError)

    def check_prerequisites_for(self, step_name):
        """
        Check whether every previous step has a checkState of 2 (including steps in previous models)
        :param step_name: Name of the step to which the process is checked
        :type step_name: str
        :return: The first item, which does not have a checkState of 2
        :rtype: QStandardItem
        """
        first_section = self.section_views[0].model()
        item = first_section.item(0)
        item_name = item.accessibleText()
        if step_name == item_name:
            return item

        prereq_given = True
        for view in self.section_views:
            section = view.model()

            i = 0
            while section.item(i) and prereq_given:
                item = section.item(i)
                item_name = item.accessibleText()
                if step_name == item_name:
                    return item
                else:
                    item_done = True if item.checkState() == 2 else False
                    prereq_given = prereq_given and item_done
                    i += 1

            if not prereq_given:
                return item