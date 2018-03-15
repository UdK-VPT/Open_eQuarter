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
    wl_uc = NULL

#differentiation between RB and NRB (for now in case of contemporary U-Values RB=NRB. After getting NRB data for contemporary case code must be adaptet)
    if parameters['BLD_USAGE'] == "RB":
        if not oeq_global.isnull(parameters['YOC']):
            wl_uc = rb_contemporary_wall_uvalue_by_building_age_lookup.get(parameters['YOC'])

    elif parameters['BLD_USAGE'] == "NRB":
        if not oeq_global.isnull(parameters['YOC']):
            wl_uc = nrb_contemporary_wall_uvalue_by_building_age_lookup.get(parameters['YOC'])

    else:
        if not oeq_global.isnull(parameters['YOC']):
            wl_uc=(((rb_contemporary_wall_uvalue_by_building_age_lookup.get(parameters['YOC'])) + (nrb_contemporary_wall_uvalue_by_building_age_lookup.get(parameters['YOC']))) / 2)

    return {'WL_UC': {'type': QVariant.Double, 'value': wl_uc}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values Contemporary',
    extension_name='Wall Quality (U_Value, Contemporary)',
    layer_name= 'U Wall (Contemporary)',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_UC',
    source_type='none',
    par_in=['YOC','BLD_USAGE'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_UC'],
    description=u"Calculate the contemporary U-Value of the Building's walls",
    evaluation_method=calculation)

extension.registerExtension(default=True)
