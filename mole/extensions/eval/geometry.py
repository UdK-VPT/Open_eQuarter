# -*- coding: utf-8 -*-

import os
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension


def calculation(self=None, parameters={}):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    dataset = {'AREA': NULL, 'PERIMETER': NULL, 'LENGTH': NULL, 'WIDTH': NULL, 'HEIGHT': NULL, 'FLOORS': NULL,
               'PDENS': NULL}
    dataset.update(parameters)
    if (not oeq_global.isnull(dataset['AREA'])):
        if (not oeq_global.isnull(dataset['PERIMETER'])):
            if oeq_global.isnull(dataset['LENGTH']):
                p = -float(dataset['PERIMETER'] / 2.0)
                q = float(dataset['AREA'])
                if ((p / 2) ** 2) > q:
                    dataset['LENGTH'] = -p / 2 + ((((p / 2) ** 2) - q) ** 0.5)
                else:
                    dataset['LENGTH'] = -p / 4
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
            if (not oeq_global.isnull(dataset['PDENS'])):
                dataset['FLOORS'] = ceil(float(dataset['PDENS'] / 4000))
                dataset['HEIGHT'] = dataset['FLOORS'] * 3.3
    else:
        if (oeq_global.isnull(dataset['HEIGHT'])):
            dataset['HEIGHT'] = dataset['FLOORS'] * 3.3

    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    result['FLOORS']['type'] = QVariant.Int

    return result


extension = OeQExtension(
    extension_id=__name__,

    category='evaluation',
    extension_name='Building Dimensions',
    field_id='DIM',
    source_type='none',
    par_in=['AREA', 'PERIMETER', 'LENGTH', 'WIDTH', 'HEIGHT', 'FLOORS', 'PDENS'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    description=u'Calculate the Building dimensions from scratch',
    evaluation_method=calculation)

extension.registerExtension(default=True)
