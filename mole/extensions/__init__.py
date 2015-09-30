import os, glob


modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
from . import *

from mole import oeq_global

oeq_global.OeQ_ExtensionsLoaded = True

# Do not remove this imports
# They are necessary to dynamically load and register the extensions
from .ext import *

OeQExtension.generic_id_cnt = 0
import imp
import exp
import eval1
import eval2
import eval3
import eval4
# OeQ_ExtensionsLoaded=True
