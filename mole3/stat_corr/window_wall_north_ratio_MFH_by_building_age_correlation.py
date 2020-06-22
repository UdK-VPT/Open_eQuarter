# OeQ autogenerated correlation for 'Window/Wall Ratio North in Correlation to the Building Age'

import math
import numpy as np
from . import oeqCorrelation as oeq
def window_wall_north_ratio_MFH_by_building_age_correlation(*xin):

    # OeQ autogenerated correlation for 'Window to Wall Ratio in Northern Direction'
    A_WIN_N_BY_AW= oeq.correlation(
    const= 14743.6179719,
    a=     -30.2572633913,
    b=     0.02327306174,
    c=     -7.95175130127e-06,
    d=     1.01829432637e-09,
    mode= "lin")

    return dict(A_WIN_N_BY_AW=A_WIN_N_BY_AW.lookup(*xin))
