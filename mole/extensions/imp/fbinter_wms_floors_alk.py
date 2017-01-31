# -*- coding: utf-8 -*-

from mole.project import config
from PyQt4.QtCore import QVariant

def load(self=None):
    self.load_wms()
    return True

def preflight(self=None):
    from mole.project.config import sample_layer_name
    #self.createSampleLayer()

def evaluation(self=None, parameters={},feature=None):
    # import functions
    from mole import oeq_global
    from qgis.core import NULL
    #prepare rgba_keys
    rgba_keys = ['R', 'G', 'B', 'a']
    if bool(self.field_id):
        rgba_keys = [self.field_id + '_' + c for c in rgba_keys]
    if feature != None:
        #sample color
        rgba = self.sampleColor(feature, blur = 3)
        # decode_color
        result = self.decode_color(rgba['R'], rgba['G'], rgba['B'], rgba['a'], [self.field_id], mode='average')
        #print result
        if all([c['value'] != NULL for c in result.values()]):
            return result
    return {self.field_id: {'type': QVariant.Int,
                         'value': 3.3}}



import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WMS',
    extension_name='Floors (ALK, WMS)',
    extension_type='information',
    field_id='FLOORS',   #used for point sampling tool
    par_in=[],
    source_type='wms',
    layer_name='Floors (WMS Capture)',
    sourcelayer_name=config.building_coordinate_layer_name,
    targetlayer_name=config.data_layer_name,
    active=False,
    description=u'',
    source='crs=EPSG:4326&dpiMode=7&format=image/png&layers=2&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/alk_gebaeude',
    source_crs='EPSG:4326',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    load_method=load,
    preflight_method=None,
    evaluation_method=evaluation,
    postflight_method=None)

extension.registerExtension(default=True)
