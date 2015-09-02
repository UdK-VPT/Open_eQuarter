# -*- coding: utf-8 -*-

import os
from mole.extensions import OeQExtension


def calculation(self=None, parameters={}):
    from PyQt4.QtCore import QVariant
    from mole.stat_util import bld_geometry
    from mole import oeq_global
    dims = bld_geometry.dimensions(parameters['AREA'], parameters['PERIMETER'], parameters['LENGTH'])
    height = parameters['HEIGTH']
    floors = parameters['FLOORS']
    if oeq_global.isnull(floors):
        if oeq_global.isnull(height):
            floors = 5
        else:
            floors = float(height) / 3.3
    else:
        if oeq_global.isnull(height):
            height = floors * 3.3

    result = {self.field_id + '_P': {'type': QVariant.String,
                                     'value': self.layer_name}}
    for i in dims.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dims[i]}})

    result.update({'HEIGTH': {'type': QVariant.Double,
                              'value': height}})
    result.update({'FLOORS': {'type': QVariant.Double,
                              'value': floors}})
    return result


def dimensions(par_in):
    from scipy.constants import golden
    # factor for golden rule
    dataset = {'AREA': NULL, 'PERIMETER': NULL, 'LENGTH': NULL, 'WIDTH': NULL, 'HEIGTH': NULL, 'FLOORS': NULL}
    dataset.update(par_in)
    if (not isnull(dataset['AREA'])):
        if (not isnull(dataset['PERIMETER'])):
            if isnull(dataset['LENGTH']):
                p = -float(dataset['PERIMETER'] / 2.0)
                q = float(dataset['AREA'])
                dataset['LENGTH'] = -p / 2 + ((((p / 2) ** 2) - q) ** 0.5)
            dataset['WIDTH'] = float(dataset['AREA']) / float(dataset['LENGTH'])
        else:
            if isnull(dataset['WIDTH']):
                if isnull(dataset['LENGTH']):
                    dataset['LENGTH'] = (float(dataset['AREA']) / golden) ** 0.5
                dataset['WIDTH'] = float(dataset['AREA']) / dataset['LENGTH']
            else:
                dataset['LENGTH'] = float(dataset['AREA']) / dataset['WIDTH']
            dataset['PERIMETER'] = 2 * (dataset['WIDTH'] + dataset['LENGTH'])
    else:
        if (not isnull(dataset['PERIMETER'])):
            if isnull(dataset['WIDTH']):
                if isnull(dataset['LENGTH']):
                    dataset['LENGTH'] = float(dataset['PERIMETER']) / (2 + 2 * golden)
                dataset['WIDTH'] = float(dataset['AREA']) / dataset['LENGTH']
            else:
                dataset['LENGTH'] = float(dataset['AREA']) / dataset['WIDTH']
            dataset['AREA'] = dataset['WIDTH'] * dataset['LENGTH']

            Umsetzung in QVARIANT!
        return dataset

    extension = OeQExtension(
        extension_id=__name__,

        category='eval',
        extension_name='Dimensions',
        field_id='DIM',
        source_type='none',
        par_in=['AREA', 'PERIMETER', 'LENGTH', 'WIDTH', 'HEIGTH', 'FLOORS'],
        active=True,
        description=u'',
        evaluation_method=calculation)

    extension.registerExtension(default=True)

    from math import sqrt
    from scipy.constants import golden

    from qgis.core import *

    def isnull(value):
        return type(value) is type(NULL)

    def lenwidth(U, A):
        Perq = float(U / 4.0)
        print Perq
        A = float(A)
        print A
        l = Perq + (((Perq ** 2) - A) ** 0.5)
        l1 = Perq - (((Perq ** 2) - A) ** 0.5)
        w = A / l
        print 'Länge  ' + str(l)
        print 'Länge  ' + str(l1)
        print 'Breite ' + str(w)
        print 'Fläche ' + str(A)
        print 'ber    ' + str(l * w)
        print 'Umfang ' + str(U)
        print 'ber    ' + str(2 * (l + w))

    def dimensions(par_in):
        from scipy.constants import golden
        # factor for golden rule
        dataset = {'AREA': NULL, 'PERIMETER': NULL, 'LENGTH': NULL, 'WIDTH': NULL, 'HEIGTH': NULL, 'FLOORS': NULL}
        dataset.update(par_in)
        if (not isnull(dataset['AREA'])):
            if (not isnull(dataset['PERIMETER'])):
                if isnull(dataset['LENGTH']):
                    p = -float(dataset['PERIMETER'] / 2.0)
                    q = float(dataset['AREA'])
                    dataset['LENGTH'] = -p / 2 + ((((p / 2) ** 2) - q) ** 0.5)
                dataset['WIDTH'] = float(dataset['AREA']) / float(dataset['LENGTH'])
            else:
                if isnull(dataset['WIDTH']):
                    if isnull(dataset['LENGTH']):
                        dataset['LENGTH'] = (float(dataset['AREA']) / golden) ** 0.5
                    dataset['WIDTH'] = float(dataset['AREA']) / dataset['LENGTH']
                else:
                    dataset['LENGTH'] = float(dataset['AREA']) / dataset['WIDTH']
                dataset['PERIMETER'] = 2 * (dataset['WIDTH'] + dataset['LENGTH'])
        else:
            if (not isnull(dataset['PERIMETER'])):
                if isnull(dataset['WIDTH']):
                    if isnull(dataset['LENGTH']):
                        dataset['LENGTH'] = float(dataset['PERIMETER']) / (2 + 2 * golden)
                    dataset['WIDTH'] = float(dataset['AREA']) / dataset['LENGTH']
                else:
                    dataset['LENGTH'] = float(dataset['AREA']) / dataset['WIDTH']
                dataset['AREA'] = dataset['WIDTH'] * dataset['LENGTH']
        return dataset
