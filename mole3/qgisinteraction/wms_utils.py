from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtGui import QPainter
from qgis.core import QgsProject, QgsMapRendererCustomPainterJob, QgsCoordinateTransform, QgsMapSettings
from mole3.oeq_global import OeQ_project_path
from osgeo import gdal
import os
import qgis
import os
import time
from webbrowser import open as open_url


from mole3.oeq_global import *
from mole3.qgisinteraction import raster_layer_interaction
from mole3.qgisinteraction import layer_interaction , legend



def wms_saveCanvasExtent(layername, filename="", crs=""):
    print(layername)
    layer = QgsProject().instance().mapLayersByName(layername)[0]
    wmsuri = layer.metadataUri()
    imgformat = wmsuri.split('format=')[1].split('&')[0]
    canvext = iface.mapCanvas().extent()
    canvcrs = QgsProject().instance().crs()
    canvsize = iface.mapCanvas().size()
    wmscrs = layer.crs()
    transform = QgsCoordinateTransform(canvcrs, wmscrs, QgsProject().instance()).transform
    wmsext = transform(canvext)

    print(canvcrs.authid())
    print(canvext)
    print(wmscrs.authid())
    print(wmsext)

    # create filename
    if not filename:
        filename = layername.split('.')[0]
    else:
        filename = filename.split('.')[0]

    filename = '_'.join(filename.split(" "))

    new_layername = filename

    temp_filename = filename + "." + imgformat.split('/')[1]

    filename = filename + ".tif"

    img = QImage(canvsize, QImage.Format_ARGB32_Premultiplied)

    # color = QColor(255, 255, 255)
    # img.fill(color.rgb())

    # create painter
    p = QPainter()
    p.begin(img)
    p.setRenderHint(QPainter.Antialiasing)

    mapSettings = QgsMapSettings()  # first create the map settings, then pass to a renderer
    # set layer set
    mapSettings.setLayers([layer])  # this takes a list of QgsMapLayer as input
    # set extent
    # rect = QgsRectangle(mapSettings.fullExtent())
    mapSettings.setExtent(wmsext)

    # set output size
    mapSettings.setOutputSize(
        img.size())  # dpi is now set separately (you would use mapsettings.setDpi(), but it's not necessary here)

    # do the rendering
    render = QgsMapRendererCustomPainterJob(mapSettings, p)  # takes the settings and painter as parameters
    render.start()  # rendering is now asynchronous, so you could use threads here
    render.waitForFinished()  # but we will block until it's finished
    p.end()

    # save image
    img.save(os.path.join(OeQ_project_path(), temp_filename), imgformat.split('/')[1])

    # open as gdal dataset
    ds = gdal.Open(os.path.join(OeQ_project_path(), temp_filename))
    ds.SetProjection(wmscrs.authid())

    # set transparency
    # ds.GetRasterBand(1).SetNoDataValue(255)
    # ds.GetRasterBand(2).SetNoDataValue(255)
    # ds.GetRasterBand(3).SetNoDataValue(255)

    bounds = [wmsext.xMinimum(), wmsext.yMaximum(), wmsext.xMaximum(), wmsext.yMinimum()]
    gdal.Translate(srcDS=ds,
                   destName=os.path.join(OeQ_project_path(), filename),
                   format="GTiff",
                   outputBounds=bounds,
                   widthPct=100,
                   heightPct=100,
                   outputSRS=wmscrs.authid())
    ds = None
    newlayer = iface.addRasterLayer(os.path.join(OeQ_project_path(), filename), new_layername)
    return (os.path.join(OeQ_project_path(), filename))

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
        #print filename
        #print dest_filename
        #dest_filename = os.path.splitext(filename)[0] + '_geo.tif'
        referencing = raster_layer_interaction.gdal_translate_layerfile(filename, dest_filename, current_crs.authid(), current_extent)

        if referencing != 0:
            print('Error number {} occured, while referencing the output .tif'.format(referencing))
        else:
            #os.remove(filename)
            filename = dest_filename

    return filename






def getWmsLegendUrl(layer): #Very quick and very dirty
    url = None
    try:
        url="http" +layer.metadata().split('LegendURLs')[1].split("image/")[1].split("http")[1].split("<")[0]
    except: pass
    return url


