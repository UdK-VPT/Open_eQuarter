import os
import json
import pickle

from zipfile import ZipFile
from PyQt4.QtGui import QListView, QStandardItemModel, QStandardItem
from PyQt4.QtCore import QSize

from mole.project.config import progress_model
from mole.view.oeq_ui_classes import QProcessViewDelegate
from mole import oeq_global
from mole import extensions
print extensions.__all__

class ProgressItemsModel:

    def __init__(self):
        self.section_views = []
        self.load_section_models(progress_model)

    def load_section_models(self, path):
        """
        Open every section<Number>.json-file in the given zipfile and build the QStandardItemModel-Classes accordingly
        Open the project_info.json if available and restore the project info
        :param path: Zipfile which contains the .json-files
        :type path: str
        :return:
        :rtype:
        """
        try:
            dir_entries = ZipFile(path).namelist()
            section_files = filter(lambda entry: entry.startswith('section') and entry.endswith('.json'), dir_entries)
            views = []
            for json_section in section_files:
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

            if 'project_info.json' in dir_entries:
                with ZipFile(path, 'r') as oeq_zip:
                    data = oeq_zip.read('project_info.json')
                    json_data = json.loads(data)

                for key in oeq_global.OeQ_project_info.keys():
                    oeq_global.OeQ_project_info[key] = json_data[key]

        except IOError, FileNotFoundError:
            print(self.__module__, FileNotFoundError)

        extensions.load()
        print [i.layer_name for i in oeq_global.OeQ_ExtensionRegistry]

    def save_oeq_project(self):
        """
        Save the current progress and the project info to a zip-file called <project_name>.oeq under the given path
        :param path: Directory which will contain the progress
        :type path: str
        :return:
        :rtype:
        """
        try:
            plugin_path = oeq_global.OeQ_plugin_path()
            project_path = oeq_global.OeQ_project_path()
            project_name = oeq_global.OeQ_project_name()

            default_progress = os.path.join(plugin_path, 'project', 'default_progress')
            project_file = os.path.join(project_path, project_name + '.oeq')
            if os.path.exists(project_file):
                os.remove(project_file)
            # write section views
            end = len(self.section_views) + 1
            for i in range(1, end):
                model = self.section_views[i-1].model()
                json_file = os.path.join(default_progress, 'section{}.json'.format(i))
                with open(json_file, "r") as jsonFile:
                    json_data = json.load(jsonFile)

                for j, step in enumerate(json_data['steplist']):
                        step['state'] = model.item(j).checkState()

                with ZipFile(project_file, 'a') as oeq_zip:
                    oeq_zip.writestr('section{}.json'.format(i), json.dumps(json_data))

            # write project info
            with ZipFile(project_file, 'a') as oeq_zip:
                oeq_zip.writestr('project_info.json', json.dumps(oeq_global.OeQ_project_info))

        except (TypeError, AttributeError) as AccessOeqGlobalError:
            print(self.__module__, AccessOeqGlobalError)

        extensions.save()
        print 'Save Project'
        print [i.layer_name for i in oeq_global.OeQ_ExtensionRegistry]


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
