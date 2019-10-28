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

    wn_qtc = NULL
    if not oeq_global.isnull([parameters['WN_AR'],parameters['WN_UC'],parameters['HHRS']]):
        wn_qtc=float(parameters['WN_AR']) * float(parameters['WN_UC'])*float(parameters['HHRS'])/1000
    return {'WN_QTC': {'type': QVariant.Double, 'value': wn_qtc}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Contemp. Transm. Heat Loss',
    extension_name='Window Quality (QT, Contemporary)',
    layer_name= 'QT Window Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_QTC',
    source_type='none',
    par_in=['WN_AR','WN_UC','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_QTC'],
    description=u"Calculate the contemporary Transmission Heat Loss of the Building's Windows",
    evaluation_method=calculation)

extension.registerExtension(default=True)
