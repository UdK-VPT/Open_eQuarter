# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config
from PyQt4.QtCore import QVariant

def load(self=None):
    self.load_wfs()
    return True

def evaluation(self=None, parameters={},feature=None):
    from mole import oeq_global
    result = {'FLOORS': {'type': QVariant.Double,
                         'value': 3.5}}
    if bool(parameters['FLRS_ALK']):
        result['FLOORS']['value'] = parameters['FLRS_ALK']
    return result


import os
from mole.extensions import OeQExtension
from mole.project import config
extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WFS',
    extension_name='Floors (ALKIS, WFS)',
    extension_type='information',
    field_id='',   #used for point sampling tool
    par_in=['FLRS_ALK', 'BSMTS_ALK'], #config.building_id_key,
    #field_rename= {"AnzahlDerO" : "FLRS_ALK", "AnzahlDerU" : "BSMTS_ALK"},
    source_type='wfs',
    layer_name='Floors (WFS Capture)',
    sourcelayer_name='Floors (WFS Capture)',
    targetlayer_name=config.data_layer_name,
    active=False,
    description=u'',
    source='http://fbinter.stadt-berlin.de/fb/wfs/geometry/senstadt/re_alkis_gebaeude?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=fis:re_alkis_gebaeude&SRSNAME=EPSG:25833',
    source_crs='EPSG:25833',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    load_method=load,
    preflight_method=None,
    evaluation_method=evaluation,
    postflight_method=None)

extension.registerExtension(default=True)

