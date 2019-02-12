from qgis.core import QgsRasterLayer, QgsApplication, QgsRaster, QgsCoordinateTransform, QgsCoordinateReferenceSystem
from qgis.PyQt.QtGui import QColor
from platform import system
from os import path
import subprocess
import time
from . import GdalUtils


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
        print((Att_Error.message))


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
        r, g, b, a = list(color_rgba.values())
        color = QColor.fromRgb(r, g, b, a)
    except (ValueError, TypeError):
        return None
    else:
        return color

'''
def shift_rastermap(layer,from_point,to_point):
    from osgeo import gdal

# Open in read/write mode
rast_src = gdal.Open(rast_fname, 1)

# Get affine transform coefficients
gt = rast_src.GetGeoTransform()
# (2776450.0, 100.0, 0.0, 6352650.0, 0.0, -100.0)

# Convert tuple to list, so we can modify it
gtl = list(gt)
gtl[0] -= 1000.0  # Move east 1 km
gtl[3] += 20000.0  # Move south 20 km
# [2777450.0, 100.0, 0.0, 6332650.0, 0.0, -100.0]

# Save the geotransform to the raster
rast_src.SetGeoTransform(tuple(gtl))
rast_src = None  # equivalent to save/close

class PointTool(QgsMapTool):
    from qgis.gui import QgsMapTool,QgsMapToolEmitPoint
    from qgis.core import QgsFeature,QgsMapLayer,QgsPoint
    from qgis.PyQt.QtGui import QMessageBox
    from qgis.PyQt.QtCore import SIGNAL,QObject
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.iface = iface
        self.points = []
        self.pointcnt = 0
    def canvasPressEvent(self, event):
        pass
    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    def canvasReleaseEvent(self, event):
        #Get the click
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    def activate(self):
        pass
    def deactivate(self):
        pass
    def isZoomTool(self):
        return False
    def isTransient(self):
        return False
    def isEditTool(self):
        return True
    def pickCoordinates(self,number_of_points = 1):
        self.points = []
        self.pointcnt = number_of_points
        self.pointEmitter = QgsMapToolEmitPoint(iface.mapCanvas())
        QObject.connect( self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.selectNow)
        iface.mapCanvas().setMapTool( self.pointEmitter )
    def selectNow(self, point, button):
      #QMessageBox.information(None, "Clicked coords", " x: " + str(point.x()) + " Y: " + str(point.y()) )
      #point1 = self.canvas.getCoordinateTransform().toMapCoordinates(point.x(), point.y())
      self.points.append(point)
      self.pointcnt -= 1
      if not self.pointcnt:
          super(PointTool, self).deactivate()
          self.emit(SIGNAL("deactivated()"))
          QObject.disconnect(self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.selectNow)
tool = PointTool(iface.mapCanvas())
tool.pickCoordinates(2)

from qgis.gui import QgsMapTool, QgsMapToolEmitPoint, QgsRubberBand
from qgis.core import QgsFeature, QgsMapLayer, QgsPoint
from qgis.PyQt.QtGui import QColor
class RectangleMapTool(QgsMapToolEmitPoint):
    from qgis.gui import QgsMapTool, QgsMapToolEmitPoint,QgsRubberBand
    from qgis.core import QgsFeature, QgsMapLayer, QgsPoint
    from qgis.PyQt.QtGui import QColor
    def __init__(self, canvas):
          self.canvas = canvas
          QgsMapToolEmitPoint.__init__(self, self.canvas)
          self.rubberBand = QgsRubberBand(self.canvas, QGis.Line)
          self.rubberBand.setColor(QColor('green'))
          self.rubberBand.setWidth(3)
          self.reset()
    def reset(self):
          self.startPoint = self.endPoint = None
          self.isEmittingPoint = False
          self.rubberBand.reset(QGis.Polygon)
    def canvasPressEvent(self, e):
          self.startPoint = self.toMapCoordinates(e.pos())
          self.endPoint = self.startPoint
          self.isEmittingPoint = True
          self.showRect(self.startPoint, self.endPoint)
    def canvasReleaseEvent(self, e):
          self.isEmittingPoint = False
          r = self.rectangle()
          if r is not None:
                print "Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum()
    def canvasMoveEvent(self, e):
          if not self.isEmittingPoint:
                return
          self.endPoint = self.toMapCoordinates(e.pos())
          self.showRect(self.startPoint, self.endPoint)
    def showRect(self, startPoint, endPoint):
          self.rubberBand.reset(QGis.Polygon)
          if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
                return
          point1 = QgsPoint(startPoint.x(), startPoint.y())
          point2 = QgsPoint(startPoint.x(), endPoint.y())
          point3 = QgsPoint(endPoint.x(), endPoint.y())
          point4 = QgsPoint(endPoint.x(), startPoint.y())
          self.rubberBand.addPoint(point1, False)
          self.rubberBand.addPoint(point2, False)
          self.rubberBand.addPoint(point3, False)
          self.rubberBand.addPoint(point4, True)    # true to update canvas
          self.rubberBand.show()
    def rectangle(self):
          if self.startPoint is None or self.endPoint is None:
                return None
          elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
                return None
          return QgsRectangle(self.startPoint, self.endPoint)
    def deactivate(self):
          super(RectangleMapTool, self).deactivate()
          self.emit(SIGNAL("deactivated()"))
tool = RectangleMapTool(iface.mapCanvas())
'''
