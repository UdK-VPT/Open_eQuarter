import platform
import os.path
from PyQt4.QtCore import *
from qgis.core import *
from osgeo import gdal

def getGdalBinPath():
    settings = QSettings()
    base_path = os.path.join(os.sep, "GdalTools", "gdalPath")
    return settings.value(base_path, u"", type=unicode)

def setGdalBinPath( path ):
    settings = QSettings()
    base_path = os.path.join(os.sep, "GdalTools", "gdalPath")
    settings.setValue(base_path, path)
# Stores GDAL binaries location

# Retrieves GDAL python modules location
def getGdalPymodPath():
    settings = QSettings()
    base_path = os.path.join(os.sep, "GdalTools", "gdalPymodPath")
    return settings.value(base_path, u"", type=unicode)

# Stores GDAL python modules location
def setGdalPymodPath( path ):
    settings = QSettings()
    base_path = os.path.join(os.sep, "GdalTools", "gdalPymodPath")
    settings.setValue(base_path, path)

# Retrieves GDAL help files location
def getHelpPath():
    settings = QSettings()
    base_path = os.path.join(os.sep, "GdalTools", "helpPath")
    return settings.value(base_path, u"", type=unicode)

# Stores GDAL help files location
def setHelpPath( path ):
    settings = QSettings()
    base_path = os.path.join(os.sep, "GdalTools", "helpPath")
    settings.setValue(base_path, path)

def setProcessEnvironment():
    envvar_list = {
        "PATH" : getGdalBinPath(),
        "PYTHONPATH" : getGdalPymodPath(),
        "GDAL_FILENAME_IS_UTF8" : "NO"
    }

    '''
    sep = os.sep

    for name, val in envvar_list.iteritems():
        if val == None or val == "":
            continue

        envval = os.getenv(name)
        if envval == None or envval == "":
            envval = str(val)
        elif (platform.system() == "Windows" and val.lower() not in envval.lower().split( sep )) or \
                (platform.system() != "Windows" and val not in envval.split( sep )):
            envval += "%s%s" % (sep, str(val))
        else:
            envval = None

        if envval != None:
            os.putenv( name, envval )
    '''
    return envvar_list


def setMacOSXDefaultEnvironment():
    # fix bug #3170: many GDAL Tools don't work in OS X standalone

    if platform.system() != "Darwin":
        return

    # QgsApplication.prefixPath() contains the path to qgis executable (i.e. .../Qgis.app/MacOS)
    # get the path to Qgis application folder
    qgis_app = u"%s/.." % QgsApplication.prefixPath()
    qgis_app = QDir( qgis_app ).absolutePath()

    qgis_bin = u"%s/bin" % QgsApplication.prefixPath()   # path to QGis bin folder
    qgis_python = u"%s/Resources/python" % qgis_app    # path to QGis python folder

    # path to the GDAL framework within the Qgis application folder (QGis standalone only)
    qgis_standalone_gdal_path = u"%s/Frameworks/GDAL.framework" % qgis_app

    # path to the GDAL framework when installed as external framework
    gdal_versionsplit = str(gdal.VersionInfo("RELEASE_NAME")).split('.')
    gdal_base_path = u"/Library/Frameworks/GDAL.framework/Versions/%s.%s" % (gdal_versionsplit[0], gdal_versionsplit[1])

    if os.path.exists( qgis_standalone_gdal_path ):  # qgis standalone
        # GDAL executables are in the QGis bin folder
        if getGdalBinPath() == '':
            setGdalBinPath( qgis_bin )
        # GDAL pymods are in the QGis python folder
        if getGdalPymodPath() == '':
            setGdalPymodPath( qgis_python )
        # GDAL help is in the framework folder
        if getHelpPath() == '':
            setHelpPath( u"%s/Resources/doc" % qgis_standalone_gdal_path )

    elif os.path.exists( gdal_base_path ):
        # all GDAL parts are in the GDAL framework folder
        if getGdalBinPath() == '':
            setGdalBinPath( u"%s/Programs" % gdal_base_path )
        if getGdalPymodPath() == '':
            setGdalPymodPath( u"%s/Python/%s.%s/site-packages" % (gdal_base_path, sys.version_info[0], sys.version_info[1]) )
        if getHelpPath() == '':
            setHelpPath( u"%s/Resources/doc" % gdal_base_path )