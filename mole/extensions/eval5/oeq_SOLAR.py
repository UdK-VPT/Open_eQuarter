# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={}):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    ratio_solar_available=0.5
    ratio_solar_installable=0.5
    solar_earnings_per_sqm=450.0

    dataset = {'SOLAR':NULL,'SOLIAR': NULL,'SOLHE': NULL,'SOLHEL': NULL,'SOLCRT': NULL}
    dataset.update(parameters)

    if not oeq_global.isnull([dataset['AHDP'], dataset['RF_AR'],dataset['LIV_AR']]):
        dataset['SOLAR']=float(dataset['RF_AR']) * float(ratio_solar_available)
        dataset['SOLIAR']=float(dataset['SOLAR'])*float(ratio_solar_installable)
        dataset['SOLHE']=solar_earnings_per_sqm * float(dataset['SOLIAR'])
        dataset['SOLHEL']=dataset['SOLHE']/float(dataset['LIV_AR'])
        dataset['SOLCRT']=float(dataset['SOLHEL'])/float(dataset['AHDP'])*100

    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result

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
    par_in=['AHDP','RF_AR','LIV_AR'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['SOLCRT'],
    description=u"Calculate the Solar Coverage Ratio (Present)",
    evaluation_method=calculation)

extension.registerExtension(default=True)
