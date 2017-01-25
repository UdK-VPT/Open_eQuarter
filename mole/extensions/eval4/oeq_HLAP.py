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
    dataset = {'HLAP': NULL}
    dataset.update(parameters)

  #  print '------'
  #  print dataset['AREA']
  #  print dataset['FLOORS']
    #print float(dataset['AREA']) * float(dataset['FLOORS']) * 0.8
  #  print dataset['BS_QTP']
  #  print dataset['RF_QTP']
  #  print dataset['WL_QTP']
  #  print dataset['WN_QTP']
    #print float(dataset['BS_QTP']) + float(dataset['RF_QTP']) + float(dataset['WL_QTP']) + float(dataset['WN_QTP'])*1.2


    if not oeq_global.isnull([dataset['AREA'] , dataset['FLOORS'] , dataset['BS_QTP'] , dataset['RF_QTP'] , dataset['WL_QTP'] , dataset['WN_QTP']]):
        living_area = float(dataset['AREA']) * float(dataset['FLOORS']) * 0.8
        qtp_total = float(dataset['BS_QTP']) + float(dataset['RF_QTP']) + float(dataset['WL_QTP']) + float(dataset['WN_QTP'])*1.2
        dataset['HLAP']=qtp_total/living_area
    #print qtp_total/living_area
  #  print '------'
    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Building Quality (QT per Living Area, Present)',
    layer_name= 'QT Building per Livig Area Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HLAP',
    source_type='none',
    par_in=['AREA','FLOORS','BS_QTP','RF_QTP','WL_QTP','WN_QTP'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HLAP'],
    description=u"Calculate the present Transmission Heat Loss per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
