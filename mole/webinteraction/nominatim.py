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
from qgis.core import QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsPoint,QgsProject

import inspect
DEBUG_MODE = False

nominatim_crs = QgsCoordinateReferenceSystem('EPSG:4326')

# Get the postal adress for the specified coordinates
def getBuildingLocationDataByCoordinates(longitude,latitude, crs=None):

    # In: Latitude
    #     Longitude
    #     Corresponding Coordinate Reference System as EPSG Code

    # Out: dict of all informations delivered by googlemaps
    if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)
    if bool(crs):
        crsSrc = QgsCoordinateReferenceSystem(int(config.default_extent_crs.split(':')[-1]),
                                              QgsCoordinateReferenceSystem.EpsgCrsId)
    else:
        crsSrc = QgsProject().instance().crs()


    # transform extent
    coord_transformer = QgsCoordinateTransform(crsSrc, nominatim_crs)
    location = coord_transformer.transform(longitude, latitude)

    latitude=location.y()
    longitude=location.x()
    urlParams = {'format': 'json',
                 'lat': str(latitude),
                 'lon' : str(longitude),
                 'addressdetails': '1',
                 'email':config.referrer_email
                 }
    url = 'https://nominatim.openstreetmap.org/reverse?' + urllib.parse.urlencode(urlParams)
    #print(url)
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(url,timeout=10)
    result = json.load(response)
    # try:
    addrlist = []
    dataset = {'latitude':'','longitude':'','state':'','town':'','city':'','suburb':'','road':'','postcode':'','country':'','house_number':'', 'crs':''}
    dataset['latitude'] = result['lat']
    dataset['longitude'] = result['lon']
    dataset.update({'crs': nominatim_crs.authid()})
    for field in list(result['address'].keys()):
        dataset.update({field : result['address'][field]})
    if (dataset['town'] == ''): dataset['town'] = dataset['city']
    if (dataset['town'] == ''): dataset['town'] = dataset['state']
    coord_transformer2 = QgsCoordinateTransform(nominatim_crs,crsSrc)
    location2 = coord_transformer2.transform(float(dataset['latitude']), float(dataset['longitude']))
    dataset['latitude']=location2.y()
    dataset['longitude']=location2.x()
    dataset['crs'] = crsSrc.authid()
    return([complete_nominatim_dataset(dataset)])
    # except:
    #    return []

# Get the coordinates for the specified adress
def getCoordinatesByAddress(address="",crs=None):

    # In: Country, City, Postal Address or Parts of it
    #     Target Coordinate Reference System as EPSG Code

    # Out: dict of all informations delivered by googlemaps
    if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)

    #if isinstance(address, str):
    #    address = address.encode('utf-8')
    #paramstring = "street="+street+"&country="+country+"&city="+city+"&format=json&addressdetails=1&email="+config.referrer_email
    #old 3
    # urlParams = {'street': street,
    #             'country':country,
     #            'city':city,
     #            'format': 'json',
     #           'addressdetails': '1',
     #           'email': config.referrer_email
     #   }
    urlParams = {'q': address,
                'format': 'json',
                'addressdetails': '1',
                'email': config.referrer_email
                }
    url='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode(urlParams)
   # print(url);
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    connected = 0
    maxtries = 10
    response = None
    while connected < maxtries:
        try:
            response = urllib.request.urlopen(url)
            connected = maxtries+1
            time.sleep(0.3)
        except:
            connected+= 1
    if connected == maxtries:
        print("Could not connect to '{}'".format(url))
    result = json.load(response)
    # print("RESULT",result)
    #result = filter(lambda i: (i['class']=="highway") & (i['type']!="pedestrian"),result)
    # try:
    addrlist = []
    if crs != None:
        targetCRS = QgsCoordinateReferenceSystem(crs)
    else:
        targetCRS = QgsProject.instance().crs()
       # print ('NOMINATIM',nominatim_crs.authid())
       # print('TARGET', targetCRS.authid())
    # for QGIS 3
    #transform = QgsCoordinateTransform(nominatim_crs, targetCRS, QgsProject.instance()).transform
    # for QGIS 2
    transform = QgsCoordinateTransform(nominatim_crs, targetCRS).transform

    for addrrecord in result:
#        if addrrecord['type'] == 'house':
        if (addrrecord['class'] == 'building') or (addrrecord['type'] in ['house','residential']):

           # print('LatBef',addrrecord['lat'])
           # print('LonBef', addrrecord['lon'])
            dataset = {'latitude': '', 'longitude': '', 'state': '', 'town': '', 'city': '', 'suburb': '', 'road': '', 'postcode': '',
                       'country': '', 'house_number': '', 'crs':''}
            location = transform(float(addrrecord['lon']),float(addrrecord['lat']))
            dataset.update({'longitude': location.x()})
            dataset.update({'latitude': location.y()})
            dataset.update({'crs': targetCRS.authid()})

            for field in list(addrrecord['address'].keys()):
                dataset.update({field: addrrecord['address'][field]})
            if (dataset['town'] == ''): dataset['town'] = dataset['city']
            if (dataset['town'] == ''): dataset['town'] = dataset['state']
            #Sprint(dataset);

            #print("Location", location)
            addrlist+= [complete_nominatim_dataset(dataset)]
        #print(addrlist)
        # except:
        #    return []
       # print('ADRESSES',addrlist)
    return addrlist

def complete_nominatim_dataset(dataset):
    if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)

    mandatory_keys = ['house_number', 'town', 'state', 'road', 'lon', 'postcode',
                      '', 'lat', 'suburb', 'country', 'crs']
    for i in mandatory_keys:
        if not i in list(dataset.keys()):
            dataset.update({i: ''})
    zip_city = ' '.join([dataset['postcode'], dataset['town']])
    dataset['formatted_location'] = ', '.join([dataset['road'], zip_city, dataset['country']])
    return dataset

def getCoordinatesByAddressTest(address,crs=None):
    if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)

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
    if crs:
        targetCRS = QgsCoordinateReferenceSystem(crs)
    else:
        targetCRS = QgsProject.instance().crs()
       # print ('NOMINATIM',nominatim_crs.authid())
       # print('TARGET', targetCRS.authid())
    transform = QgsCoordinateTransform(nominatim_crs, targetCRS, QgsProject.instance()).transform

    for addrrecord in result:
        dataset = {}
        location = transform(QgsPoint(addrrecord['lon'], addrrecord['lat']))
        dataset['latitude'] = location.y()
        dataset['longitude'] = location.x()
        dataset['crs'] = targetCRS.authid()

    # except:
    #    return []
    return addrlist


#address ='Georg-Leoewenstein-Strasse 14, Berlin, Germany'
#print(address)


def translate_to_google_location_dataset(dataset):
    if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)

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
    if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)

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
    if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)

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
    if DEBUG_MODE: print("debug", inspect.currentframe().f_code.co_name)

    from mole.qgisinteraction import legend
    from mole.project import config
    adress=getBuildingLocationDataByBLD_ID(building_id)
    if adress:
        adress = adress[0]

    return {'latitude':adress['latitude'],'longitude':adress['longitude'],'crs': config.project_crs}
