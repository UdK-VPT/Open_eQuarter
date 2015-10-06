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
    dataset = {'HLAC': NULL}
    dataset.update(parameters)

    if not oeq_global.isnull([dataset['AREA'] , dataset['FLOORS'] , dataset['BS_QTC'] , dataset['RF_QTC'] , dataset['WL_QTC'] , dataset['WN_QTC']]):
        living_area = float(dataset['AREA']) * float(dataset['FLOORS']) * 0.8
        qtp_total = float(dataset['BS_QTC']) + float(dataset['RF_QTC']) + float(dataset['WL_QTC']) + float(dataset['WN_QTC'])*1.2
        dataset['HLAC']=qtp_total/living_area
    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Building Quality (QT per Livig Area, Contemporary)',
    layer_name= 'QT Building per Livig Area Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HLAC',
    source_type='none',
    par_in=['AREA','FLOORS','BS_QTC','RF_QTC','WL_QTC','WN_QTC'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['HLAC'],
    description=u"Calculate the contemporary Transmission Heat Loss per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
