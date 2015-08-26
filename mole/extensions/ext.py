import os
import pickle
from mole import oeq_global


def average(self=None, parameters={}):
    from PyQt4.QtCore import QVariant
    print parameters
    print parameters.values()
    if parameters != {}:
        # print sum(float(parameters.values()))/len(parameters)
        return {self.field_id + '_P': {'type': QVariant.String,
                                       'value': self.layer_name},
                self.field_id + '_M': {'type': QVariant.Double,
                                       'value': sum([float(i) for i in parameters.values()]) / len(parameters)}}
    else:
        return {self.field_id + '_P': {'type': QVariant.String,
                                       'value': NULL},
                self.field_id + '_M': {'type': QVariant.Double,
                                       'value': NULL}}


class OeQExtension:
    def __init__(self, category=None,
                 field_id=None,
                 extension_id=None,
                 extension_name=None,
                 layer_name='New OeQ Extension',
                 layer_id=None,
                 description='Extention Details',
                 source_type=None,
                 active=False,
                 source=None,
                 par_in=None,
                 par_out=None,
                 colortable=None,
                 evaluation_method=None):
        self.field_id = field_id
        if extension_id is None:
            self.extension_id = 'userdefined_' + str(OeQExtension.generic_id_cnt)
            OeQExtension.generic_id_cnt += 1
        else:
            self.extension_id = extension_id
        if extension_name is None:
            extension_name = layer_name + ' (' + source_type.upper() + ')'
        self.extension_name = extension_name
        self.category = category
        self.layer_name = layer_name
        self.layer_id = layer_id
        self.description = description
        self.type = type
        self.source = source
        self.active = active
        self.source_type = source_type
        if evaluation_method is None:
            self.evaluator = average
        else:
            self.evaluator = evaluation_method
        if par_in is None:
            self.par_in = [field_id + '_L', field_id + '_H']
        else:
            self.par_in = par_in
        if par_out is None:
            self.par_out = self.get_par_out()
        else:
            self.par_out = par_out
        if colortable is None:
            colortable = os.path.join(__file__[:-3] + '.qml')
            print colortable
        if os.path.isfile(colortable):
            self.colortable = colortable
        else:
            self.colortable = None

    def update(self, category=None,
               field_id=None,
               extension_id=None,
               extension_name=None,
               layer_name='New OeQ Extension',
               layer_id=None,
               description='Extention Details',
               source_type=None,
               active=False,
               source=None,
               par_in=None,
               par_out=None,
               colortable=None,
               evaluation_method=None):
        if category != None: self.category = category
        if field_id != None: self.field_id = field_id
        if extension_id != None: self.extension_id = extension_id
        if extension_name != None: self.extension_name = extension_name
        if layer_name != None: self.layer_name = layer_name
        if layer_id != None: self.layer_id = layer_id
        if description != None: self.description = description
        if source_type != None: self.source_type = source_type
        if active != None: self.active = active
        if source != None: self.source = source
        if par_in != None: self.par_in = par_in
        if par_out != None: self.par_out = par_out
        if colortable != None: self.colortable = colortable
        if evaluation_method != None: self.evaluator = evaluation_method

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def registerExtension(self, default=False):
        from mole.oeq_global import OeQ_ExtensionRegistry, OeQ_ExtensionDefaultRegistry
        # if self.category == 'import':
        #    OeQ_ImportExtensionRegistry.append(self)
        # elif self.category == 'export':
        #      OeQ_ExportExtensionRegistry.append(self)
        # elif self.category == 'evaluation':

        if default:
            OeQ_ExtensionDefaultRegistry.append(self)
        else:
            OeQ_ExtensionRegistry.append(self)

    def evaluate(self, parameter):
        return self.evaluator(self, parameter)

    def dummy_par(self):
        return dict(zip(self.par_in, [1 for i in self.par_in]))

    def get_par_out(self):
        return self.evaluate(dict(zip(self.par_in, [1 for i in self.par_in]))).keys()

    def default_colortable(self):
        defcolortable = by_extension_id(self.extension_id, registry=oeq_global.OeQ_ExtensionDefaultRegistry)
        if defcolortable != []: return defcolortable[0].colortable
        return None

    def update_colortable(self, overwrite=False):
        from shutil import copyfile
        ct_default = self.default_colortable()
        if oeq_global.OeQ_project_path() == u'.':
            self.colortable = ct_default
        else:
            ct_project = os.path.join(oeq_global.OeQ_project_path(), self.layer_name + '.qml')
            if overwrite:
                try:
                    os.remove(ct_now)
                except:
                    pass
            if os.path.isfile(ct_project):
                self.colortable = ct_project
            else:
                self.colortable = None
                if ct_default != None:
                    if os.path.isfile(ct_default):
                        copyfile(ct_default, ct_project)
                        self.colortable = ct_project
            print ct_project
        print ct_default
        print self.colortable


