# coding = utf-8
import os
import json
import mole
import qgis.utils


import xml.etree.ElementTree as etree
from io import open
from collections import OrderedDict

class ColorEntryManager:
    """
    Model for the color picker, which keeps track of the colors which are related to a layer
    and can save/read these information to/from disk.
    """
    def __init__(self):
        self.layer_values_map = {}
        self.layer_abbreviation_map = {}

    def add_layer(self, layer_name):
        if not self.layer_values_map.has_key(layer_name):
            self.layer_values_map[layer_name] = OrderedDict()

    def set_layer_abbreviation(self, layer_name, abbreviation):
        self.layer_abbreviation_map[layer_name] = abbreviation

    def set_color_map_of_layer(self, color_map, layer_name):
        self.layer_values_map[layer_name] = dict(color_map)

    def add_color_value_quadruple_to_layer(self, cv_quadruple, layer):
        color_key = cv_quadruple[0]
        value_triple = cv_quadruple[1:]
        try:
            layer_colors = self.layer_values_map[layer]
            layer_colors[color_key] = value_triple
        except KeyError, Error:
            print('{}: {}'.format(self.__module__, Error))

    def write_map_to_disk(self, layer_name, out_path):
        if self.layer_values_map.has_key(layer_name):

            out_dict = self.layer_values_map[layer_name]
            if out_dict:
                if self.layer_abbreviation_map.has_key(layer_name):
                    out_dict = {'Abbreviation': self.layer_abbreviation_map[layer_name], 'Legend': out_dict}

                try:
                    with open(out_path, 'w', encoding='utf-8') as json_outfile:
                        json_string = json.dumps(out_dict, ensure_ascii=False)
                        json_outfile.write(unicode(json_string))

                    return os.path.exists(out_path)
                except IOError, Error:
                    return False
                    print('{}: {}'.format(self.__module__, Error))

    def read_color_map_from_disk(self, in_path):
        file_name = os.path.basename(in_path)
        layer_name = os.path.splitext(file_name)[0]
        self.layer_values_map[layer_name] = {}

        result_dict = {}
        try:
            json_data = open(in_path)
            data = json.load(json_data)

            if data.has_key('Abbreviation'):
                self.layer_abbreviation_map[layer_name] = data['Abbreviation']
                data = data['Legend']

            for color, value_list in data.iteritems():
                result_dict[color] = (value_list[0], value_list[1], value_list[2])

            json_data.close()
        except IOError, Error:
            print('{}: {}'.format(self.__module__, Error))

        self.set_color_map_of_layer(result_dict, layer_name)

    def remove_color_entry_from_layer(self, color_entry, layer):
        entries = self.layer_values_map[layer]
        del entries[color_entry]
        self.set_color_map_of_layer(entries, layer)


    def write_color_map_as_qml(self, layer_name, out_path):

        def qml_header():
            return('<!DOCTYPE qgis PUBLIC \'http://mrcc.com/qgis.dtd\' \'SYSTEM\'>\n'
                    '<qgis version="' + qgis.utils.QGis.QGIS_VERSION + '">\n'
                    '   <edittypes></edittypes>\n'
                    '   <renderer-v2 symbollevels="0" type="graduatedSymbol">\n'
                    '       <ranges>\n')
        def qml_range(id,lower,upper,label=None):
            if label == None: label= str(round(float(lower),1)) + ' - ' + str(round(float(upper),1))
            return '            <range render="true" symbol="'+ str(id) + '" lower="' + str(lower) + '" upper="' + str(upper) + '" label="' + label + '"/>\n'

        def qml_inter1():
            return('        </ranges>\n'
                   '        <symbols>\n')

        def qml_symbol(id,R,G,B,alpha):
            return('            <symbol alpha="1" type="fill" name="' + str(id) + '">\n'
                    '               <layer pass="0" class="SimpleFill" locked="0">\n'
                    '                   <prop k="border_width_map_unit_scale" v="0,0"/>\n'
                    '                   <prop k="color" v="'+ str(R) + ',' + str(G) + ',' + str(B) + ',' + str(alpha) + '"/>\n'
                    '                   <prop k="joinstyle" v="bevel"/>\n'
                    '                   <prop k="offset" v="0,0"/>\n'
                    '                   <prop k="offset_map_unit_scale" v="0,0"/>\n'
                    '                   <prop k="offset_unit" v="MM"/>\n'
                    '                   <prop k="outline_color" v="0,0,0,255"/>\n'
                    '                   <prop k="outline_style" v="solid"/>\n'
                    '                   <prop k="outline_width" v="0.66"/>\n'
                    '                   <prop k="outline_width_unit" v="MM"/>\n'
                    '                   <prop k="style" v="solid"/>\n'
                    '               </layer>\n'
                    '           </symbol>\n')

        def qml_inter2():
            return('        </symbols>\n'
                    '   </renderer-v2>\n'
                    '   <customproperties>\n')

        def qml_property(key,value):
            return('        <property key="'+ str(key) + '" value="' + str(value) + '"/>\n')

        def qml_footer():
            return('    </customproperties>\n'
                    '   <blendMode>0</blendMode>\n'
                    '   <featureBlendMode>0</featureBlendMode>\n'
                    '   <layerTransparency>0</layerTransparency>\n'
                    '   <displayfield>gml_id</displayfield>\n'
                    '   <label>0</label>\n'
                    '   <labelattributes></labelattributes>\n'
                    '   <editform>.</editform>\n'
                    '   <editforminit></editforminit>\n'
                    '   <featformsuppress>0</featformsuppress>\n'
                    '   <annotationform>.</annotationform>\n'
                    '   <editorlayout>generatedlayout</editorlayout>\n'
                    '   <excludeAttributesWMS/>\n'
                    '   <excludeAttributesWFS/>\n'
                    '   <attributeactions/>\n'
                    '</qgis>')


        if self.layer_values_map.has_key(layer_name):
            out_dict = self.layer_values_map[layer_name]
            if out_dict:
                qml=qml_header()
                cnt=0
                out_ranges=""
                out_symbols=""
                out_properties=""
                for entry in out_dict.keys():
                    rgba=entry.replace(" ","").replace("RGBa(","").replace(")","").split(",")
                    #["Id"]=entry[1]
                    #["lowLim"]=entry[2]
                    #["highLim"]=entry[3]
                    out_ranges=out_ranges + qml_range(cnt,out_dict[entry][1],out_dict[entry][2],None)
                    print rgba
                    out_symbols = out_symbols  + qml_symbol(cnt,rgba[0],rgba[1],rgba[2],rgba[3])
                    out_properties=out_properties + qml_property("ParName"+ str(cnt), out_dict[entry][0])
                    cnt+=1
                if self.layer_abbreviation_map.has_key(layer_name):
                    out_properties=out_properties + qml_property("LayAbr", self.layer_abbreviation_map[layer_name])

                qml_out= qml_header() + out_ranges + qml_inter1() + out_symbols + qml_inter2() + out_properties + qml_footer()

                try:
                    with open(out_path, 'w', encoding='utf-8') as qml_file:
                        qml_file.write(unicode(qml_out))

                    return os.path.exists(out_path)
                except IOError, Error:
                    return False
                    print('{}: {}'.format(self.__module__, Error))

    def read_color_map_from_qml(self, in_path):
        file_name = os.path.basename(in_path)
        layer_name = os.path.splitext(file_name)[0]
        self.layer_values_map[layer_name] = {}

        result_dict = {}

        def get_colors(tree):
            out_col={}
            symbols=tree.find('renderer-v2/symbols')
            for i in symbols:
                layer=i.find('layer')
                for j in layer:
                    if j.attrib['k']=='color':
                        out_col[i.attrib['name']] = 'RGBa( ' + j.attrib['v'].replace(',',' , ') + ')'
            return out_col

        def get_ranges(tree):
            out_rng={}
            ranges=tree.find('renderer-v2/ranges')
            for i in ranges:
                out_rng[i.attrib['symbol']]= [i.attrib['lower'],i.attrib['upper']]
            return out_rng

        def get_parNames(tree):
            out_par={}
            props=tree.find('customproperties')
            for i in props:
                if i.attrib['key'].startswith('ParName'):
                    name=i.attrib['key']
                    name=name.replace("ParName","")
                    print name
                    print i.attrib['value']
                    print i.attrib

                    out_par[name]= i.attrib['value']
            return out_par

        def get_abrev(tree):
            out_par={}
            props=tree.find('customproperties')
            for i in props:
                if i.attrib['key'].startswith('LayAbr'):
                    out_par['LayAbr'] = i.attrib['value']
            return out_par

        try:
            qml_tree=etree.parse(in_path)
            qml_col=get_colors(qml_tree)
            qml_par=get_parNames(qml_tree)
            qml_rng=get_ranges(qml_tree)
            qml_abr=get_abrev(qml_tree)
            ID_range=[]
            for i in qml_col.keys():
                result_dict[qml_col[i]]= [qml_par[i],qml_rng[i][0],qml_rng[i][1]]


            if len(qml_abr)>0:
                self.layer_abbreviation_map[layer_name] = qml_abr[0]

        except IOError, Error:
           print('{}: {}'.format(self.__module__, Error))

        self.set_color_map_of_layer(result_dict, layer_name)



