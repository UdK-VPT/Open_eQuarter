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
    wn_uc = NULL

#differentiation between RB and NRB (for now in case of contemporary U-Values RB=NRB. After getting NRB data for contemporary case code must be adaptet)
    if parameters['BLD_USAGE'] == "RB":
        if not oeq_global.isnull(parameters['YOC']):
            wn_uc = rb_contemporary_window_uvalue_by_building_age_lookup.get(parameters['YOC'])

    elif parameters['BLD_USAGE'] == "NRB":
        if not oeq_global.isnull(parameters['YOC']):
            wn_uc= nrb_contemporary_window_uvalue_by_building_age_lookup.get(parameters['YOC'])

    else:
        if not oeq_global.isnull(parameters['YOC']):
            wn_uc=(((rb_contemporary_window_uvalue_by_building_age_lookup.get(parameters['YOC'])) + (nrb_contemporary_window_uvalue_by_building_age_lookup.get(parameters['YOC']))) / 2)

    return {'WN_UC': {'type': QVariant.Double, 'value': wn_uc}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values Contemporary',
    extension_name='Window Quality (U_Value, Contemporary)',
    layer_name= 'U Window Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_UC',
    source_type='none',
    par_in=['YOC','BLD_USAGE'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_UC'],
    description="Calculate the contemporary U-Value of the Building's windows",
    evaluation_method=calculation)

extension.registerExtension(default=True)
