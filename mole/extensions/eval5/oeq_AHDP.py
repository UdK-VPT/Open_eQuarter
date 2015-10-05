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
    dataset = {'AHDP': NULL}
    dataset.update(parameters)

    print '------'
    print dataset['HLAP']

    if not oeq_global.isnull([dataset['HLAP']]):
        dataset['AHDP']= float(dataset['HLAP']) + 40.0 * 0.8
        # Air Change Heatloss for standard Rooms 40kWh/m2a nach Geiger Lüftung im Wohnungsbau
        # 20% of the Total Area are used for stairs and floors


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
    extension_name='AHD Building per Livig Area Present',
    layer_name= 'Annual Heat Demand (per Living Area, Present)',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='AHDP',
    source_type='none',
    par_in=['HLAP'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['AHDP'],
    description=u"Calculate present Annual Heat Demand per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
