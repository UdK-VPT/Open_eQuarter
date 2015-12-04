from qgisinteraction import layer_interaction,
from mole.project import config
from qgis.core import QgsCoordinateReferenceSystem, QgsFeature


def get_address(building_id):
    googleMapsCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
    layer = layer_interaction.find_layer_by_name(config.pst_input_layer_name)
    layerCrs = layer.crs()
    print config.pst_input_layer_name
    print googleMapsCrs.authid()
    print layerCrs.authid()
    transform = QgsCoordinateTransform(layerCrs, googleMapsCrs).transform
    provider = layer.dataProvider()
    building = filter(lambda x: x.attribute('BLD_ID') == str(building_id), provider.getFeatures())
    if len(building) == 0: return None
    geom = building[0].geometry()
    # if geom.vectorType() == QGis.Point:
    location = transform(geom.asPoint())
    url = 'http://maps.google.com/maps/api/geocode/json?sensor=false&latlng=' + str(location.y()) + ',' + str(
        location.x())
    print url
    response = urllib2.urlopen(url)
    result = json.load(response)
    print result
    try:
        return result['results'][0]['address_components']
    except:
        return None
        '''
        http: // maps.google.com / maps / api / geocode / json?sensor = false & latlng = 37.4418834, -122.1430195

        http: // maps.google.com / maps / api / geocode / json?sensor = false & latlng = 1497629.51478, 6891333.65947
        '''
