# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config
from mole.oeq_global import OeQ_get_bld_id, isnull


def load(self=None):
    self.load_wfs()
    return True


def preflight(self=None):
    from mole.project import config
    from PyQt4.QtCore import QVariant
    from qgis.core import QgsField
    from mole.qgisinteraction.layer_interaction import add_attributes_if_not_exists
    from mole.oeq_global import OeQ_get_bld_id
    layer = self.layer()
    #print layer.name()
    if layer == None:
        return False
    features = layer.getFeatures()
    provider = layer.dataProvider()
    #in the Berlin Hausumringe WFS there are additional Features that describe specific building parts. As they are not relevant here they are removed by usig the key "Bauart_sch"
    to_remove =[]
    for i in features:
        try:
            if not isnull(i['Bauart_sch']):
                to_remove.append(i.id())
        except:
            return False

    provider.deleteFeatures(to_remove)

    # in the Berlin Hausumringe WFS there are additional Attributes that are not important here. they are removed
    fields = provider.fields()
    provider.deleteAttributes(range(0,len(fields)))
    layer.updateFields()

    # create building_ids
    add_attributes_if_not_exists(layer, [QgsField(config.building_id_key,QVariant.String)])
    layer.updateFields()
    features = layer.getFeatures()
    layer.startEditing()
    for i in features:
        i[config.building_id_key] = OeQ_get_bld_id()
        layer.updateFeature(i)
    layer.commitChanges()
    return True

def evaluation(self=None, parameters={},feature=None):
    from PyQt4.QtCore import QVariant
    ar = None
    per = None
    id = None

    if feature:
            geometry = feature.geometry()
            #print geometry
            ar = geometry.area()
            per = geometry.length()
            id = feature[config.building_id_key] #necessary to safe dependency check
    #print ar
    #print per
    #print id

    return {config.building_id_key: {'type': QVariant.String,
                           'value': id},
            'AREA': {'type': QVariant.Double,
                           'value': ar},
            'PERIMETER': {'type': QVariant.Double,
                           'value': per}
            }

def postflight(self=None):
    return True
    #return self.createDatabase()



import os
from mole.extensions import OeQExtension
from mole.project import config
extension = OeQExtension(
    extension_id=__name__,
    category='',
    subcategory='',
    extension_name='Building Outlines (ALK, WFS)',
    extension_type='basic',
    field_id='',   #used for point sampling tool
    par_in= [], #[config.building_id_key,'AREA','PERIMETER'],
    #par_out=[config.building_id_key,'AREA','PERIMETER'],
    source_type='wfs',
    layer_name=config.building_outline_layer_name,
    sourcelayer_name=config.building_outline_layer_name,
    targetlayer_name=config.building_outline_layer_name,#config.data_layer_name,
    active=True,
    description=u'',
    source='http://fbinter.stadt-berlin.de/fb/wfs/geometry/senstadt/re_alkis_gebaeude?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=fis:re_alkis_gebaeude&SRSNAME=EPSG:25833',
   # source='http://fbinter.stadt-berlin.de/fb/wfs/geometry/senstadt/re_hausumringe?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=fis:re_hausumringe&SRSNAME=EPSG:25833',
    source_crs='EPSG:25833',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    load_method= load,
    preflight_method = preflight,
    evaluation_method= evaluation,
    postflight_method = None)

extension.registerExtension(default=True)
