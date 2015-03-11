from io import open
import json

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