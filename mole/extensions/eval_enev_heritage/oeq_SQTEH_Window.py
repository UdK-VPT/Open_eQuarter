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
    from PyQt4.QtCore import QVariant

    wn_sqteh = NULL
    if not oeq_global.isnull([parameters['WN_UEH'],parameters['HHRS']]):
        wn_sqteh= float(parameters['WN_UEH'])*float(parameters['HHRS'])/1000
    return {'WN_SQTEH': {'type': QVariant.Double, 'value': wn_sqteh}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Heritage Spec. Transm. Heat Loss',
    extension_name='Window SpecTransm (SQT, EnEV Heritage)',
    layer_name= 'SQT Window EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_SQTEH',
    source_type='none',
    par_in=['WN_UEH','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_SQTEH'],
    description=u"Calculate the EnEV Heritage Transmission Heat Loss of the Building's Windows per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
