from qgis.core import QgsRasterLayer, QgsApplication, QgsRaster, QgsCoordinateTransform
from PyQt4.QtGui import QColor
from platform import system
from os import path
import subprocess
import time
import GdalUtils


def gdal_warp_layer(layer, target_crs):

    try:
        source_crs = layer.crs().toProj4()
        input_path = layer.publicSource()
        input_path = path.normpath(input_path)
        out_path = path.dirname(input_path)
        out_path = path.normpath(out_path)
        out_path = path.join(out_path, layer.name() + '_transformed.tif')

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

        # wait until the file exists to add geo-references
        while not path.exists(input_path):
            time.sleep(0.1)

        cmd = ['gdalwarp', '-s_srs', str(source_crs),'-t_srs', str(target_crs), input_path, out_path]

        gdalwarp = subprocess.Popen(cmd, env=environment)

        #ToDo Add timeout function
        return gdalwarp.wait()
    except AttributeError as Att_Error:
        print(Att_Error.message)


def extract_color_at_point(raster, point, point_crs):

    if not raster.crs() == point_crs:
        xform = QgsCoordinateTransform(point_crs, raster.crs())
        point = xform.transform(point)

    color_rgba = raster.dataProvider().identify(point,QgsRaster.IdentifyFormatValue).results()
    try:
        r, g, b, a = color_rgba.values()
        color = QColor.fromRgb(r, g, b, a)
    except ValueError:
        return None
    else:
        return color