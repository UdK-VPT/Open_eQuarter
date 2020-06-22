# OeQ autogenerated correlation for 'Living Area in a Building in Correlation to the Portion of Buildings with 3 to 6 Flats'

import math
import numpy as np
from . import oeqCorrelation as oeq
def get(*xin):

    # OeQ autogenerated correlation for 'Total Living Area of all Flats of a Building'
    TOTAL_LIVING_AREA= oeq.correlation(
    const=  148.11311868,
    a=     4.83420245803,
    b=     -0.0934802870571,
    c=     0.00119008231227,
    d=     -4.54076922254e-06,
    mode= "lin")

    return dict(TOTAL_LIVING_AREA=TOTAL_LIVING_AREA.lookup(*xin))
