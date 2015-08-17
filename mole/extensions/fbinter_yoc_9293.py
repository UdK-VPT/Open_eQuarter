# -*- coding: utf-8 -*-
from mole.extensions import oeq_extension
from mole.oeq_global import *


def average(self, layer):
    print test
    print self.parname_2


fbinter_yoc_9293 = oeq_extension(
    name='Year of Construction (WMS)',
    description=u'Gebaeudealter 199293 Scan der Karte Gebaeudealter 1992 93 aus der Veroeffentlichung: Staedtebauliche Entwicklung Berlins seit 1650 in Karten',
    url='http://fbinter.stadt-berlin.de/fb/wms/senstadt/gebaeudealter',
    evaluation_method=parodie)


def evaluation(object, building_ID):
    evaluation_method = Nonetitle = 'Year of Construction (fbinter 92/93)'


print fbinter_yoc_9293.evaluate(99)
print fbinter_yoc_9293.name
