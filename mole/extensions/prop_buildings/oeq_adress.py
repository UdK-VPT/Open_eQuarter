# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from qgis.core import NULL
    from mole.webinteraction import googlemaps
    from PyQt4.QtCore import QVariant
    if bool(feature):
        crs = int(self.layer('source').crs().authid().split(':')[1])
        #print self.layer('source').crs().authid()
        #print crs
        #print parameters
        bdata = googlemaps.getBuildingLocationDataByCoordinates(parameters['LON'], parameters['LAT'] , crs = crs)
        try:
            bdata = bdata[0]
        except:
            pass
        #print bdata

        #print bdata
        if bool(bdata):
            return {  'BLD_LON2': {'type': QVariant.Double, 'value': str(bdata[u'longitude'])},
                      'BLD_LAT2': {'type': QVariant.Double, 'value': str(bdata[u'latitude'])},
                      'BLD_NUM': {'type': QVariant.String , 'value':bdata[u'street_number'].encode('utf8')},
                      'BLD_STR': {'type': QVariant.String, 'value': bdata[u'route'].encode('utf8')},
                      'BLD_COD': {'type': QVariant.String, 'value': bdata[u'postal_code'].encode('utf8')},
                      'BLD_CTY': {'type': QVariant.String, 'value': bdata[u'administrative_area_level_1'].encode('utf8')},
                      'BLD_CTR': {'type': QVariant.String, 'value': bdata[u'country'].encode('utf8')},
                      'BLD_CRS': {'type': QVariant.String, 'value': str(crs)}
                 }

    return {'BLD_LON2': {'type': QVariant.String, 'value': NULL},
                      'BLD_LAT2': {'type': QVariant.String, 'value': NULL},
                      'BLD_NUM': {'type': QVariant.String, 'value': NULL},
                      'BLD_STR': {'type': QVariant.String, 'value': NULL},
                      'BLD_COD': {'type': QVariant.String, 'value': NULL},
                      'BLD_CTY': {'type': QVariant.String, 'value': NULL},
                      'BLD_CTR': {'type': QVariant.String, 'value': NULL},
                      'BLD_CRS': {'type': QVariant.String, 'value': NULL}}

extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='General',
    extension_name='Building Adress',
    layer_name= None,
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='ADRESS',
    source_type='none',
    par_in=['LON','LAT'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=None,
    description=u"Building Adress",
    evaluation_method=calculation)

extension.registerExtension(default=True)

