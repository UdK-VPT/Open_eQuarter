# -*- coding: utf-8 -*-
"""
/****************************************************************************************

 Project:               Open eQuarter / Mole
 Module:                webinteraction.googlemaps
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
from qgis.core import *
import urllib
import urllib2
import json


# Get the postal adress for the specified coordinates
def getAddressByCoordinates(latitude,longitude,crs=None):

    # In: Latitude
    #     Longitude
    #     Corresponding Coordinate Reference System as EPSG Code

    # Out: dict of all informations delivered by googlemaps

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

# Get the coordinates for the specified adress
def getCoordinatesByAddress(address,crs=None):

    # In: Country, City, Postal Address or Parts of it
    #     Target Coordinate Reference System as EPSG Code

    # Out: dict of all informations delivered by googlemaps
    if isinstance(address, unicode):
        address = address.encode('utf-8')

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





# Get the postal adress for the specified BLD_ID
# (QeQ Specific Building Identifier thoughout all tables)
def getAdressByBLD_ID(building_id):

    # In: BLD_ID
    #     Target Coordinate Reference System as EPSG Code

    # Out: dict of all informations delivered by googlemaps

    layer = layer_interaction.find_layer_by_name(config.pst_input_layer_name)
    if not layer: return None
    layerEPSG=int(layer.crs().authid()[5:])
    provider=layer.dataProvider()
    building=filter(lambda x: x.attribute('BLD_ID')==str(building_id), provider.getFeatures())
    if len(building)==0: return None
    geom = building[0].geometry()
    return getAddressByCoordinates(geom.asPoint().y(),geom.asPoint().x(), layerEPSG)
