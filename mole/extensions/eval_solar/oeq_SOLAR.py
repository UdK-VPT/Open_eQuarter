# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    ratio_solar_installable=0.6
    solar_earnings_per_sqm=350.0

    soliar = NULL
    solhe = NULL
    solhel = NULL
    solcrt = NULL

    if not oeq_global.isnull([parameters['AHDP'], parameters['FR_AR'],parameters['LIV_AR']]):
        soliar=float(parameters['FR_AR'])*float(ratio_solar_installable)
        solhe=solar_earnings_per_sqm * float(soliar)
        solhel=solhe/float(parameters['LIV_AR'])
        solcrt=float(solhel)/float(parameters['AHDP'])*100

    return {'SOLIAR': {'type': QVariant.Double,
                           'value': soliar},
                       'SOLHE': {'type': QVariant.Double,
                            'value': solhe},
                       'SOLHEL': {'type': QVariant.Double,
                             'value': solhel},
                       'SOLCRT': {'type': QVariant.Double,
                              'value': solcrt}}

extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='Solarthermics',
    extension_name='Solar Coverage Ratio (P)',
    layer_name= 'Solar Coverage Ratio (Present)',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='SOLCRT',
    source_type='none',
    par_in=['AHDP','FR_AR','LIV_AR'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['SOLCRT'],
    description=u"Calculate the Solar Coverage Ratio (Present)",
    evaluation_method=calculation)

extension.registerExtension(default=True)
