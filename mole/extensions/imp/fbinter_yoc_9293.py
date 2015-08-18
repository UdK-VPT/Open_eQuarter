# -*- coding: utf-8 -*-
from mole.extensions import oeq_extension


def average(self):
    print 'test'
    print self.parname_2


extension = oeq_extension(
    field_id='YOC',
    extension_name='Year of Construction (WMS)',
    layer_name='Year of Construction (WMS)',
    description=u'Gebaeudealter 199293 Scan der Karte Gebaeudealter 1992 93 '
                + u'aus der Veroeffentlichung: Staedtebauliche Entwicklung Berlins seit 1650 in Karten',
    source='http://fbinter.stadt-berlin.de/fb/wms/senstadt/gebaeudealter',
    evaluation_method=average)

extension.registerExtension()
extension.registerDialog()
