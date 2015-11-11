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
    dataset = {'AHDC': NULL}
    dataset.update(parameters)

 #   print '------'
  #  print dataset['HLAC']

    if not oeq_global.isnull([dataset['HLAC']]):
        dataset['AHDC']=float(dataset['HLAC']) + 40.0 * 0.8
        # Air Change Heatloss for standard Rooms 40kWh/m2a nach Geiger Lüftung im Wohnungsbau
        # 20% of the Total Area are used for stairs and floors


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
    extension_name='AHD Building per Livig Area Contemporary',
    layer_name= 'Annual Heat Demand (per Living Area, Contemporary)',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='AHDC',
    source_type='none',
    par_in=['HLAC'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['AHDC'],
    description=u"Calculate contemporary Annual Heat Demand per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)

'''
for k in range(1,25):
   print [e.extension_id for e in  ext.by_state(True)[k].required()]
'''
