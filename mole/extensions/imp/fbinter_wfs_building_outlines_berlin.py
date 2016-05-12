# -*- coding: utf-8 -*-

import os
from mole.extensions import OeQExtension
from mole.project import config


def calculation(self=None, parameters={}):

    return {}

extension = OeQExtension(
    extension_id=__name__,
    category='Basic',
    subcategory='File',
    field_id='OUTL',
    par_in=[],
    par_out=['PERIMETER'],
    source_type='shp',
    extension_name='Building Outlines ("Hausumringe")',
    layer_name=config.housing_layer_name,
    layer_in=config.housing_layer_name,
    description=u'',
    active=False,
    evaluation_method=calculation,
    source=os.path.join(os.path.expanduser('~'), 'Hausumringe EPSG3857', 'Hausumringe EPSG3857.shp'),
    source_crs='EPSG:3857',
    extension_filepath=__file__,
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'))
#from . import *

extension.registerExtension(default=True)
