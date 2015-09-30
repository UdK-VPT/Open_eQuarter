# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={}):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    dataset = {'HTP': NULL}
    dataset.update(parameters)
    qtp_total = float(dataset['BS_QTP']) + float(dataset['RF_QTP']) + float(dataset['WL_QTP']) + float(dataset['WN_QTP'])*1.2
    env_area =  float(dataset['BS_AR']) + float(dataset['RF_AR']) + float(dataset['WL_AR']) + float(dataset['WN_AR'])
    dataset['HTP']=qtp_total/env_area
    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Envelope Quality (HT, Present)',
    layer_name= 'HT Envelope Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='HTP',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','BS_QTP','RF_QTP','WL_QTP','WN_QTP'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['HTP'],
    description=u"Calculate the present Transmission Heat Koefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
