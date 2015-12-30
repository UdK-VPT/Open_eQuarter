# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config

def calculation(self=None, parameters={}):
    from mole import oeq_global
    result = self.decode_color(parameters['YOC_R'],
                             parameters['YOC_G'],
                             parameters['YOC_B'],
                             parameters['YOC_a'],
                             ['YOC'],
                             mode='average')
    #print result['YOC']['value']
    if oeq_global.isnull(result['YOC']['value']):
        result['YOC']['value'] = oeq_global.OeQ_project_info['average_build_year']
    return result

import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WMS',
    source_type='wms',
    field_id='YOC',   #used for point sampling tool
    extension_name='Year of Construction (92/93, WMS)',
    layer_name='Year of Construction (WMS Capture)',
    description=u'Gebäudealter 199293 Scan der Karte Gebäudealter 1992 93 '
                + u'aus der Veroeffentlichung: Staedtebauliche Entwicklung Berlins seit 1650 in Karten',
    source='crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/gebaeudealter',
    source_crs='EPSG:3068',
    par_in=['YOC_R','YOC_G','YOC_B','YOC_a'],
    layer_in=config.pst_output_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    evaluation_method=calculation)

extension.registerExtension(default=True)
