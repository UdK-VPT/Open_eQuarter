import os
import json

from zipfile import ZipFile
from PyQt4.QtGui import QListView, QStandardItemModel, QStandardItem
from PyQt4.QtCore import QSize

from mole.project import config
from mole.view.oeq_ui_classes import QProcessViewDelegate


class ProgressItemsModel():

    def __init__(self):
        self.section_views = []
        self.load_section_models(config.progress_model)

    def load_section_models(self, path):
        """
        Open every sectionX.json-file in the given directory and build the QStandardItemModel-Classes accordingly
        :param path: Directory which contains the .json-files
        :type path: str
        :return:
        :rtype:
        """
        try:
            dir_entries = ZipFile(path).namelist()
            files = filter(lambda entry: entry.startswith('section') and entry.endswith('.json'), dir_entries)
            views = []
            for json_section in files:
                with ZipFile(path, 'r') as oeq_zip:
                    data = oeq_zip.read(json_section)
                    json_data = json.loads(data)

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
                views.append(step_items)

            self.section_views = views
        except IOError, FileNotFoundError:
            print(self.__module__, FileNotFoundError)

    def save_section_models(self, path):
        """
        Save the current progress to a folder calles 'oeq_progress' under the given path
        :param path: Directory which will contain the progress
        :type path: str
        :return:
        :rtype:
        """
        default_progress = os.path.join(config.plugin_dir, 'project', 'default_progress')
        path = os.path.join(path, 'oeq_progress.oeq')
        if os.path.exists(path):
            os.remove(path)

        for i in range(1, 6):
            model = self.section_views[i-1].model()
            json_file = os.path.join(default_progress, 'section{}.json'.format(i))
            with open(json_file, "r") as jsonFile:
                json_data = json.load(jsonFile)

            for j, step in enumerate(json_data['steplist']):
                    step['state'] = model.item(j).checkState()

            print(json.dumps(json_data))

            with ZipFile(path, 'a') as oeq_zip:
                oeq_zip.writestr('section{}.json'.format(i), json.dumps(json_data))

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