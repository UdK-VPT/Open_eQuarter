# -*- coding: utf-8 -*-
"""
/****************************************************************************************

 Project:               Open eQuarter / Mole
 Module:                webinteraction.mapquest
 Description:           Georeferenced information mining
 Mandatory:             QGIS installation

 Responsibility:        Werner Kaul
                        werner.kaul@udk-berlin.de

 Creation Date:         2015-07-03

                               -------------------

 Development:           University of Arts Berlin
                        Institut für Architektur und Städtebau (IAS)
                        Fachgebiet Versorgungsplanung und Versorgungstechnik (VPT)
                        Einsteinufer 43
                        10587 Berlin
                        Germany

 Team:                  Christoph Nytsch-Geusen
                        nytsch@udk-berlin.de

                        Werner Kaul
                        werner.kaul@udk-berlin.de

                        Kim Gülle
                        kimonline@posteo.de

                               -------------------

 Copyright:             (c)2014-2015 University of Arts Berlin
                        Institut für Architektur und Städtebau (IAS)
                        Fachgebiet Versorgungsplanung und Versorgungstechnik (VPT)

 ****************************************************************************************/

/*****************************************************************************************

 This program is free software; you can redistribute it and/or modify it under the terms
 of the GNU General Public License as published by the Free Software Foundation; either
 version 2 of the License, or (at your option) any later version.

 All our software is developed to the best of our knowledge and belief. But we do not
 become liable for any damage or disadvantage caused by it's usage, outcomes or sideeffect
 in any way.

 *****************************************************************************************/
"""
# Import the PyQt and QGIS libraries
from mole.qgisinteraction import layer_interaction
from mole.project import config
#from qgis.core import *
import urllib
import urllib2
import json
from qgis.core import QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsPoint


# Get the postal adress for the specified coordinates
def getBuildingLocationDataByCoordinates(longitude,latitude, crs=None):

    # In: Latitude
    #     Longitude
    #     Corresponding Coordinate Reference System as EPSG Code

    # Out: dict of all informations delivered by googlemaps
    if bool(crs):
        sourceCRS=QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.EpsgCrsId)
        googleMapsCRS=QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        transform = QgsCoordinateTransform(sourceCRS, googleMapsCRS).transform
        location=transform(QgsPoint(longitude, latitude))
        latitude=location.y()
        longitude=location.x()
    url='http://maps.google.com/maps/api/geocode/json?sensor=false&latlng='+str(latitude)+','+str(longitude)
    response = urllib2.urlopen(url)
    result = json.load(response)
    # try:
    addrlist = []
    for addrrecord in result['results']:
        dataset = {}
        for i in addrrecord['address_components']:
            dataset[i['types'][0]] = i['long_name']
        geom = addrrecord['geometry']
        dataset['latitude'] = geom['location']['lat']
        dataset['longitude'] = geom['location']['lng']
        if  bool(crs):
            transform2 = QgsCoordinateTransform(googleMapsCRS,sourceCRS).transform
            location2=transform2(QgsPoint(dataset['longitude'], dataset['latitude']))
            dataset['latitude']=location2.y()
            dataset['longitude']=location2.x()
        addrlist.append(complete_google_dataset(dataset))
    return addrlist
    # except:
    #    return []

# Get the coordinates for the specified adress
def getCoordinatesByAddress(address,crs=None):

    # In: Country, City, Postal Address or Parts of it
    #     Target Coordinate Reference System as EPSG Code

    # Out: dict of all informations delivered by googlemaps
    if isinstance(address, unicode):
        address = address.encode('utf-8')

    urlParams = {'q': address,
                 'format': 'json',
                'addressdetails': '1',
        }
    url='http://nominatim.openstreetmap.org/search?'+urllib.urlencode(urlParams)

    response = urllib2.urlopen(url)
    result = json.load(response)
    #print result['results']

    # try:
    addrlist = []
    for addrrecord in result:
        dataset = {}
        dataset['latitude'] = addrrecord['lat']
        dataset['longitude'] = addrrecord['lon']
        if crs:
            targetCRS = QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.EpsgCrsId)
            googleMapsCRS = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
            location = QgsCoordinateTransform(googleMapsCRS, targetCRS).transform(QgsPoint(dataset['longitude'], dataset['latitude']))
            dataset['latitude'] = location.y()
            dataset['longitude'] = location.x()
        addrlist.append(complete_google_dataset(dataset))
    # except:
    #    return []
    return addrlist

