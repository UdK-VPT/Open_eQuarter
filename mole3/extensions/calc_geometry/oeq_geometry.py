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
    from qgis.PyQt.QtCore import QVariant
    # factor for golden rule
    dataset = {'AREA': NULL, 'PERIMETER': NULL, 'LENGTH': NULL, 'WIDTH': NULL, 'HEIGHT': NULL, 'FLOORS': NULL,
               'WN_RAT':NULL,'WL_COM':NULL,'BS_AR':NULL,'WL_AR':NULL,'WN_AR':NULL,'RF_AR':NULL,'LIV_AR':NULL}
    dataset.update(parameters)
    #print parameters
    if (not oeq_global.isnull(dataset['AREA'])):
        if (not oeq_global.isnull(dataset['PERIMETER'])):
            if oeq_global.isnull(dataset['LENGTH']):
                p = -float(dataset['PERIMETER'] / 2.0)
                q = float(dataset['AREA'])
                if ((p / 2) ** 2) > q:
                    dataset['LENGTH'] = -p / 2 + ((((p / 2) ** 2) - q) ** 0.5)
                else:
                    dataset['LENGTH'] = -p / 4
            #print config.building_id_key

            #print 'LENGTH'
            #print dataset['LENGTH']
            #print 'AREA'
            #print dataset['AREA']

            dataset['WIDTH'] = float(dataset['AREA']) / float(dataset['LENGTH'])
            l_max = max(dataset['WIDTH'], dataset['LENGTH'])
            l_min = min(dataset['WIDTH'], dataset['LENGTH'])
            dataset['WIDTH'] = l_min
            dataset['LENGTH'] = l_max
        else:
            if oeq_global.isnull(dataset['WIDTH']):
                if oeq_global.isnull(dataset['LENGTH']):
                    dataset['LENGTH'] = (float(dataset['AREA']) / golden) ** 0.5
                dataset['WIDTH'] = float(dataset['AREA']) / dataset['LENGTH']
            else:
                dataset['LENGTH'] = float(dataset['AREA']) / dataset['WIDTH']
            l_max = max(dataset['WIDTH'], dataset['LENGTH'])
            l_min = min(dataset['WIDTH'], dataset['LENGTH'])
            dataset['WIDTH'] = l_min
            dataset['LENGTH'] = l_max
            dataset['PERIMETER'] = 2 * (dataset['WIDTH'] + dataset['LENGTH'])
    else:
        if (not oeq_global.isnull(dataset['PERIMETER'])):
            if oeq_global.isnull(dataset['WIDTH']):
                if oeq_global.isnull(dataset['LENGTH']):
                    dataset['LENGTH'] = float(dataset['PERIMETER']) / (2 + 2 * golden)
                dataset['WIDTH'] = float(dataset['AREA']) / dataset['LENGTH']
            else:
                dataset['LENGTH'] = float(dataset['AREA']) / dataset['WIDTH']
            l_max = max(dataset['WIDTH'], dataset['LENGTH'])
            l_min = min(dataset['WIDTH'], dataset['LENGTH'])
            dataset['WIDTH'] = l_min
            dataset['LENGTH'] = l_max
            dataset['AREA'] = dataset['WIDTH'] * dataset['LENGTH']
    if oeq_global.isnull(dataset['FLOORS']):
        if (not oeq_global.isnull(dataset['HEIGHT'])):
            dataset['FLOORS'] = floor(dataset['HEIGHT'] / 3.3)
        else:
            if (not oeq_global.isnull(parameters['PDENS'])):
                dataset['FLOORS'] = ceil(float(parameters['PDENS'] / 4000))
                dataset['HEIGHT'] = dataset['FLOORS'] * 3.3
    else:
        if (oeq_global.isnull(dataset['HEIGHT'])):
            dataset['HEIGHT'] = dataset['FLOORS'] * 3.3
    #print type(dataset['YOC'])
    #print dataset['YOC']
    if oeq_global.isnull(dataset['WN_RAT']) & (not oeq_global.isnull(parameters['YOC'])):
       # try:
       dataset['WN_RAT']=window_wall_ratio_AVG_by_building_age_lookup.get(parameters['YOC'])
        #except:
        #    pass

    if oeq_global.isnull(dataset['WL_COM']) & (not oeq_global.isnull(parameters['PDENS'])):
        dataset['WL_COM']=common_walls_by_population_density_corr.get(parameters['PDENS'])

    if oeq_global.isnull(dataset['BS_AR']) & (not oeq_global.isnull(dataset['AREA'])):
        dataset['BS_AR']=dataset['AREA']

    if oeq_global.isnull(dataset['WL_AR'])& (not oeq_global.isnull(dataset['PERIMETER'])) & (not oeq_global.isnull(dataset['WL_COM']))& (not oeq_global.isnull(dataset['WIDTH'])) & (not oeq_global.isnull(dataset['WN_RAT'])):
        dataset['WL_AR']=(dataset['PERIMETER']-dataset['WL_COM']* dataset['WIDTH'])* dataset['HEIGHT']*(1-dataset['WN_RAT'])

    if oeq_global.isnull(dataset['RF_AR']):
        dataset['RF_AR']=dataset['AREA']

    if oeq_global.isnull(dataset['WN_AR'])& (not oeq_global.isnull(dataset['PERIMETER'])) & (not oeq_global.isnull(dataset['WL_COM']))& (not oeq_global.isnull(dataset['WIDTH'])) & (not oeq_global.isnull(dataset['WN_RAT'])):
        dataset['WN_AR']=(dataset['PERIMETER']-dataset['WL_COM']* dataset['WIDTH'])*dataset['HEIGHT']*dataset['WN_RAT']

    if not oeq_global.isnull([dataset['AREA'],dataset['FLOORS']]):
        dataset['LIV_AR'] = float(dataset['AREA']) * float(dataset['FLOORS']) * 0.8
    #print dataset


    result = {}
    for i in list(dataset.keys()):
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    result['FLOORS']['type'] = QVariant.Int

    return result


extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='Geometry',
    extension_name='Building Dimensions',
    layer_name= 'Dimensions',
    field_id='DIM',
    source_type='none',
    par_in=['AREA', 'PERIMETER', 'LENGTH', 'WIDTH', 'HEIGHT', 'FLOORS', 'PDENS','YOC',config.building_id_key],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=False,
    description='Calculate the Building dimensions from scratch',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    evaluation_method=calculation)

extension.registerExtension(default=True)
