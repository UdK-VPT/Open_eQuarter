# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_wall_uvalue_by_building_age_lookup
from mole.stat_corr import nrb_contemporary_wall_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    return {'WL_UE': {'type': QVariant.Double, 'value': 0.24}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values EnEV',
    extension_name='Wall Quality (U_Value, EnEV)',
    layer_name= 'U Wall EnEV',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_UE',
    source_type='none',
    par_in=[],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_UE'],
    description=u"Calculate the EnEV U-Value of the Building's walls",
    evaluation_method=calculation)

extension.registerExtension(default=True)
