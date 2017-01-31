# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_roof_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    rf_uc = NULL
    if not oeq_global.isnull(parameters['YOC']):
        rf_uc=contemporary_roof_uvalue_by_building_age_lookup.get(parameters['YOC'])
    return {'RF_UC': {'type': QVariant.Double, 'value': rf_uc}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values Contemporary',
    extension_name='Roof Quality (U_Value, Contemporary)',
    layer_name= 'U Roof Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_UC',
    source_type='none',
    par_in=['YOC'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_UC'],
    description=u"Calculate the contemporary U-Value of the Building's roof",
    evaluation_method=calculation)

extension.registerExtension(default=True)
