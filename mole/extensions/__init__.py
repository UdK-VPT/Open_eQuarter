import glob
from mole.oeq_global import *


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
            self.parname_1 = field_id + '_L'
        else:
            self.parname_1 = parname_1
        if parname_2 is None:
            self.parname_2 = field_id + '_H'
        else:
            self.parname_2 = parname_2
        if parnames_out is None:
            self.parnames_out = field_id
        else:
            self.parnames_out = parnames_out
        self.evaluator = evaluation_method

    def getInformationSource(self):
        return InformationSource(extension=self.extension_name,
                                 type=self.type,
                                 field_id=self.field_id,
                                 layer_name=self.layer_name,
                                 source=self.source)

    def registerExtension(self):
        print "register extension"
        OeQ_ImportExtensionRegistry.append(self)

    def registerDialog(self):
        print "register dialog"
        OeQ_information_defaults.append(self.getInformationSource())

    def evaluate(self):
        self.evaluator(self)


modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
from . import *

