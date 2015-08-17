import os, glob, sys
from mole.oeq_global import *
from mole.model.file_manager import InformationSource


class oeq_extension:
    def __init__(self, field_id=None,
                 extension_name='Empty Extension',
                 layer_name='New OeQ Extension',
                 description='Extention Details',
                 type='wms',
                 source='http://fbinter.stadt-berlin.de/fb/wms/senstadt/gebaeudealter',
                 parname_1=None,
                 parname_2=None,
                 parnames_out=None,
                 evaluation_method=None):
        self.field_id = field_id
        self.extension_name = extension_name
        self.layer_name = layer_name
        self.description = description
        self.type = type
        self.source = source
        if parname_1 is None:
            self.parname_1 = symbol + '_L'
        else:
            self.parname_1 = parname_1
        if parname_2 is None:
            self.parname_2 = symbol + '_H'
        else:
            self.parname_2 = parname_2
        if parnames_out is None:
            self.parnames_out = symbol
        else:
            self.parnames_out = parnames_out
        self.evaluator = evaluation_method


def getInformationSource(self):
    return InformationSource(extension=self.extension_name, type=self.type, field_id=self.field_id,
                             layer_name=self.layer_name, source=self.source)


def evaluate(self, param):
    self.evaluator(self, param)


modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
