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
            if (not isnull(i['BAT'])) & (0 != i['BAT']):
                to_remove.append(i.id())
        except:
            return False

    provider.deleteFeatures(to_remove)

    # in the Berlin Hausumringe WFS there are additional Attributes that are not important here. they are removed
    conversion_fields = [[u'AOG',u'FLRS_ALK'],[u'GFK',u'FUNC_ALK'],[u'BAW',u'KIND_ALK']]
    fields = filter(lambda f: f.name() not in [i[0] for i in conversion_fields], provider.fields())
    fieldnames =[field.name() for field in fields]
    to_remove = []
    count = 0
    for field in provider.fields():
        if field.name() in fieldnames:
            to_remove.append(count)
        count += 1

    provider.deleteAttributes(to_remove)
    layer.updateFields()

    # in the Berlin Hausumringe WFS there are additional Attributes that are not important here. they are removed
    layer.startEditing()
    for cf in conversion_fields:
        count = 0
        for field in provider.fields():
            #print field.name()
            if field.name() == cf[0]:
                layer.renameAttribute(count,cf[1])
                break
            count += 1
    layer.commitChanges()


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
    from qgis.core import QgsDistanceArea, QgsCoordinateReferenceSystem
    ar = NULL
    per = NULL
    id = NULL
    flr = NULL
    usage = NULL
    kind = NULL
    da_engine=QgsDistanceArea()
    da_engine.setSourceCrs(QgsCoordinateReferenceSystem(int(config.project_crs.split(':')[-1]), QgsCoordinateReferenceSystem.EpsgCrsId))
    da_engine.setEllipsoid(config.project_ellipsoid)
    da_engine.setEllipsoidalMode(True)
    if feature:
            geometry = feature.geometry()
            #print geometry
            ar = da_engine.measureArea(geometry)
            per =da_engine.measurePerimeter(geometry)
            id = feature[config.building_id_key] #necessary to safe dependency check
            flr = feature[u'FLRS_ALK']  # necessary to safe dependency check
            usage = feature[u'FUNC_ALK']  # necessary to safe dependency check
            kind = feature[u'KIND_ALK']  # necessary to safe dependency check

    #print ar
    #print per
    #print id

    return {config.building_id_key: {'type': QVariant.String,
                           'value': id},
            'AREA_ALK': {'type': QVariant.Double,
                           'value': ar},
            'PERI_ALK': {'type': QVariant.Double,
                           'value': per},
            'FLRS_ALK': {'type': QVariant.Double,
                           'value': flr},
            'FUNC_ALK': {'type': QVariant.Double,
                       'value': usage},
            'KIND_ALK': {'type': QVariant.Double,
                       'value': kind},
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
    #source='http://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_wfs_alkis_gebaeudeflaechen?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=fis:s_wfs_alkis_gebaeudeflaechen&SRSNAME=EPSG:25833',
    source='http://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_wfs_alkis_gebaeudeflaechen?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=fis:s_wfs_alkis_gebaeudeflaechen&SRSNAME=urn:ogc:def:crs:EPSG:6.9:25833',
    #source='http://fbinter.stadt-berlin.de/fb/wfs/geometry/senstadt/re_hausumringe?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=fis:re_hausumringe&SRSNAME=EPSG:25833',
    source_crs='EPSG:25833',
    bbox_crs='EPSG:25833',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    load_method= load,
    preflight_method = preflight,
    evaluation_method= evaluation,
    postflight_method = None)

extension.registerExtension(default=True)
