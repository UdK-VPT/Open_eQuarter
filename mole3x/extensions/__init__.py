import os, glob


modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f).split('.')[0] for f in modules if not f.endswith("__init__.py")]

from .ext import *

from mole3 import oeq_global

#oeq_global.OeQ_ExtensionsLoaded = True

# Do not remove this imports
# They are necessary to dynamically load and register the extensions
#from ext import *

#OeQExtension.generic_id_cnt = 0
try:
    from .acqu_berlin import *
    from .acqu_hamburg import *
    from .prop_buildings import *
    from .crea_basics import *
    from .calc_geometry import *
    from .crea_basics import *
    from .eval_contemporary import *
    from .eval_enev import *
    from .eval_enev_heritage import *
    from .eval_present import *
    from .eval_present_heritage import *

    OeQ_ExtensionsLoaded=True
except:
    pass

