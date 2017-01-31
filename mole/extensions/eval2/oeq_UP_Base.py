# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import present_base_uvalue_AVG_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    bs_up = NULL
    if not oeq_global.isnull(parameters['YOC']):
        bs_up = present_base_uvalue_AVG_by_building_age_lookup.get(parameters['YOC'])
    return {'BS_UP': {'type': QVariant.Double, 'value': bs_up}}



extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values Present',
    extension_name='Base Quality (U_Value, Present)',
    layer_name= 'U Base Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='BS_UP',
    source_type='none',
    par_in=['YOC'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['BS_UP'],
    description=u"Calculate the present U-Value of the Building's baseplate",
    evaluation_method=calculation)

extension.registerExtension(default=True)
