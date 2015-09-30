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
    dataset = {'AVR': NULL}
    dataset.update(parameters)
    volume = float(dataset['AREA']) * float(dataset['HEIGHT'])
    env_area =  float(dataset['BS_AR']) + float(dataset['RF_AR']) + float(dataset['WL_AR']) + float(dataset['WN_AR'])
    dataset['AVR']=env_area/volume
    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='AV Ratio',
    layer_name= 'AV Ratio',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='AVR',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','AREA','HEIGHT'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['AVR'],
    description=u"Calculate the present Transmission Heat Koefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
