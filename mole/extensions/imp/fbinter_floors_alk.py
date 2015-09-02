# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config

def calculation(self=None, parameters={}):
    from PyQt4.QtCore import QVariant
    from qgis.core import NULL
    # print parameters
    # print parameters.values()
    result = {self.field_id + '_P': {'type': QVariant.String,
                                     'value': self.layer_name},
              'FLOORS': {'type': QVariant.Double,
                         'value': NULL}}
    if parameters != {}:
        print 'FLR Par In Before'
        print parameters
        # print sum([float(i) for i in parameters.values()]) / len(parameters)
        try:
            # print sum([float(i) for i in parameters.values()]) / len(parameters)
            result['FLOORS']['value'] = sum([float(i) for i in parameters.values()]) / len(parameters)
        except:
            pass
    print 'FLR Par In Past'
    print parameters

    return result
    # else:
    #    return {self.field_id + '_P': {'type': QVariant.String,
    #                                   'value': NULL},
    #           'FLOORS': {'type': QVariant.Double,
    #                      'value': NULL}}


import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='import',
    extension_name='Floors (ALK Berlin, WMS)',
    field_id='FLRS',
    source_type='wms',
    layer_name='Floors',
    active=True,
    description=u'',
    colortable=os.path.join(__file__[:-3] + '.qml'),
    source='crs=EPSG:4326&dpiMode=7&format=image/png&layers=2&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/alk_gebaeude',
    evaluation_method=calculation)

extension.registerExtension(default=True)
