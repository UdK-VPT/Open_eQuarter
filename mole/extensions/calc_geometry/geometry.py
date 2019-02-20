# -*- coding: utf-8 -*-

import os
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import common_walls_by_population_density_corr,window_wall_ratio_AVG_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    dataset = {'LENGTH': NULL, 'WIDTH': NULL, 'HEIGHT': NULL,'WN_RAT':NULL,'WL_COM':NULL,'BS_AR':NULL,'WL_AR':NULL,'TWL_AR':NULL,'WN_AR':NULL,'RF_AR':NULL,'LIV_AR':NULL}
    #dataset.update(parameters)
    #calculate dimesion a and b of a representing rectangle from the proportion of AREA and PERIMETER
    if bool(parameters['PERIMETER']) & bool(parameters['AREA']):
        p = -float(parameters['PERIMETER'] / 2.0)
        q = float(parameters['AREA'])
        if ((p / 2) ** 2) > q:
            dimension_a = -p / 2 + ((((p / 2) ** 2) - q) ** 0.5)
        else:
            dimension_a = -p / 4

        # calculate length of a representing rectangle
        dimension_b = float(parameters['AREA']) / float(dimension_a)
        # set LENGTH to max of a and b and WIDTH to min
        dataset['WIDTH'] = min(dimension_a, dimension_b)
        dataset['LENGTH'] = max(dimension_a, dimension_b)

        dataset['HEIGHT'] = parameters['FLOORS'] * config.default_floor_height
        #print type(dataset['YOC'])
        #print dataset['YOC']

    if bool(parameters['YOC']):
       dataset['WN_RAT']=window_wall_ratio_AVG_by_building_age_lookup.get(parameters['YOC'])

    if bool(parameters['PDENS']):
        dataset['WL_COM']=common_walls_by_population_density_corr.get(parameters['PDENS'])

    if bool(parameters['AREA']):
        dataset['BS_AR']=parameters['AREA']

    if bool(parameters['PERIMETER']) & bool(dataset['HEIGHT']):
        dataset['TWL_AR']=(parameters['PERIMETER']*dataset['HEIGHT'])

    if bool(parameters['PERIMETER']) & bool(dataset['WL_COM'])  & bool(dataset['WIDTH'])  & bool(dataset['HEIGHT'])  & bool(dataset['WN_RAT']):
        dataset['WL_AR']=(parameters['PERIMETER']-dataset['WL_COM']* dataset['WIDTH'])* dataset['HEIGHT']*(1-dataset['WN_RAT'])

    if bool(parameters['AREA']):
        dataset['RF_AR']=parameters['AREA']

    if bool(parameters['PERIMETER']) & bool(dataset['WL_COM'])  & bool(dataset['WIDTH'])  & bool(dataset['HEIGHT'])  & bool(dataset['WN_RAT']):
        dataset['WN_AR']=(parameters['PERIMETER']-dataset['WL_COM']* dataset['WIDTH'])*dataset['HEIGHT']*dataset['WN_RAT']

    if bool([parameters['AREA'],parameters['FLOORS']]):
        dataset['LIV_AR'] = float(parameters['AREA']) * float(parameters['FLOORS']) * 0.8
    #print dataset


    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='General',
    extension_name='Building Dimensions',
    layer_name= 'Dimensions',
    field_id=None,
    source_type='none',
    par_in=['AREA', 'PERIMETER', 'FLOORS', 'PDENS','YOC'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    description=u'Calculate the Building dimensions from AREA, PERIMETER, FLOORS, PDENS and YOC',
    show_results=None,
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    evaluation_method=calculation)

extension.registerExtension(default=True)
