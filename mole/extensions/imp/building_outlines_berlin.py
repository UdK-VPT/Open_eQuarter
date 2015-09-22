# -*- coding: utf-8 -*-

import os
from mole.extensions import OeQExtension
from mole.project import config


def calculation(self=None, parameters={}):
    return {}


extension = OeQExtension(
    extension_id=__name__,
    category='import',
    field_id='OUTL',
    par_in=[],
    source_type='shp',
    extension_name='Building Outlines ("Hausumringe")',
    layer_name=config.housing_layer_name,
    layer_in=config.housing_layer_name,
    description=u'',
    active=True,
    evaluation_method=calculation,
    source=os.path.join(os.path.expanduser('~'), 'Hausumringe EPSG3857', 'Hausumringe EPSG3857.shp'),
    extension_filepath=__file__,
    colortable = os.path.join(__file__[:-3] + '.qml'))

extension.registerExtension(default=True)