def complete_google_dataset(dataset):
    mandatory_keys = [u'street_number', u'locality', u'sublocality_level_1', u'route', 'longitude', u'postal_code',
                      u'administrative_area_level_1', u'country', 'latitude'u'sublocality_level_2']
    for i in mandatory_keys:
        if not i in dataset.keys():
            dataset.update({i: ''})
    zip_city = ' '.join(filter(bool, [dataset['postal_code'], dataset['locality']]))
    dataset['formatted_location'] = ', '.join(filter(bool, [dataset['route'], zip_city, dataset['country']]))
    return dataset

def getCoordinatesByAddressTest(address,crs=None):
    import urllib
    import urllib2
    import json
    if isinstance(address, unicode):
        address = address.encode('utf-8')

    urlParams = {'q': address,
                 'format': 'json',
                'addressdetails': '1',
        }
    url='http://nominatim.openstreetmap.org/search?'+urllib.urlencode(urlParams)
    print url
    response = urllib2.urlopen(url)
    result =  json.load(response)
    addrlist = []
    print len
    for addrrecord in result:
        dataset = {}
        dataset['latitude'] = addrrecord['lat']
        dataset['longitude'] = addrrecord['lon']
        print dataset
        #if crs:
        #    location = transform(QgsPoint(dataset['longitude'], dataset['latitude']))
        #    dataset['latitude'] = location.y()
         #   dataset['longitude'] = location.x()
        #addrlist.append(complete_google_dataset(dataset))
    # except:
    #    return []
    return addrlist


address ='Georg-Leoewenstein-Strasse 14, Berlin, Germany'
print address


def translate_to_google_location_dataset(dataset):
    translation_table = {u'house_number':u'street_number',
                          u'town': u'locality',
                          u'state': u'sublocality_level_1',
                          u'road': u'route',
                          u'lon': 'longitude',
                          u'postcode' : u'postal_code',
                          u'country': u'country',
                          u'lat':'latitude',
                          u'suburb':u'sublocality_level_2'}
    nominatim_keys = [u'house_number',u'state',u'suburb',u'road',u'postcode',]
    if not 'town' in dataset.keys():
        dataset.update({u'town':dataset[u'state']})


    for i in translation_table.keys():
        if not i in dataset.keys():
            dataset.update({i: ''})
    zip_city = ' '.join(filter(bool, [dataset['postal_code'], dataset['locality']]))
    dataset['formatted_location'] = ', '.join(filter(bool, [dataset['route'], zip_city, dataset['country']]))
    return dataset






# Get the postal adress for the specified BLD_ID
# (QeQ Specific Building Identifier thoughout all tables)
def getBuildingLocationDataByBLD_ID(building_id, crs=None):
    # In: BLD_ID
    #     Target Coordinate Reference System as EPSG Code
    # Out: dict of all informations delivered by googlemaps
    from mole.qgisinteraction import legend
    from mole.project import config
    layer = legend.nodeByName(config.building_coordinate_layer_name)
    if not layer: return None
    layer = layer[0].layer()
    layerEPSG=int(layer.crs().authid()[5:])
    provider=layer.dataProvider()
    building=filter(lambda x: x.attribute(config.building_id_key)==str(building_id), provider.getFeatures())
    if len(building)==0: return None
    geom = building[0].geometry()
    result = getBuildingLocationDataByCoordinates(geom.asPoint().x(), geom.asPoint().y(), layerEPSG)
    for i in result:
        i.update({'crs':crs.authid()})
    return result

def getBuildingCoordinateByBLD_ID(building_id, crs=None):
    from mole.qgisinteraction import legend
    from mole.project import config
    adress=getBuildingLocationDataByBLD_ID(building_id)
    if adress:
        adress = adress[0]

    return {'latitude':adress['latitude'],'longitude':adress['longitude'],'crs': QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId).authid()}
