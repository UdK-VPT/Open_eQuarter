import os, sys
from django.contrib.gis.utils import LayerMapping
from crow.models import Layer, OeQLayer, oeq_layer_mapping


def run(shp_location='../../layers/Heinrich_db.shp', verbose=True):

    try:
        shp = os.path.abspath(os.path.join(os.path.dirname(__file__), shp_location))
        layer = Layer()
        layer.name = 'Heinrich'
        layer.save()
        lm = LayerMapping(OeQLayer, shp, oeq_layer_mapping, transform=False, encoding='iso-8859-1')
        lm.save(strict=True, verbose=verbose)

        for feature in OeQLayer.objects.all():
            feature.layer_id = layer.id
            feature.save()

    except IndexError as MissingArgErr:
        print('Please provide the relative location of the shapefile as first argument.')

