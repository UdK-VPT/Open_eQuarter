# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config

def calculation(self=None, parameters={}):
        return self.decode_color(parameters['PDENS_R'],
                                 parameters['PDENS_G'],
                                 parameters['PDENS_B'],
                                 parameters['PDENS_a'],
                                 ['PDENS'],
                                 'average')


import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WMS',
    extension_name='Population Density (2012, WMS)',
    field_id='PDENS',  #used for point sampling tool
    source_type='wms',
    layer_name='Population Density (WMS Capture)',
    par_in=['PDENS_R','PDENS_G','PDENS_B','PDENS_a'],
    layer_in=config.pst_output_layer_name,
    layer_out=config.data_layer_name,
    source='crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k06_06ewdichte2012',
    active=True,
    description=u'',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    evaluation_method=calculation)

extension.registerExtension(default=True)
