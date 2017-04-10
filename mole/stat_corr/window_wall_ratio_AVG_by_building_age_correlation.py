# OeQ autogenerated correlation for 'Window/Wall Ratio in Correlation to the Building Age'

import math
import numpy as np
from . import oeqCorrelation as oeq
def get(*xin):

    # OeQ autogenerated correlation for 'Window to Wall Ratio in all Directions'
    A_WIN_BY_AW= oeq.correlation(
    const= -5481.11187181,
    a=     11.1935821089,
    b=     -0.00857180719327,
    c=     2.917470346e-06,
    d=     -3.72396722858e-10,
    mode= "lin")

    return dict(A_WIN_BY_AW=A_WIN_BY_AW.lookup(*xin))

