# -*- coding: utf-8 -*-

import os
import time

from PyQt4.QtGui import QProgressBar
from PyQt4.QtCore import Qt
from qgis.utils import iface
from qgis.core import QgsProject, NULL

from project import config

OeQ_ExtensionRegistry = []
OeQ_ExtensionDefaultRegistry = []

OeQ_ExtensionsLoaded = False

# global OeQ_project_info
OeQ_project_info = {
    'project_name': u'MyProject',
    'description': u'The aim of this project, is to analyse a quarter.',
    'location_city': u'City or street',
    'location_postal': u'Postal',
    'location_lon': u'Lon',
    'location_lat': u'Lat',
    'location_crs': u'CRS',
    'heating_degree_days': 390.06,
    'average_build_year': 1950,
    'population_density': 14000
}

# global OeQ_project_name
def OeQ_project_name():
    path_to_project = QgsProject.instance().fileName()
    filename = os.path.basename(path_to_project)
    project_name = filename.split('.')[0]
    return project_name


#global OeQ_project_path
def OeQ_project_path():
    qgis_path = QgsProject.instance().readPath('')
    normed_path = os.path.normpath(qgis_path)
    return normed_path


#global OeQ_plugin_path
def OeQ_plugin_path():
    no_timeout = 50
    file_location = os.path.realpath(__file__)
    while not os.path.exists(file_location) and no_timeout:
        time.sleep(0.1)
        file_location = os.path.realpath(__file__)
        no_timeout -= 1

    plugin_dir = os.path.dirname(file_location)
    return plugin_dir


# global OeQ_style_path
def OeQ_style_path():
    return os.path.join(OeQ_plugin_path() + 'styles')


# the project path equals './' as long as the project has not been saved
#global OeQ_project_saved
def OeQ_project_saved():
    # return OeQ_project_path() != './'
    return OeQ_project_name() != ''


def OeQ_init_progressbar(title='Be patient!', message='Background calculations are going on...', timeout=0,
                         maxcount=100):
    widget = iface.messageBar().createMessage(title, message)

    # set a new message bar
    progressbarwidget = QProgressBar()
    progressbarwidget.setAlignment(Qt.AlignLeft)
    progressbarwidget.setMaximum(maxcount)
    progressbarwidget.setValue(0)
    widget.layout().addWidget(progressbarwidget)

    # pass the progress bar to the message Bar
    iface.messageBar().pushWidget(widget, iface.messageBar().INFO)
    print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"
    return progressbarwidget


def OeQ_push_progressbar(progressbarwidget, progress_counter):
    progress_counter = progress_counter + 1
    progressbarwidget.setValue(progress_counter)
    print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"
    return progress_counter


def OeQ_kill_progressbar():
    iface.messageBar().clearWidgets()


def OeQ_init_info(title='Be patient!', message='Background calculations are going on...'):
    widget = iface.messageBar().createMessage(title, message)
    iface.messageBar().pushWidget(widget, iface.messageBar().INFO)
    print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"


def OeQ_kill_info():
    iface.messageBar().clearWidgets()


def OeQ_init_warning(title='Be patient!', message='Background calculations are going on...'):
    widget = iface.messageBar().createMessage(title, message)
    iface.messageBar().pushWidget(widget, iface.messageBar().WARNING)
    print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"


def OeQ_kill_warning():
    iface.messageBar().clearWidgets()


def OeQ_init_error(title='Be patient!', message='Background calculations are going on...'):
    widget = iface.messageBar().createMessage(title, message)
    iface.messageBar().pushWidget(widget, iface.messageBar().CRITICAL)
    print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"


def OeQ_kill_error():
    iface.messageBar().clearWidgets()


def isnull(value):
    return type(value) is type(NULL)
