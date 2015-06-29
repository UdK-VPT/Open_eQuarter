import os
from PyQt4.QtGui import QProgressBar
from PyQt4.QtCore import Qt
from qgis.utils import iface
from qgis.core import QgsProject,NULL

global OeQ_project_info
OeQ_project_info = {
    'name': '',
    'description': '',
    'location': '',
    'location_postal': 0,
    'heating_dd': 0.0, 
    'avg_yoc': 0,
    'pop_dens': 0.0
}
global autorun_enabled

global OeQ_project_name
def OeQ_project_name(): return os.path.basename(QgsProject.instance().fileName()).split(".")[0]

global OeQ_project_path
def OeQ_project_path(): return os.path.normpath(QgsProject.instance().readPath(''))

global OeQ_plugin_path
def OeQ_plugin_path(): return os.path.dirname(os.path.realpath(__file__))
# the project path equals './' as long as the project has not been saved
global OeQ_project_saved 
def OeQ_project_saved(): return OeQ_project_path() != './' 

def OeQ_init_progressbar(title='Be patient!',message='Background calculations are going on...',timeout=0,maxcount=100):
  widget = iface.messageBar().createMessage(title,message)      

  #set a new message bar
  progressbarwidget = QProgressBar()
  progressbarwidget.setAlignment(Qt.AlignLeft)
  progressbarwidget.setMaximum(maxcount)           
  progressbarwidget.setValue(0)
  widget.layout().addWidget(progressbarwidget)

  #pass the progress bar to the message Bar
  iface.messageBar().pushWidget(widget, iface.messageBar().INFO)
  print "THIS PRINTLN IS NECESSARY TO TRIGGER THE MESSAGEBAR"
  return progressbarwidget

def OeQ_push_progressbar(progressbarwidget,progress_counter):
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
