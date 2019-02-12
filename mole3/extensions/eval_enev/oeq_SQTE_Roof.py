# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from qgis.PyQt.QtCore import QVariant

    rf_sqte = NULL
    if not oeq_global.isnull([parameters['RF_UE'],parameters['HHRS']]):
        rf_sqte= float(parameters['RF_UE'])*float(parameters['HHRS'])/1000 *0.35 #correction factor
    return {'RF_SQTE': {'type': QVariant.Double, 'value': rf_sqte}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Spec. Transm. Heat Loss',
    extension_name='Roof SpecTransm (SQT, EnEV)',
    layer_name= 'SQT Roof EnEV',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_SQTE',
    source_type='none',
    par_in=['RF_UE','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_SQTE'],
    description="Calculate the EnEV Transmission Heat Loss of the Building's Roof per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
