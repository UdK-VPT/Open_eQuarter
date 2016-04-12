# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config
from PyQt4.QtCore import QVariant

def calculation(self=None, parameters={}):
    from mole import oeq_global
    result = {'FLOORS': {'type': QVariant.Int,
                         'value': 3.5}}
    if not oeq_global.isnull(parameters['FLRS_ALK']):
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
    field_id='',   #used for point sampling tool
    par_in=['FLRS_ALK', 'BSMTS_ALK'],
    field_rename= {"AnzahlDerO" : "FLRS_ALK", "AnzahlDerU" : "BSMTS_ALK"},
    par_out=['FLOORS','BASMTS'],
    source_type='wfs',
    layer_name='Floors (WFS Capture)',
    layer_in=config.pst_output_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    description=u'',
    source='http://fbinter.stadt-berlin.de/fb/wfs/geometry/senstadt/re_alkis_gebaeude?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=fis:re_alkis_gebaeude&SRSNAME=EPSG:25833',
    source_crs='EPSG:25833',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    evaluation_method=calculation)

extension.registerExtension(default=True)

