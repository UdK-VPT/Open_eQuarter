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
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
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
        nominatimCRS=QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        transform = QgsCoordinateTransform(sourceCRS, nominatimCRS).transform
        location=transform(QgsPoint(longitude, latitude))
        latitude=location.y()
        longitude=location.x()
    urlParams = {'format': 'json',
                 'lat': str(latitude),
                 'lon' : str(longitude),
                 'addressdetails': '1',
                 'email':config.referrer_email
                 }
    url = 'https://nominatim.openstreetmap.org/reverse?' + urllib.parse.urlencode(urlParams)
    response = urllib.request.urlopen(url,timeout=10)
    result = json.load(response)
    # try:
    addrlist = []
    dataset = {'latitude':'','longitude':'','state':'','town':'','suburb':'','road':'','postcode':'','country':'','house_number':'',}
    dataset['latitude'] = result['lat']
    dataset['longitude'] = result['lon']
    for field in list(result['address'].keys()):
        dataset.update({field : result['address'][field]})
    if (dataset['town'] == ''): dataset['town'] = result['address']['city']
    if  bool(crs):
        transform2 = QgsCoordinateTransform(nominatimCRS,sourceCRS).transform
        location2=transform2(QgsPoint(float(dataset['longitude']), float(dataset['latitude'])))
        dataset['latitude']=location2.y()
        dataset['longitude']=location2.x()
    return([complete_nominatim_dataset(dataset)])
    # except:
    #    return []

# Get the coordinates for the specified adress
def getCoordinatesByAddress(address,crs=None):

    # In: Country, City, Postal Address or Parts of it
    #     Target Coordinate Reference System as EPSG Code

    # Out: dict of all informations delivered by googlemaps
    if isinstance(address, str):
        address = address.encode('utf-8')

    urlParams = {'q': address,
                 'format': 'json',
                'addressdetails': '1',
                 'email': config.referrer_email
        }
    url='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode(urlParams)
    #print(url);
    response = urllib.request.urlopen(url)
    result = json.load(response)

    # try:
    addrlist = []
    for addrrecord in result:
        dataset = {'latitude': '', 'longitude': '', 'state': '', 'town': '', 'suburb': '', 'road': '', 'postcode': '',
                   'country': '', 'house_number': '', }
        dataset.update({'latitude': addrrecord['lat']})
        dataset.update({'longitude': addrrecord['lon']})
        for field in list(addrrecord['address'].keys()):
            dataset.update({field: addrrecord['address'][field]})
        if (dataset['town'] == ''): dataset['town'] = addrrecord['address']['city']
        #print(crs);
        if crs:
           targetCRS = QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.EpsgCrsId)
           nominatimCRS = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
           location = QgsCoordinateTransform(nominatimCRS, targetCRS).transform(QgsPoint(float(dataset['longitude']), float(dataset['latitude'])))
           dataset['latitude'] = location.y()
           dataset['longitude'] = location.x()
        addrlist.append(complete_nominatim_dataset(dataset))
    # except:
    #    return []
    return addrlist

def complete_nominatim_dataset(dataset):
    mandatory_keys = ['house_number', 'town', 'state', 'road', 'lon', 'postcode',
                      '', 'lat', 'suburb', 'country']
    for i in mandatory_keys:
        if not i in list(dataset.keys()):
            dataset.update({i: ''})
    zip_city = ' '.join([dataset['postcode'], dataset['town']])
    dataset['formatted_location'] = ', '.join([dataset['road'], zip_city, dataset['country']])
    return dataset

def getCoordinatesByAddressTest(address,crs=None):
    import urllib.request, urllib.parse, urllib.error
    import urllib.request, urllib.error, urllib.parse
    import json
    if isinstance(address, str):
        address = address.encode('utf-8')

    urlParams = {'q': address,
                 'format': 'json',
                'addressdetails': '1',
                 'email':config.referrer_email
        }
    url='http://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode(urlParams)
    #print(url)
    response = urllib.request.urlopen(url)
    result =  json.load(response)
    addrlist = []
    #print(len)
    for addrrecord in result:
        dataset = {}
        dataset['latitude'] = addrrecord['lat']
        dataset['longitude'] = addrrecord['lon']
        #print(dataset)
        #if crs:
        #    location = transform(QgsPoint(dataset['longitude'], dataset['latitude']))
        #    dataset['latitude'] = location.y()
         #   dataset['longitude'] = location.x()
        #addrlist.append(complete_google_dataset(dataset))
    # except:
    #    return []
    return addrlist


#address ='Georg-Leoewenstein-Strasse 14, Berlin, Germany'
#print(address)


def translate_to_google_location_dataset(dataset):
    translation_table = {'house_number':'street_number',
                          'town': 'locality',
                          'state': 'sublocality_level_1',
                          'road': 'route',
                          'lon': 'longitude',
                          'postcode' : 'postal_code',
                          'country': 'country',
                          'lat':'latitude',
                          'suburb':'sublocality_level_2'}
    nominatim_keys = ['house_number','state','suburb','road','postcode','country','state']
    if not 'town' in list(dataset.keys()):
        dataset.update({'town':dataset['state']})


    for i in list(translation_table.keys()):
        if not i in list(dataset.keys()):
            dataset.update({i: ''})
    zip_city = ' '.join(filter(bool, [dataset['postal_code'], dataset['locality']]))
    dataset['formatted_location'] = ', '.join(filter(bool, [dataset['route'], zip_city, dataset['country']]))
    return dataset

def translate_to_nominatim_location_dataset(dataset):
    translation_table = {'street_number' : 'house_number',
                          'locality': 'town' ,
                          'sublocality_level_1' : 'state' ,
                          'route' : 'road',
                          'longitude' : 'lon' ,
                          'postal_code' : 'postcode'  ,
                          'country' : 'country' ,
                          'latitude' : 'lat',
                          'sublocality_level_2' : 'suburb'}
    nominatim_keys = ['house_number','state','suburb','road','postcode',]
    if not 'locality' in list(dataset.keys()):
        dataset.update({'locality':dataset['state']})


    for i in list(translation_table.keys()):
        if not i in list(dataset.keys()):
            dataset.update({i: ''})
    zip_city = ' '.join(filter(bool, [dataset['postal_code'], dataset['locality']]))
    dataset['formatted_location'] = ', '.join(filter(bool, [dataset['road'], zip_city, dataset['country']]))
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
    building=[x for x in provider.getFeatures() if x.attribute(config.building_id_key)==str(building_id)]
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
