import os, glob


modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f).split('.')[0] for f in modules if not f.endswith("__init__.py")]

from .ext import *

from mole import oeq_global

oeq_global.OeQ_ExtensionsLoaded = True

# Do not remove this imports
# They are necessary to dynamically load and register the extensions
#from ext import *

#OeQExtension.generic_id_cnt = 0
try:
    from imp import *
    from exp import *
    from eval1 import *
    from eval2 import *
    from eval3 import *
    from eval4 import *
    from eval5 import *
    OeQ_ExtensionsLoaded=True
except:
    pass

