# coding = utf-8

from io import open
import os
import json
import mole

class ColorEntryManager():
    """
    Model for the color picker, which keeps track of the colors which are related to a layer
    and can save/read these information to/from disk.
    """
    def __init__(self):
        self.layer_values_map = {}

    def add_layer(self, layer):
        if not self.layer_values_map.has_key(layer):
            self.layer_values_map[layer] = {}

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

            color_dict = self.layer_values_map[layer_name]
            if color_dict:

                try:
                    with open(out_path, 'w', encoding='utf-8') as json_outfile:
                        json_string = json.dumps(color_dict, ensure_ascii=False)
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


class MunicipalInformationParser():
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


class MunicipalInformationTree():
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

    def write_tree_to_disk(self, tree):
        pass