# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole3 import oeq_global
from mole3.project import config
from mole3.extensions import OeQExtension
from mole3.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    return {}


extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='General',
    extension_name='Year of Construction',
    layer_name= 'Year of Construction',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id= None,
    source_type='none',
    par_in= [],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['YOC'],
    description="Year of Construction",
    evaluation_method=calculation)

extension.registerExtension(default=True)
