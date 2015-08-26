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


extension = OeQExtension(
    extension_id=__name__,

    category='evaluation',
    extension_name='Dimensions',
    field_id='DIM',
    source_type='none',
    par_in=['AREA', 'PERIMETER', 'LENGTH', 'HEIGTH', 'FLOORS'],
    active=True,
    description=u'',
    evaluation_method=calculation)

extension.registerExtension(default=True)
