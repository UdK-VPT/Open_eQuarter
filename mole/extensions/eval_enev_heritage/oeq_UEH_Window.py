# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_window_uvalue_by_building_age_lookup
from mole.stat_corr import nrb_contemporary_window_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
from math import floor, ceil
    from PyQt4.QtCore import QVariant
    wn_ueh = NULL

# differentiation between RB and NRB (for now in case of contemporary U-Values RB=NRB. After getting NRB data for contemporary case code must be adaptet)
    if parameters['BLD_USAGE'] == "RB":
        if not oeq_global.isnull(parameters['YOC']):
            wn_ueh = 1.3

    elif parameters['BLD_USAGE'] == "NRB":
        if not oeq_global.isnull(parameters['YOC']):
            wn_ueh = 1.3
            # u-value in enev for rb and nrb is the same for window

    else:
        if not oeq_global.isnull(parameters['YOC']):
            wn_ueh = 1.3

    return {'WN_UEH': {'type': QVariant.Double, 'value': wn_ueh}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values EnEV Heritage',
    extension_name='Window Quality (U_Value, EnEV Heritage)',
    layer_name= 'U Window EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_UEH',
    source_type='none',
    par_in=['YOC','BLD_USAGE','HERIT_STAT'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_UEH'],
    description=u"Calculate the EnEV Heritage U-Value of the Building's windows",
    evaluation_method=calculation)

extension.registerExtension(default=True)
