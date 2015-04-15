from platform import system


def qgis_prefix_path():
    if system() == 'Windows':
        return 'D:/OSGEO4~1/apps/qgis'
    else:
        return '/Applications/QGIS.app/Contents/MacOS'