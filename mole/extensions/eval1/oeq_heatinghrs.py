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
    dataset = {'HHRS':NULL}
    dataset.update(parameters)
    print [dataset[i] for i in dataset.keys()]
    print oeq_global.OeQ_project_info['heating_degree_days']
    dataset['HHRS']=float(oeq_global.OeQ_project_info['heating_degree_days']) * 24

    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    #extension_id=__name__,
    category='Evaluation',
    subcategory='General',
    extension_name='Average Heating Hours',
    layer_name= 'Average Heating Hours',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='HHRS',
    source_type='none',
    par_in=[],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['HHRS'],
    description=u"Calculate Average Heating Hours",
    evaluation_method=calculation)

extension.registerExtension(default=True)
