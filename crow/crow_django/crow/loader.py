import os, sys
from django.contrib.gis.utils import LayerMapping
from crow.models import OeQLayer, oeq_layer_mapping


def run(shp_location='../../../OeQ_Unters/Heinrich_db.shp', verbose=True):

    try:
        shp = os.path.abspath(os.path.join(os.path.dirname(__file__), shp_location))
        lm = LayerMapping(OeQLayer, shp, oeq_layer_mapping, transform=False, encoding='iso-8859-1')
        lm.save(strict=True, verbose=verbose)
    except IndexError as MissingArgErr:
        print('Please provide the relative location of the shapefile as first argument.')