class MunicipalInformationParser:
    """
    A parser-class to scan a .json file for all municipals with a given postcode.
    """
    def __init__(self):
        self.municipal = []

        mole_path = mole.__file__
        mole_path = os.path.dirname(mole_path)
        municipal_json_path = os.path.join(mole_path, 'project', 'municipal_db.json')
        self.municipal_json_file = municipal_json_path

    def parse_municipal(self, postcode):
        self.municipal = []
        try:
            with open(self.municipal_json_file, encoding='utf-8') as file:
                for line in file:
                    entry = json.loads(line, encoding='utf-8')

                    try:
                        municipal_entry = {}
                        if entry['POSTCODE'] == postcode:
                            for key, value in entry.iteritems():
                                municipal_entry[key.encode('utf-8')] = value

                            municipal_entry['NAME'] = municipal_entry['NAME'].encode('utf-8')
                            self.municipal.append(municipal_entry)
                    except KeyError, Error:
                        print('{} \n Resulted in KeyError: {}'.format(entry, Error))

        except IOError, Error:
            print('{}: {}'.format(self.__module__, Error))


class MunicipalInformationTree:
    """
    A model which stores all municipal information ordered by postal-code in a tree-like array-structure.
    """
    def __init__(self):
        self.tree = {}
        mole_path = mole.__file__
        mole_path = os.path.dirname(mole_path)
        municipal_json_path = os.path.join(mole_path, 'project', 'municipal_db.json')
        self.municipal_json_file = municipal_json_path

    def find_keys_on_level(self, level):
        keys = {}
        if level >= 0 and level < 10:
            try:
                with open(self.municipal_json_file, encoding='utf-8') as file:
                    for line in file:
                        entry = json.loads(line, encoding='utf-8')

                        try:
                            postcode = str(entry['POSTCODE'])
                            key = postcode[level]
                            keys[key] = {}
                        except KeyError, Error:
                            print('{} \n Resulted in KeyError: {}'.format(entry, Error))

            except IOError, Error:
                print('{}: {}'.format(self.__module__, Error))
        return keys

    def split_data_to_tree_model(self):
        try:
            with open(self.municipal_json_file, encoding='utf-8') as file:
                for line in file:
                    entry = json.loads(line, encoding='utf-8')

                    try:
                        postcode = str(entry['POSTCODE'])
                        l0_key = postcode[0]
                        l1_key = postcode[1]
                        l2_key = postcode[2:]
                        self.tree[l0_key][l1_key][l2_key].append(entry)

                    except KeyError, Error:
                        if not postcode:
                            print('{} \n Resulted in KeyError: {}'.format(entry, Error))

                        else:
                            if not self.tree.has_key(l0_key):
                                self.tree[l0_key] = {}

                            if not self.tree[l0_key].has_key(l1_key):
                                self.tree[l0_key][l1_key] = {}

                            if not self.tree[l0_key][l1_key].has_key(l2_key):
                                self.tree[l0_key][l1_key][l2_key] = []

                            self.tree[l0_key][l1_key][l2_key].append(entry)

        except IOError, Error:
            print('{}: {}'.format(self.__module__, Error))