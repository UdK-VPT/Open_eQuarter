from PyQt4.QtGui import QMessageBox
from qgis.core import QgsProject

import qgis
import os
import time
from webbrowser import open as open_url


from mole.oeq_global import *
from mole.qgisinteraction import raster_layer_interaction
from mole.qgisinteraction import layer_interaction , legend


def save_wms_extent_as_image(wms_layer_name, max_res = 2064, geo_reference_output = True):

    export_wms_layer = legend.nodeByName(wms_layer_name)
    if not export_wms_layer: return None
    export_wms_layer = export_wms_layer[0].layer()
    iface = qgis.utils.iface
    canvas = iface.mapCanvas()

    current_crs = canvas.mapSettings().destinationCrs()
    current_extent = canvas.extent()
    export_extent = raster_layer_interaction.transform_wms_geo_data(export_wms_layer, current_extent, current_crs)

    #info_text = 'The current extent will now be clipped. This may take some time.'
    #QMessageBox.information(iface.mainWindow(), 'Info', info_text)
    if not geo_reference_output:
      export_wms_layer.setLayerName(export_wms_layer.name().replace("_RAW",""))

    filename = layer_interaction.save_layer_as_image(export_wms_layer, export_extent, OeQ_project_path(), max_res)

    if geo_reference_output:
         # wait until the file exists to add geo-references
        no_timeout = 30
        while not os.path.exists(filename) and no_timeout:
            time.sleep(0.1)
            no_timeout -= 1
        #dest_filename=os.path.splitext(filename)[0]
        dest_filename=filename.replace("_RAW","")
        print filename
        print dest_filename
        #dest_filename = os.path.splitext(filename)[0] + '_geo.tif'
        referencing = raster_layer_interaction.gdal_translate_layerfile(filename, dest_filename, current_crs.authid(), current_extent)

        if referencing != 0:
            print 'Error number {} occured, while referencing the output .tif'.format(referencing)
        else:
            #os.remove(filename)
            filename = dest_filename

    return filename

def getWmsLegendUrl(layer): #Very quick and very dirty
    m=layer.metadata()
    m=m.split('LegendURLs')
    for i in m:
        k=i.split("image/gif")
        if (type(k) is type([])) & (len(k) > 1): break
        k=i.split("image/jpg")
        if (type(k) is type([])) & (len(k) > 1): break
    if (type(k) is not type([])) | (len(k) < 2): return None
    k=k[1].split("http")
    if (type(k) is not type([])) | (len(k) < 2): return None
    url='http'+k[1].split('<')[0]
    return url
    #open_url(url,new=2) #2 means Open in a new TAB if possible