def by_category(category=None, registry=None):
    if registry is None:
        registry = oeq_global.OeQ_ExtensionRegistry
    if category is None:
        return registry
    return filter(lambda ext: ext.category == category, registry)


def by_state(active=None, category=None, registry=None):
    registry = by_category(category, registry)
    if active is None:
        return registry
    return filter(lambda ext: ext.active == active, registry)


def by_name(name=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if name is None:
        return registry
    return filter(lambda ext: ext.extension_name == name, registry)


def by_layername(name=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if name is None:
        return registry
    return filter(lambda ext: ext.layer_name == name, registry)


def by_type(type=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if type is None:
        return registry
    return filter(lambda ext: ext.source_type == type, registry)


def by_field_id(field_id=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if field_id is None:
        return registry
    return filter(lambda ext: ext.field_id == field_id, registry)


def by_layerid(layer_id=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if layer_id is None:
        return registry
    return filter(lambda ext: ext.layer_id == layer_id, registry)


def by_extension_id(extension_id=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if extension_id is None:
        return registry
    return filter(lambda ext: ext.extension_id == extension_id, registry)


def save():
    print 'Save Extentsions to project'
    project_path = oeq_global.OeQ_project_path()
    project_name = oeq_global.OeQ_project_name()
    registry_file = os.path.join(project_path, project_name + '.xreg')
    print registry_file
    try:
        with open(registry_file, 'wb') as output:
            pickle.dump(oeq_global.OeQ_ExtensionRegistry, output, pickle.HIGHEST_PROTOCOL)
    except IOError, FileNotFoundError:
        print(self.__module__, FileNotFoundError)


def load_defaults():
    import copy
    oeq_global.OeQ_ExtensionRegistry = copy.deepcopy(oeq_global.OeQ_ExtensionDefaultRegistry)
    for ext in oeq_global.OeQ_ExtensionRegistry:
        ext.update_colortable(True)
    oeq_global.OeQ_ExtensionsLoaded = True

    print [i.layer_name for i in oeq_global.OeQ_ExtensionRegistry]
    print [i.layer_name for i in oeq_global.OeQ_ExtensionDefaultRegistry]
    print [i.colortable for i in oeq_global.OeQ_ExtensionRegistry]


def load():
    print 'Load Extentsions from project'
    project_path = oeq_global.OeQ_project_path()
    project_name = oeq_global.OeQ_project_name()
    registry_file = os.path.join(project_path, project_name + '.xreg')
    print registry_file
    if os.path.isfile(registry_file):
        try:
            with open(registry_file, 'rb') as input:
                oeq_global.OeQ_ExtensionRegistry = pickle.load(input)
                oeq_global.OeQ_ExtensionsLoaded = True
        except IOError, FileNotFoundError:
            print(self.__module__, FileNotFoundError)

    else:
        load_defaults()
    if oeq_global.OeQ_ExtensionRegistry == []:
        load_defaults()
    for ext in oeq_global.OeQ_ExtensionRegistry:
        ext.update_colortable()
    print [i.layer_name for i in oeq_global.OeQ_ExtensionRegistry]
    print [i.colortable for i in oeq_global.OeQ_ExtensionRegistry]


def export():
    pass
