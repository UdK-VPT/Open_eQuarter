# OeQ autogenerated correlation for 'Number of Flats per Building in Correlation to population density '

import math
import numpy as np
from . import oeqCorrelation as oeq
def get(*xin):

    # OeQ autogenerated correlation for 'Average Number of Flats per Building'
    BLD_NOFLAT_AVG= oeq.correlation(
    const= 0.496063962509,
    a=     0.832051782819,
    b=     -0.245727278912,
    c=     0.023673087556,
    mode= "log")

    return dict(BLD_NOFLAT_AVG=BLD_NOFLAT_AVG.lookup(*xin))

