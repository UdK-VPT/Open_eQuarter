
from qgisinteraction import layer_interaction
from mole.project import config
from qgis.core import QgsCoordinateReferenceSystem
import urllib
import urllib2
import json

def getAddressByCoordinates(latitude,longitude,crs=None):
    if crs:
        sourceCRS=QgsCoordinateReferenceSystem(crs)
        googleMapsCRS=QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(sourceCRS, googleMapsCRS).transform
        location=transform(QgsPoint(longitude, latitude))
        latitude=location.y()
        longitude=location.x()
    url='http://maps.google.com/maps/api/geocode/json?sensor=false&latlng='+str(latitude)+','+str(longitude)
    response = urllib2.urlopen(url)
    result = json.load(response)
    try:
        out={}
        addrcomp= result['results'][0]['address_components']
        for i in addrcomp:
            out[i['types'][0]]=i['long_name']
        geom= result['results'][0]['geometry']
        out['latitude=']=geom['location']['lat']
        out['longitude=']=geom['location']['lng']
        return out
    except:
        return None

def getCoordinatesByAddress(address,crs=None):
    urlParams = {
                'address': address,
                'sensor': 'false',
        }
    url='http://maps.google.com/maps/api/geocode/json?'+urllib.urlencode(urlParams)
    response = urllib2.urlopen(url)
    result = json.load(response)
    try:
        out={}
        addrcomp= result['results'][0]['address_components']
        for i in addrcomp:
           out[i['types'][0]]=i['long_name']
        geom= result['results'][0]['geometry']
        out['latitude']=geom['location']['lat']
        out['longitude']=geom['location']['lng']
    except:
            return None
    if crs:
        targetCRS=QgsCoordinateReferenceSystem(crs)
        googleMapsCRS=QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(googleMapsCRS,targetCRS).transform
        location=transform(QgsPoint(out['longitude'],out['latitude']))
        out['latitude']=location.y()
        out['longitude']=location.x()
    return out





def getAdressByBLD_ID(building_id):
    layer = layer_interaction.find_layer_by_name(config.pst_input_layer_name)
    if not layer: return None
    layerEPSG=int(layer.crs().authid()[5:])
    provider=layer.dataProvider()
    building=filter(lambda x: x.attribute('BLD_ID')==str(building_id), provider.getFeatures())
    if len(building)==0: return None
    geom = building[0].geometry()
    return getAddressByCoordinates(geom.asPoint().y(),geom.asPoint().x(), layerEPSG)
