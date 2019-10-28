# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from math import floor, ceil
    from PyQt4.QtCore import QVariant

    bs_sqte= NULL
    if not oeq_global.isnull([parameters['BS_UE'],parameters['HHRS']]):
        bs_sqte= float(parameters['BS_UE'])*float(parameters['HHRS'])/1000 *0.35 #correction factor
    return {'BS_SQTE': {'type': QVariant.Double, 'value': bs_sqte}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Spec. Transm. Heat Loss',
    extension_name='Base SpecTransm (SQT, EnEV)',
    layer_name= 'SQT Base EnEV',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='BS_SQTE',
    source_type='none',
    par_in=['BS_UE','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['BS_SQTE'],
    description=u"Calculate the EnEV Transmission Heat Loss of the Building's baseplate per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
