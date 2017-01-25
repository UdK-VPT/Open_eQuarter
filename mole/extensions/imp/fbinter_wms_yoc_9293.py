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
        color = self.decode_color(rgba['R'], rgba['G'], rgba['B'], rgba['a'], [self.field_id], mode='average')
        #print color
        if all([c['value'] != NULL for c in color.values()]):
            return color
    return {self.field_id: {'type': QVariant.Int,
                         'value': oeq_global.OeQ_project_info['average_build_year']}}


import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WMS',
    source_type='wms',
    field_id='YOC',   #used for point sampling tool
    extension_name='Year of Construction (92/93, WMS)',
    extension_type='information',
    layer_name='Year of Construction (WMS Capture)',
    description=u'Gebäudealter 199293 Scan der Karte Gebäudealter 1992 93 '
                + u'aus der Veroeffentlichung: Staedtebauliche Entwicklung Berlins seit 1650 in Karten',
    source='crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/gebaeudealter',
    source_crs='EPSG:3068',
    par_in= [],
    sourcelayer_name=config.building_coordinate_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    load_method=load,
    preflight_method=preflight,
    evaluation_method=evaluation,
    postflight_method=None)

extension.registerExtension(default=True)

