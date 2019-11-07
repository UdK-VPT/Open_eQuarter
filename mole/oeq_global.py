
# -*- coding: utf-8 -*-

import os
import time,datetime

from PyQt4.QtGui import QProgressBar
from PyQt4.QtCore import Qt
from qgis.utils import iface
from qgis.core import QgsProject, NULL

from project import config

OeQ_ExtensionRegistry = []
OeQ_ExtensionDefaultRegistry = []

OeQ_ExtensionsLoaded = False

first_of_all_calculation_times =datetime.datetime(1900, 1, 1, 0, 0)

OeQ_BuildingIndex = 0

def OeQ_get_bld_id():
    global OeQ_BuildingIndex
    OeQ_BuildingIndex += 1
    return OeQ_BuildingIndex

# global OeQ_project_info
OeQ_project_info = {
    'project_name': u'New Project',
    'description': u'The aim of this project, is to analyse a quarter.',
    'location_city': u'City or street',
    'location_city_short': u'City',
    'location_street': u'Street',
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
    return os.path.join(OeQ_plugin_path() , 'styles')


# the project path equals './' as long as the project has not been saved
#global OeQ_project_saved
def OeQ_project_saved():
    return (len(OeQ_project_path()) > 3)
    #return OeQ_project_name() != ''



def fix_german_umlauts(thetext):
    #thetext = str(thetext)
    codetype = type(thetext)
    if codetype != unicode:
        thetext = unicode(thetext, "utf-8")

    #print type(thetext)

    trans = {u'ä':u'ae',u'Ä':u'Ae',u'ö':u'oe',u'Ö':u'Oe',u'ü':u'ue', u'Ü':u'Ue',u'ß':u'ss'}
    for i in trans.keys():
        k = thetext.split(i)
        #print k
        l = trans[i]
        #print l
        thetext = l.join(k)
    if codetype != unicode:
        return str(thetext)
    else:
        return thetext

def OeQ_push_progressbar(title='Be patient!', message='Background calculations are going on...', timeout=0,
                         maxcount=100):
    widget = iface.messageBar().createMessage(title, message)

    # set a new message bar
    progressbarwidget = QProgressBar()
    progressbarwidget.setAlignment(Qt.AlignLeft)
    progressbarwidget.setMaximum(maxcount)
    progressbarwidget.setValue(0)
    widget.layout().addWidget(progressbarwidget)

    # pass the progress bar to the message Bar
    baritem=iface.messageBar().pushWidget(widget, iface.messageBar().INFO)
    OeQ_unlockQgis()
    #print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"
    return {'widget':progressbarwidget,'baritem':baritem}


def OeQ_update_progressbar(progressbar, progress_counter,message = None):
    progress_counter = progress_counter + 1
    OeQ_unlockQgis()
    progressbar['widget'].setValue(progress_counter)
    OeQ_unlockQgis()
    #print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"

    return progress_counter


def OeQ_pop_progressbar(progressbar=None):
    if not progressbar:
        iface.messageBar().clearWidgets()
    else:
        iface.messageBar().popWidget(progressbar['baritem'])


def OeQ_push_info(title='Be patient!', message='Background calculations are going on...'):
    widget = iface.messageBar().createMessage(title, message)
    iface.messageBar().pushWidget(widget, iface.messageBar().INFO)
    OeQ_unlockQgis()
    return widget
    #print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"



def OeQ_pop_info(baritem=None):
    if not baritem:
        iface.messageBar().clearWidgets()
    else:
        iface.messageBar().popWidget(baritem)


OeQ_StatusWidget = None

def OeQ_push_status(title='Status: ', message='Complete'):
    global OeQ_StatusWidget
    OeQ_StatusWidget = iface.messageBar().createMessage(title, message)
    iface.messageBar().pushWidget(OeQ_StatusWidget, iface.messageBar().INFO)
    OeQ_unlockQgis()
    return OeQ_StatusWidget
    #print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"


def OeQ_pop_status():
    global OeQ_StatusWidget
    if bool(OeQ_StatusWidget):
        try:
            iface.messageBar().popWidget(OeQ_StatusWidget)
        except:
            pass





def OeQ_push_warning(title='Be patient!', message='Background calculations are going on...'):
    widget = iface.messageBar().createMessage(title, message)
    iface.messageBar().pushWidget(widget, iface.messageBar().WARNING)
    OeQ_unlockQgis()
    return widget
    #print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"


def OeQ_pop_warning(baritem=None):
    if not baritem:
        iface.messageBar().clearWidgets()
    else:
        iface.messageBar().popWidget(baritem)


def OeQ_push_error(title='Be patient!', message='Background calculations are going on...'):
    widget = iface.messageBar().createMessage(title, message)
    iface.messageBar().pushWidget(widget, iface.messageBar().CRITICAL)
    OeQ_unlockQgis()
    return widget
    #print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"


def OeQ_pop_error(baritem=None):
    if not baritem:
        iface.messageBar().clearWidgets()
    else:
        iface.messageBar().popWidget(baritem)



def isnull(value):
    if type(value) != type([]):
        value = [value]
    for i in value:
        if type(i) is type(NULL):
            return True
    return False

def isEmpty(string):
    return ((string == '') | (string == u''))

def isStringOrUnicode(string):
 return (type(string) == type('')) | (type(string) == type(u''))

QeQ_current_work_layer = None

def OeQ_unlockQgis():
    import sys
    sys.stdout.write('')
    sys.stdout.write('')
    sys.stdout.write('')
    sys.stdout.write('')


from PyQt4.QtCore import QSettings

QeQ_disableDialogAfterAddingFeatureState = False

def QeQ_disableDialogAfterAddingFeature():
    # get user defined current setting
    global QeQ_disableDialogAfterFeatureState
    QeQ_disableDialogAfterFeatureState = QSettings().value( '/qgis/digitizing/disable_enter_attribute_values_dialog')
    # override setting
    QSettings().setValue( '/qgis/digitizing/disable_enter_attribute_values_dialog', True )


def QeQ_enableDialogAfterAddingFeature():
    # restore setting
    global QeQ_disableDialogAfterFeatureState
    QSettings().setValue( '/qgis/digitizing/disable_enter_attribute_values_dialog', QeQ_disableDialogAfterAddingFeatureState )

OeQ_Solo_Layers_Temp =[]




from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


def OeQ_wait_for_renderer(timeout=10000):
    """Block loop until signal emitted, or timeout (ms) elapses."""
    from PyQt4.QtCore import QEventLoop,QTimer
    #print 'wait for renderer...',
    # function call if action timed out
    def timed_out(render_result_flag):
        render_result_flag[0]=False
        loop.quit()
    #define loop
    loop = QEventLoop()
    #define Timer
    timer=QTimer()
    #define render_result
    render_result = [True]

    OeQ_wait(2)

    #check wether Canvas is drawing
    if iface.mapCanvas().isDrawing():
        #connect mapCanvasRefreshed and renderComplete events to quit loop
        iface.mapCanvas().renderComplete.connect(loop.quit)
        #iface.mapCanvas().mapCanvasRefreshed.connect(loop.quit)
        # if a timeout is defined and other than 0
        if bool(timeout):
            # start timer
            timer.singleShot(timeout,lambda: timed_out(render_result))
        #and jump into the loop
        loop.exec_()
        #disconnect after loop has quit
        #iface.mapCanvas().mapCanvasRefreshed.disconnect(loop.quit)
        iface.mapCanvas().renderComplete.disconnect(loop.quit)
    #print 'Done'
    return render_result[0]

def OeQ_wait_until_layer_exists():
    pass

def OeQ_wait_for_file(filepath,timeout=10000):
    """Block loop until signal emitted, or timeout (ms) elapses."""
    from PyQt4.QtCore import QEventLoop,QTimer
    from os.path import isfile
    import platform
    import os
    if platform.system() == 'Darwin':
        return True
    if isfile(filepath):
        return True
    loop = QEventLoop()
    timer=QTimer()
    file_result = [True]
    #
    def check_file(testpath):

        if isfile(testpath):
            timer.stop()
            loop.quit()
    #
    timer.timeout.connect(lambda: check_file(filepath))
    timer.setSingleShot(False)
    timer.start(500)
    #
    def timed_out(file_result_flag):
        file_result_flag[0]=False
        loop.quit()
    #
    if timeout >500:
        timer.singleShot(timeout,lambda: timed_out(file_result))
    loop.exec_()
    return file_result[0]



def OeQ_wait(sec):
    from PyQt4.QtCore import QEventLoop,QTimer
    #print 'wait ' + str(sec) + ' sec',
    loop = QEventLoop()
    QTimer.singleShot(sec*1000,loop.quit)
    loop.exec_()
    #print "Done"

def test(testo):
    from qgis.core import QgsRasterLayer,QgsMapLayerRegistry
    from mole import oeq_global
    urlWithParams = 'url=http://kaart.maaamet.ee/wms/alus&format=image/png&layers=MA-ALUS&styles=&crs=EPSG:3301'
    rlayer = QgsRasterLayer(urlWithParams, 'MA-ALUS', 'wms')
    QgsMapLayerRegistry.instance().addMapLayer(rlayer)
    #print oeq_global.OeQ_wait_for_renderer(testo)



