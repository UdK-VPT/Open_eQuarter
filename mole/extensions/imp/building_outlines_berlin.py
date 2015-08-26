# -*- coding: utf-8 -*-

import os
from mole.extensions import OeQExtension
from mole.project.config import housing_layer_name

extension = OeQExtension(
    extension_id=__name__,
    category='import',
    field_id='OUTL',
    source_type='shp',
    extension_name='Building Outlines ("Hausumringe")',
    layer_name=housing_layer_name,
    description=u'',
    active=True,
    colortable=os.path.join(__file__[:-3] + '.qml'),
    source=os.path.join(os.path.expanduser('~'), 'Hausumringe EPSG3857', 'Hausumringe EPSG3857.shp'))

extension.registerExtension(default=True)
