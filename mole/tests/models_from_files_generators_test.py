import unittest
import sys, io, json, os

from mole.model.file_manager import ColorEntryManager


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.cem = ColorEntryManager()

    def test_dict_can_be_added_to_layer_in_color_entry_manager(self):

        test_layer = 'my_test_layer'
        test_dict = { 'RGBa(0, 0, 255, 255)' : (70, 20), 'RGBa(0, 0, 220, 255)' : (70, 20) }
        self.cem.set_color_map_of_layer(test_dict, test_layer)
        self.assertDictContainsSubset({test_layer: test_dict}, self.cem.layer_values_map)

    def test_layer_can_be_passed_to_color_entry_manager(self):

        test_layer = 'my_test_layer.tif'
        self.cem.add_layer(test_layer)

        self.assertDictContainsSubset({test_layer: {}}, self.cem.layer_values_map)

    def test_layer_map_does_not_get_overwritten_in_cem(self):

        test_layer = 'my_test_layer'
        test_dict = { 'RGBa(0, 0, 255, 255)' : (70, 20), 'RGBa(0, 0, 220, 255)' : (70, 20) }
        self.cem.set_color_map_of_layer(test_dict, test_layer)
        self.cem.add_layer(test_layer)
        self.assertDictContainsSubset({test_layer: test_dict}, self.cem.layer_values_map)

        test_dict['RGBa(0, 20, 255, 255)'] = (47,11)
        self.assertNotEqual(self.cem.layer_values_map[test_layer], test_dict)

    def test_color_value_triple_can_be_added_to_layer_in_cem(self):
        test_layer = 'my_test_layer'
        test_dict = { 'RGBa(0, 0, 255, 255)' : (70, 20), 'RGBa(0, 0, 220, 255)' : (70, 20) }
        self.cem.set_color_map_of_layer(test_dict, test_layer)
        color_value_triple = ('RGBa(0, 20, 255, 255)', 47, 11)

        self.cem.add_color_value_triple_to_layer(color_value_triple, test_layer)
        test_dict[color_value_triple[0]] = color_value_triple[1:]
        self.assertDictContainsSubset({test_layer: test_dict}, self.cem.layer_values_map)

    def test_cem_writes_map_to_correct_path(self):
        path = sys.path[0]
        cem = ColorEntryManager()
        layer_name = 'my_test_layer'
        cem.add_layer(layer_name)
        cem.add_color_value_triple_to_layer(('Color', 0, 1), layer_name)
        out_path = os.path.join(path, layer_name + '.txt')
        cem.write_map_to_disk(layer_name, out_path)

        self.assertTrue(os.path.exists(out_path))
        try:
            os.remove(out_path)
        except IOError, Error:
            print(Error)

    def test_cem_writes_map_only_if_layer_and_map_exist(self):
        path = sys.path[0]
        cem = ColorEntryManager()
        layer_name = 'my_test_layer'
        out_path = os.path.join(path, layer_name + '.txt')
        cem.write_map_to_disk(layer_name, out_path)
        self.assertFalse(os.path.exists(out_path))

        cem.add_layer(layer_name)
        cem.write_map_to_disk(layer_name, out_path)
        self.assertFalse(os.path.exists(out_path))

    def test_json_file_for_correctness(self):
        path = sys.path[0]
        cem = ColorEntryManager()
        layer_name = 'my_test_layer'
        out_path = os.path.join(path, layer_name + '.txt')
        cem.add_layer(layer_name)
        dict = {'RGBa(0, 0, 255, 255)': (120, 11)}
        dict['RGBa(0, 0, 255, 255)'] = (131,28)
        dict['RGBa(123, 21, 255, 255)'] = (2,8)
        dict['RGBa(2, 33, 25, 2)'] = (1,4)
        dict['RGBa(170, 12, 17, 36)'] = (12,238)
        cem.set_color_map_of_layer(dict, layer_name)
        cem.write_map_to_disk(layer_name, out_path)
        self.assertTrue(os.path.exists(out_path))

        try:
            json_data = io.open(out_path)
            data = json.load(json_data)
            result_dict = {}

            for color, value_list in data.iteritems():
                result_dict[color] = tuple(value_list)

            self.assertDictContainsSubset(dict, result_dict)
            json_data.close()
            print(data)

        except IOError, Error:
            self.fail(Error)

        finally:
            try:
                os.remove(out_path)
            except IOError, Error:
                print(Error)

if __name__ == '__main__':
    unittest.main()
