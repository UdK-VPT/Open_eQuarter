# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole3 import oeq_global
from mole3.project import config
from mole3.extensions import OeQExtension
from mole3.stat_corr import rb_contemporary_window_uvalue_by_building_age_lookup
from mole3.stat_corr import nrb_contemporary_window_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from qgis.PyQt.QtCore import QVariant
    return {'WN_UE': {'type': QVariant.Double, 'value': 1.3}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values EnEV',
    extension_name='Window Quality (U_Value, EnEV)',
    layer_name= 'U Window EnEV',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_UE',
    source_type='none',
    par_in=[],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_UE'],
    description="Calculate the EnEV U-Value of the Building's windows",
    evaluation_method=calculation)

extension.registerExtension(default=True)
