# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_roof_uvalue_by_building_age_lookup
from mole.stat_corr import nrb_contemporary_roof_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    rf_ueh = NULL

# differentiation between RB and NRB (for now in case of contemporary U-Values RB=NRB. After getting NRB data for contemporary case code must be adaptet)
    if parameters['BLD_USAGE'] == "RB":
        if not oeq_global.isnull(parameters['YOC']):
            rf_ueh = 0.24

    elif parameters['BLD_USAGE'] == "NRB":
        if not oeq_global.isnull(parameters['YOC']):
            rf_ueh = 0.24
            # u-value in enev for rb and nrb is the same for roof

    else:
        if not oeq_global.isnull(parameters['YOC']):
            rf_ueh = 0.24

    return {'RF_UEH': {'type': QVariant.Double, 'value': rf_ueh}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values EnEV Heritage',
    extension_name='Roof Quality (U_Value, EnEV Heritage)',
    layer_name= 'U Roof EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_UEH',
    source_type='none',
    par_in=['YOC','BLD_USAGE','HERIT_STAT'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_UEH'],
    description=u"Calculate the EnEV Heritage U-Value of the Building's roof",
    evaluation_method=calculation)

extension.registerExtension(default=True)
