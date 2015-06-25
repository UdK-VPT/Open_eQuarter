from qgis.core import QgsRasterLayer, QgsApplication, QgsRaster, QgsCoordinateTransform, QgsCoordinateReferenceSystem
from PyQt4.QtGui import QColor
from platform import system
from os import path
import subprocess
import time
import GdalUtils


def get_environment():
    # setup the MacOSX path to both GDAL executables and python modules
    if system() == 'Darwin':
        GdalUtils.setMacOSXDefaultEnvironment()

    environment = GdalUtils.setProcessEnvironment()

    if system() == 'Windows':
        # The gdal-processing executables are located at <QGIS Installation folder>\bin
        # The gcs.csv-file (required as a GDAL_DATA env-var) is stored in <QGIS Installation folder>\share\gdal
        # The projection files (required as a PROJ_LIB env-var) are stored in <QGIS Installation folder>\share\proj
        # prefixPath() returns <QGIS Installation folder>\apps\qgis
        gdal_location = path.join(QgsApplication.prefixPath(), '..', '..', 'bin')
        gdal_data = path.join(QgsApplication.prefixPath(), '..', '..', 'share', 'gdal')
        gdal_python_tools = path.join(QgsApplication.prefixPath(), 'python', 'plugins', 'GdalTools')
        gdal_projection = path.join(QgsApplication.prefixPath(), '..', '..', 'share', 'proj')
        environment['PATH'] = str(path.abspath(gdal_location))
        environment['PYTHONPATH'] = str(path.abspath(gdal_python_tools))
        environment['GDAL_DATA'] = str(path.abspath(gdal_data))
        environment['PROJ_LIB'] = str(path.abspath(gdal_projection))

    return environment

def gdal_warp_layer(layer, target_crs):

    try:
        source_crs = layer.crs().toProj4()
        input_path = layer.publicSource()
        input_path = path.normpath(input_path)
        out_path = path.dirname(input_path)
        out_path = path.normpath(out_path)
        out_path = path.join(out_path, layer.name() + '_transformed.tif')
        environment = get_environment()

        # wait until the file exists to add geo-references
        while not path.exists(input_path):
            time.sleep(0.1)

        cmd = ['gdalwarp', '-s_srs', str(source_crs),'-t_srs', str(target_crs), input_path, out_path]

        gdalwarp = subprocess.Popen(cmd, env=environment)

        #ToDo Add timeout function
        return gdalwarp.wait()
    except AttributeError as Att_Error:
        print(Att_Error.message)


def gdal_addo_layerfile(file, sampling_algorithm, number_of_pyramids):

    environment = get_environment()
    pyramids = []
    for i in range(1,number_of_pyramids+1):
        pyramids.append(str(2**i))

    cmd = ['gdaladdo', '-r', sampling_algorithm, file] + pyramids

    gdaladdo = subprocess.Popen(cmd, env=environment)

    #ToDo Add timeout function
    return gdaladdo.wait()


def gdal_translate_layerfile(src_filename, dst_filename, crs, extent):
    """
    Call the gdal_translate command and add geo-information.
    :param src_filename: The file (in the format "/folder/subfolder/filename.tif") that needs to be referenced
    :type src_filename: str
    :param dst_filename: The destination of the referenced file in the format "/folder/subfolder/filename_goe.tif"
    :param crs: The destination coordinate reference system (must be the same crs as the extent's crs)
    :type crs: str
    :param extent: The extent holding the x- and y-coordinates of the layer
    :type extent: QgsRectangle
    :return:
    :rtype:
    """
    ulx = extent.xMinimum()
    uly = extent.yMaximum()
    lrx = extent.xMaximum()
    lry = extent.yMinimum()

    environment = get_environment()

    cmd = ['gdal_translate', '-a_srs', crs, '-a_ullr', repr(ulx), repr(uly), repr(lrx), repr(lry), str(src_filename.encode('utf-8')),
           str(dst_filename.encode('utf-8'))]

    # Error code 127 corresponds to 'command not found'
    gdal_process = subprocess.Popen(cmd, env=environment)

    #ToDo Add timeout function
    return gdal_process.wait()


def get_wms_url(wms_layer):
    """
    Extract the url of the server from which the given WMS-Layer was loaded.
    :param wms_layer: The WMS-layer
    :type wms_layer: QgsRasterLayer
    :return url: The url to the wms-server
    :rtype url: str
    """
    src = wms_layer.source()
    start = src.find('url=')
    url = ''
    if start > -1:
        start += 4
        end = src.find('&', start)
        if end > -1:
            url = src[start:end]
        else:
            url = src[start:]

    return url

def get_wms_crs(wms_layer):
    """
    Extract information in which crs the layer is provided by the WMS-server
    :param wms_layer: The WMS-layer
    :type wms_layer: QgsRasterLayer
    :return wms_crs: The crs provided by the server
    :rtype wms_crs: str
    """
    src = wms_layer.source()
    wms_crs = ''
    start = src.find('crs=')
    if start > -1:
        start += 4
        end = src.find('&', start)
        if end > -1:
            wms_crs = src[start:end]
        else:
            wms_crs = src[start:]

    return wms_crs


def transform_wms_geo_data(wms_layer, extent, extent_crs):
    """
    Transform the extent from the extent_crs to the crs of the server providing the wms_layer.
    :param wms_layer: The WMS-layer
    :type wms_layer: QgsRasterLayer
    :param extent: The extent which shall be transformed
    :type extent: QgsRectangle
    :param extent_crs: The crs which corresponds to the extent
    :type extent_crs: QgsCoordinateReferenceSystem
    :return extent: The extent (transformed to the WMS-server's crs)
    :rtype wms_crs: QgsRectangle
     """
    wms_crs = get_wms_crs(wms_layer)
    target_crs = QgsCoordinateReferenceSystem(wms_crs)

    if not extent_crs == target_crs:
        coord_transformer = QgsCoordinateTransform(extent_crs, target_crs)
        return coord_transformer.transform(extent)
    else:
        return extent


def extract_color_at_point(raster, point, point_crs):

    if not raster.crs() == point_crs:
        xform = QgsCoordinateTransform(point_crs, raster.crs())
        point = xform.transform(point)

    color_rgba = raster.dataProvider().identify(point,QgsRaster.IdentifyFormatValue).results()
    try:
        r, g, b, a = color_rgba.values()
        color = QColor.fromRgb(r, g, b, a)
    except (ValueError, TypeError):
        return None
    else:
        return color