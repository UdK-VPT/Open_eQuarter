# This is an auto-generated Django model module created by ogrinspect.
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.utils import timezone
from django.conf import settings

class Layer(models.Model):
    name = models.CharField(max_length=254)

    def features(self):
        return OeQLayer.objects.filter(layer=self)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('layer_detail', kwargs={'pk': self.pk})

class OeQLayer(models.Model):
    layer = models.ForeignKey(Layer, null=True)
    gml_id = models.CharField(max_length=254, null=True)
    spatial_na = models.CharField(max_length=254, null=True)
    spatial_al = models.CharField(max_length=254, null=True)
    spatial_ty = models.CharField(max_length=254, null=True)
    bld_id = models.CharField(max_length=254, null=True)
    area = models.FloatField(null=True)
    perimeter = models.FloatField(null=True)
    yoc = models.FloatField(null=True)
    pdens = models.FloatField(null=True)
    floors = models.FloatField(null=True)
    wn_ar = models.FloatField(null=True)
    rf_ar = models.FloatField(null=True)
    wl_com = models.FloatField(null=True)
    height = models.FloatField(null=True)
    wl_ar = models.FloatField(null=True)
    width = models.FloatField(null=True)
    length = models.FloatField(null=True)
    bs_ar = models.FloatField(null=True)
    wn_rat = models.FloatField(null=True)
    liv_ar = models.FloatField(null=True)
    hhrs = models.FloatField(null=True)
    bs_uc = models.FloatField(null=True)
    rf_uc = models.FloatField(null=True)
    wl_uc = models.FloatField(null=True)
    wn_uc = models.FloatField(null=True)
    bs_up = models.FloatField(null=True)
    rf_up = models.FloatField(null=True)
    wl_up = models.FloatField(null=True)
    wn_up = models.FloatField(null=True)
    bs_qtc = models.FloatField(null=True)
    rf_qtc = models.FloatField(null=True)
    wl_qtc = models.FloatField(null=True)
    wn_qtc = models.FloatField(null=True)
    bs_qtp = models.FloatField(null=True)
    rf_qtp = models.FloatField(null=True)
    wl_qtp = models.FloatField(null=True)
    wn_qtp = models.FloatField(null=True)
    bs_sqtc = models.FloatField(null=True)
    rf_sqtc = models.FloatField(null=True)
    wl_sqtc = models.FloatField(null=True)
    wn_sqtc = models.FloatField(null=True)
    bs_sqtp = models.FloatField(null=True)
    rf_sqtp = models.FloatField(null=True)
    wl_sqtp = models.FloatField(null=True)
    wn_sqtp = models.FloatField(null=True)
    achl = models.FloatField(null=True)
    avr = models.FloatField(null=True)
    hlac = models.FloatField(null=True)
    hlap = models.FloatField(null=True)
    htc = models.FloatField(null=True)
    htp = models.FloatField(null=True)
    ahdc = models.FloatField(null=True)
    ahdp = models.FloatField(null=True)
    solhel = models.FloatField(null=True)
    solar = models.FloatField(null=True)
    solhe = models.FloatField(null=True)
    solcrt = models.FloatField(null=True)
    soliar = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

# Auto-generated `LayerMapping` dictionary for OeQLayer model
oeq_layer_mapping = {
    'gml_id' : 'gml_id',
    'spatial_na' : 'spatial_na',
    'spatial_al' : 'spatial_al',
    'spatial_ty' : 'spatial_ty',
    'bld_id' : 'BLD_ID',
    'area' : 'AREA',
    'perimeter' : 'PERIMETER',
    'yoc' : 'YOC',
    'pdens' : 'PDENS',
    'floors' : 'FLOORS',
    'wn_ar' : 'WN_AR',
    'rf_ar' : 'RF_AR',
    'wl_com' : 'WL_COM',
    'height' : 'HEIGHT',
    'wl_ar' : 'WL_AR',
    'width' : 'WIDTH',
    'length' : 'LENGTH',
    'bs_ar' : 'BS_AR',
    'wn_rat' : 'WN_RAT',
    'liv_ar' : 'LIV_AR',
    'hhrs' : 'HHRS',
    'bs_uc' : 'BS_UC',
    'rf_uc' : 'RF_UC',
    'wl_uc' : 'WL_UC',
    'wn_uc' : 'WN_UC',
    'bs_up' : 'BS_UP',
    'rf_up' : 'RF_UP',
    'wl_up' : 'WL_UP',
    'wn_up' : 'WN_UP',
    'bs_qtc' : 'BS_QTC',
    'rf_qtc' : 'RF_QTC',
    'wl_qtc' : 'WL_QTC',
    'wn_qtc' : 'WN_QTC',
    'bs_qtp' : 'BS_QTP',
    'rf_qtp' : 'RF_QTP',
    'wl_qtp' : 'WL_QTP',
    'wn_qtp' : 'WN_QTP',
    'bs_sqtc' : 'BS_SQTC',
    'rf_sqtc' : 'RF_SQTC',
    'wl_sqtc' : 'WL_SQTC',
    'wn_sqtc' : 'WN_SQTC',
    'bs_sqtp' : 'BS_SQTP',
    'rf_sqtp' : 'RF_SQTP',
    'wl_sqtp' : 'WL_SQTP',
    'wn_sqtp' : 'WN_SQTP',
    'achl' : 'ACHL',
    'avr' : 'AVR',
    'hlac' : 'HLAC',
    'hlap' : 'HLAP',
    'htc' : 'HTC',
    'htp' : 'HTP',
    'ahdc' : 'AHDC',
    'ahdp' : 'AHDP',
    'solhel' : 'SOLHEL',
    'solar' : 'SOLAR',
    'solhe' : 'SOLHE',
    'solcrt' : 'SOLCRT',
    'soliar' : 'SOLIAR',
    'geom' : 'MULTIPOLYGON',
}


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    layer = models.ForeignKey(Layer)
    text = models.TextField(null=False, default='')
    date_created = models.DateTimeField(default=timezone.now)
