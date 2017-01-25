# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    dataset = {'HTC': NULL}
    dataset.update(parameters)

    if not oeq_global.isnull([dataset['BS_UC'] , dataset['BS_AR'] , dataset['RF_UC'] , dataset['RF_AR'] , dataset['WL_UC'] , dataset['WL_AR'] , dataset['WN_UC'] , dataset['WN_AR']]):
        qtp_total = float(dataset['BS_UC'] * dataset['BS_AR'] *0.35 ) + float(dataset['RF_UC'] * dataset['RF_AR']) + float(dataset['WL_UC'] * dataset['WL_AR'] ) + float(dataset['WN_UC'] * dataset['WN_AR'])
        env_area =  float(dataset['BS_AR']) + float(dataset['RF_AR']) + float(dataset['WL_AR']) + float(dataset['WN_AR'])
        dataset['HTC']=qtp_total/env_area
    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Envelope Quality (SHT, Contemporary)',
    layer_name= 'SHT Envelope Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HTC',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','BS_UC','RF_UC','WL_UC','WN_UC'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HTC'],
    description=u"Calculate the contemporary Transmission Heat Coefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
