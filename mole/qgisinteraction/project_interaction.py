from qgis.core import QgsProject


def project_exists():
    """
    Check if a QgsProject-instance was created
    :return project_exists: If the Project was saved
    :rtype: bool
    """
    project_path = QgsProject.instance().readPath('./')

    # if the path is './', the project has not yet been saved
    project_exists = not project_path == './'
    return project_exists


def is_new_project():
    if (len(QgsProject.QgsMapLayerRegistry.instance().mapLayers()) is 0) and (
        QgsProject.QgsProject.instance().fileName() is u''):
        return True
    else:
        return False
