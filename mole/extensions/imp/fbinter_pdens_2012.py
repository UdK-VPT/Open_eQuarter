# -*- coding: utf-8 -*-


import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='import',
    extension_name='Population Density (2012, WMS)',
    field_id='PDENS',
    source_type='wms',
    layer_name='Population Density',
    active=True,
    description=u'',
    colortable=os.path.join(__file__[:-3] + '.qml'),
    source='crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k06_06ewdichte2012')

extension.registerExtension(default=True)
