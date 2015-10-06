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
    dataset = {'ACHL': NULL}
    dataset.update(parameters)

    print '------'
    print dataset['AREA']
    print dataset['FLOORS']
    #print float(dataset['AREA']) * float(dataset['FLOORS']) * 0.8
    print dataset['HHRS']

    #print float(dataset['BS_QTP']) + float(dataset['RF_QTP']) + float(dataset['WL_QTP']) + float(dataset['WN_QTP'])*1.2


    if not oeq_global.isnull([dataset['AREA'] , dataset['FLOORS'], dataset['HHRS']]):
        living_area = float(dataset['AREA']) * float(dataset['FLOORS']) * 0.8 * 0.8 #20% Construction, 20 % floors and stairs
        dataset['ACHL']= 20 * living_area *float(dataset['HHRS'])/1000
    #print qtp_total/living_area
    print '------'
    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Air change heat loss',
    layer_name= 'Air change heat loss',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='ACHL',
    source_type='none',
    par_in=['AREA','FLOORS','HHRS'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['ACHL'],
    description=u"Calculate Air Change Heat loss per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
