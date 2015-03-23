# coding = utf-8

from io import open
import os
import json
import mole

class ColorEntryManager():

    def __init__(self):
        self.layer_values_map = {}

    def add_layer(self, layer):
        if not self.layer_values_map.has_key(layer):
            self.layer_values_map[layer] = {}

    def set_color_map_of_layer(self, color_map, layer_name):
        self.layer_values_map[layer_name] = dict(color_map)

    def add_color_value_triple_to_layer(self, cv_triple, layer):
        color_key = cv_triple[0]
        value_tuple = cv_triple[1:]
        try:
            layer_colors = self.layer_values_map[layer]
            layer_colors[color_key] = value_tuple
        except KeyError, Error:
            print(Error)

    def write_map_to_disk(self, layer_name, out_path):
        if self.layer_values_map.has_key(layer_name):

            color_dict = self.layer_values_map[layer_name]
            if color_dict:

                try:
                    with open(out_path, 'w', encoding='utf-8') as json_outfile:
                        json_string = json.dumps(color_dict, ensure_ascii=False)
                        json_outfile.write(unicode(json_string))
                except IOError, Error:
                    print(Error)


class MunicipalInformationParser():

    def __init__(self):
        self.municipal = []

        mole_path = mole.__file__
        mole_path = os.path.dirname(mole_path)
        municipal_json_path = os.path.join(mole_path, 'project_data', 'municipal_db.json')
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
            print(Error)

class MunicipalInformationTree():

    def __init__(self):
        self.tree = {}
        mole_path = mole.__file__
        mole_path = os.path.dirname(mole_path)
        municipal_json_path = os.path.join(mole_path, 'project_data', 'municipal_db.json')
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
                print(Error)
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
            print(Error)

    def write_tree_to_disk(self, tree):
        pass