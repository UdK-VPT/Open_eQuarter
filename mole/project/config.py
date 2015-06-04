import os

from platform import system
from qgis.core import QgsRectangle

import mole

# Project information
project_crs = 'EPSG:3857'

### Information needed to use external plugins
# OpenStreetMap plugin
ol_plugin_name = 'openlayers_plugin'
open_layer_type_id = 4
# id=0 - Google Physical
# id=1 - Google Streets
# id=4 - OpenStreetMap

# Point Sampling Tool
pst_plugin_name = 'pointsamplingtool'
pst_output_layer_name = 'pst_out'
pst_input_layer_name = 'Building centroids'

# Realcentroid plugin
real_centroid_plugin_name = 'realcentroid'

### Default values
# default extent is set, after the OSM-layer was loaded (currently: extent of Germany)
x = 10.447683
y = 51.163375
scale = 4
default_extent = QgsRectangle(x - scale, y - scale, x + scale, y + scale)
default_extent_crs = 'EPSG:4326'

# name of the shapefile which will be created to define the investigation area
investigation_shape_layer_name = 'Investigation Area'
housing_layer_name = 'Floor plan'
housing_coordinate_layer_name = 'Building centroids'
# name of the wms-raster which will be loaded and is the basis for the clipping
clipping_raster_layer_name = 'Investigation Area - raster'
color_match_tolerance = 30


### Default paths
plugin_dir = os.path.dirname(mole.__file__)
progress_model = os.path.join(plugin_dir, 'project', 'default_progress.oeq')
investigation_area_style = os.path.join(plugin_dir, 'project', 'oeq_ia_style.qml')
valid_centroids_style = os.path.join(plugin_dir, 'project', 'oeq_valid_centroid_style.qml')

def qgis_prefix_path():
    if system() == 'Windows':
        return 'D:/OSGEO4~1/apps/qgis'
    else:
        return '/Applications/QGIS.app/Contents/MacOS'