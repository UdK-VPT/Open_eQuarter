# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole3 import oeq_global
from mole3.project import config
from mole3.extensions import OeQExtension
from mole3.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from qgis.PyQt.QtCore import QVariant

    wl_sqteh = NULL
    if not oeq_global.isnull([parameters['WL_UEH'],parameters['HHRS']]):
        wl_sqteh= float(parameters['WL_UEH'])*float(parameters['HHRS'])/1000
    return {'WL_SQTEH': {'type': QVariant.Double, 'value': wl_sqteh}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Heritage Spec. Transm. Heat Loss',
    extension_name='Wall SpecTransm (SQT, EnEV Heritage)',
    layer_name= 'SQT Wall EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_SQTEH',
    source_type='none',
    par_in=['WL_UEH','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_SQTEH'],
    description="Calculate the EnEV Heritage Transmission Heat Loss of the Building's Walls per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
