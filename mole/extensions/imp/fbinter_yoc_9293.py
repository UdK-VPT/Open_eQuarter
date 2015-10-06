# -*- coding: utf-8 -*-

from mole import oeq_global
from PyQt4.QtCore import QVariant
from qgis.core import NULL


def calculation(self=None, parameters={}):
    # print parameters
    # print parameters.values()
    result = {self.field_id + '_P': {'type': QVariant.String,
                                     'value': self.layer_name},
              'YOC': {'type': QVariant.Double,
                      'value': oeq_global.OeQ_project_info['average_build_year']}}
    if parameters != {}:
        # print sum(float(parameters.values()))/len(parameters)
        try:
            result['YOC']['value'] = sum([float(i) for i in parameters.values()]) / len(parameters)
        except:
            result['YOC']['value'] = oeq_global.OeQ_project_info['average_build_year']

    return result


def calculation_OLD(self=None, parameters={}):
    from PyQt4.QtCore import QVariant
    from mole import oeq_global

    # print "YOC"
    #print parameters

    if parameters != {}:
        # print sum(float(parameters.values()))/len(parameters)
        if oeq_global.isnull(parameters[self.par_in[0]]) or oeq_global.isnull(parameters[self.par_in[1]]):
            return {self.field_id + '_P': {'type': QVariant.String,
                                           'value': self.layer_name},
                    'YOC': {'type': QVariant.Double,
                            'value': oeq_global.OeQ_project_info['average_build_year']}}
        else:
            return {self.field_id + '_P': {'type': QVariant.String,
                                           'value': self.layer_name},
                    'YOC': {'type': QVariant.Double,
                            'value': sum([float(i) for i in parameters.values()]) / len(parameters)}}
    else:
        return {self.field_id + '_P': {'type': QVariant.String,
                                       'value': NULL},
                'YOC': {'type': QVariant.Double,
                        'value': NULL}}


import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WMS',
    field_id='YOC',
    source_type='wms',
    extension_name='Year of Construction (92/93, WMS)',
    layer_name='Year of Construction (WMS Capture)',
    description=u'Gebäudealter 199293 Scan der Karte Gebäudealter 1992 93 '
                + u'aus der Veroeffentlichung: Staedtebauliche Entwicklung Berlins seit 1650 in Karten',
    source='crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/gebaeudealter',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    active=True,
    evaluation_method=calculation)

extension.registerExtension(default=True)
