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

    bs_qtp = NULL
    if not oeq_global.isnull([parameters['BS_AR'],parameters['BS_UP'],parameters['HHRS']]):
        bs_qtp=float(parameters['BS_AR']) * float(parameters['BS_UP'])*float(parameters['HHRS'])/1000 *0.35 #correction factor
    return {'BS_QTP': {'type': QVariant.Double, 'value': bs_qtp}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Present Transm. Heat Loss',
    extension_name='Base Quality (QT, Present)',
    layer_name= 'QT Base Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='BS_QTP',
    source_type='none',
    par_in=['BS_AR','BS_UP','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['BS_QTP'],
    description=u"Calculate the present Transmission Heat Loss of the Building's baseplate",
    evaluation_method=calculation)

extension.registerExtension(default=True)
