# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config

def calculation(self=None, parameters={}):
#    print self.extension_name()
#    self.layer_in=self.load_wfs().name
#    print self.layer_in
    return {}



import os
from mole.extensions import OeQExtension
from mole.project import config
extension = OeQExtension(
    extension_id=__name__,
    category='Basic',
    subcategory='WFS',
    extension_name='Building Outlines (ALK, WFS)',
    field_id='',   #used for point sampling tool
    par_in=[],
    par_out=['BLD_ID','AREA','PERIMETER'],
    source_type='wfs',
    layer_name=config.housing_layer_name,
    layer_in=None,
    layer_out=config.data_layer_name,
    active=True,
    description=u'',
    source='http://fbinter.stadt-berlin.de/fb/wfs/geometry/senstadt/re_hausumringe?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=fis:re_hausumringe&SRSNAME=EPSG:25833',
    source_crs='EPSG:25833',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    evaluation_method=calculation)

extension.registerExtension(default=True)
