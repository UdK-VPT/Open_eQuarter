# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from qgis.PyQt.QtCore import QVariant
    try:
        volume  =  float(parameters['AREA']) * float(parameters['HEIGHT'])
    except:
        volume = NULL
    return{'VOLUME':{'type': QVariant.Double,
                        'value': volume}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Geometry',
    extension_name='Building Volume',
    layer_name= 'Building Volume',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    #field_id='VOLUME',
    source_type='layer',
    par_in=['AREA','HEIGHT'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['VOLUME'],
    description="Calculate the Volume of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)

if __name__ == "__main__":
    calculation(None,{'AREA':400,'HEIGHT':12})