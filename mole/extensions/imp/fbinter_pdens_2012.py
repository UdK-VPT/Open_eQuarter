# -*- coding: utf-8 -*-


from mole import oeq_global
from PyQt4.QtCore import QVariant
from qgis.core import NULL
from mole.project import config


def calculation(self=None, parameters={}):
    # print parameters
    # print parameters.values()
    result = {self.field_id + '_P': {'type': QVariant.String,
                                     'value': self.layer_name},
              'PDENS': {'type': QVariant.Double,
                        'value': oeq_global.OeQ_project_info['population_density']}}
    if parameters != {}:
        # print sum(float(parameters.values()))/len(parameters)
        try:
            result['PDENS']['value'] = sum([float(i) for i in parameters.values()]) / len(parameters)
        except:
            result['PDENS']['value'] = oeq_global.OeQ_project_info['population_density']

    return result

import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WMS',
    extension_name='Population Density (2012, WMS)',
    field_id='PDENS',
    source_type='wms',
    layer_name='Population Density (WMS Capture)',
    active=True,
    description=u'',
    source='crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k06_06ewdichte2012',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    evaluation_method=calculation)

extension.registerExtension(default=True)
