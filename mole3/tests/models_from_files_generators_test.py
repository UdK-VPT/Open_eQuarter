# coding=utf-8
import unittest
import sys
import io
import json
import os

from mole.model.file_manager import ColorEntryManager, MunicipalInformationParser, MunicipalInformationTree


class ColorEntryManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.cem = ColorEntryManager()
        self.test_dict = { 'RGBa(0, 0, 255, 255)' : ('Fieldname1', 70, 20), 'RGBa(0, 0, 220, 255)' : ('Fieldname1', 70, 20) }
        self.test_layer = 'my_test_layer'

    def tearDown(self):
        path = sys.path[0]
        out_path = os.path.join(path, self.test_layer + '.txt')
        try:
            os.remove(out_path)
        except OSError:
            pass

    def test_dict_can_be_added_to_layer_in_color_entry_manager(self):
        self.cem.set_color_map_of_layer(self.test_dict, self.test_layer)
        self.assertDictContainsSubset({self.test_layer: self.test_dict}, self.cem.layer_values_map)

    def test_layer_can_be_passed_to_color_entry_manager(self):
        test_layer = 'my_test_layer.tif'
        self.cem.add_layer(test_layer)

        self.assertDictContainsSubset({test_layer: {}}, self.cem.layer_values_map)

    def test_layer_map_does_not_get_overwritten_in_cem(self):
        self.cem.set_color_map_of_layer(self.test_dict, self.test_layer)
        self.cem.add_layer(self.test_layer)
        self.assertDictContainsSubset({self.test_layer: self.test_dict}, self.cem.layer_values_map)

        self.test_dict['RGBa(0, 20, 255, 255)'] = ('Invalid', 47,11)
        self.assertNotEqual(self.cem.layer_values_map[self.test_layer], self.test_dict)

    def test_color_value_triple_can_be_added_to_layer_in_cem(self):
        self.cem.set_color_map_of_layer(self.test_dict, self.test_layer)
        color_value_quadruple = ('RGBa(0, 20, 255, 255)', 'name', 47, 11)

        self.cem.add_color_value_quadruple_to_layer(color_value_quadruple, self.test_layer)
        self.test_dict[color_value_quadruple[0]] = color_value_quadruple[1:]
        self.assertDictContainsSubset({self.test_layer: self.test_dict}, self.cem.layer_values_map)

    def test_cem_writes_map_to_correct_path(self):
        path = sys.path[0]
        cem = ColorEntryManager()
        layer_name = 'my_test_layer'
        cem.add_layer(layer_name)
        cem.add_color_value_quadruple_to_layer(('Color', 'name', 0, 1), layer_name)
        out_path = os.path.join(path, layer_name + '.txt')
        cem.write_map_to_disk(layer_name, out_path)

        self.assertTrue(os.path.exists(out_path))
        try:
            os.remove(out_path)
        except IOError as Error:
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

        dict = {'RGBa(0, 0, 255, 255)': ('name0', 120, 11)}
        dict['RGBa(0, 0, 255, 255)'] = ('name1', 131,28)
        dict['RGBa(123, 21, 255, 255)'] = ('name2', 2,8)
        dict['RGBa(2, 33, 25, 2)'] = ('name3', 1,4)
        dict['RGBa(170, 12, 17, 36)'] = ('name4', 12,238)

        cem.set_color_map_of_layer(dict, layer_name)
        cem.write_map_to_disk(layer_name, out_path)
        self.assertTrue(os.path.exists(out_path))

        try:
            json_data = io.open(out_path)
            data = json.load(json_data)
            result_dict = {}

            for color, value_list in data.items():
                result_dict[color] = (value_list[0], value_list[1], value_list[2])

            self.assertDictContainsSubset(dict, result_dict)
            json_data.close()

        except IOError as Error:
            self.fail(Error)

        finally:
            try:
                os.remove(out_path)
            except IOError as Error:
                print(Error)

    def test_json_file_with_abbreviation_for_correctness(self):
        path = sys.path[0]
        cem = ColorEntryManager()
        layer_name = 'my_test_layer'
        abbreviation = '01TestLy'
        out_path = os.path.join(path, layer_name + '.txt')
        cem.add_layer(layer_name)

        dict = {'RGBa(0, 0, 255, 255)': ('name0', 120, 11)}
        dict['RGBa(0, 0, 255, 255)'] = ('name1', 131,28)
        dict['RGBa(123, 21, 255, 255)'] = ('name2', 2,8)
        dict['RGBa(2, 33, 25, 2)'] = ('name3', 1,4)
        dict['RGBa(170, 12, 17, 36)'] = ('name4', 12,238)

        cem.set_color_map_of_layer(dict, layer_name)
        cem.set_layer_abbreviation(layer_name, abbreviation)
        cem.write_map_to_disk(layer_name, out_path)
        self.assertTrue(os.path.exists(out_path))

        try:
            json_data = io.open(out_path)
            data = json.load(json_data)
            result_dict = {}
            for color, value_list in data['Legend'].items():
                result_dict[color] = (value_list[0], value_list[1], value_list[2])

            self.assertEqual(data['Abbreviation'], abbreviation)
            self.assertDictContainsSubset(dict, result_dict)
            json_data.close()

        except IOError as Error:
            self.fail(Error)

        finally:
            try:
                os.remove(out_path)
            except IOError as Error:
                print(Error)

    def test_cem_reads_file_from_disk_into_color_entry(self):
        path = sys.path[0]
        out_path = os.path.join(path, self.test_layer + '.txt')

        dict = {'RGBa(0, 0, 255, 255)': ('name1', 120, 11)}
        dict['RGBa(0, 0, 255, 255)'] = ('name1', 131,28)
        dict['RGBa(123, 21, 255, 255)'] = ('name1', 2,8)
        dict['RGBa(2, 33, 25, 2)'] = ('name1', 1,4)
        dict['RGBa(170, 12, 17, 36)'] = ('name1', 12,238)

        try:
            with io.open(out_path, 'w', encoding='utf-8') as json_outfile:
                json_string = json.dumps(dict, ensure_ascii=False)
                json_outfile.write(str(json_string))
        except (IOError, OSError) as Error:
            self.fail('Could not write test-data due to error: ' + Error)

        self.cem.read_color_map_from_disk(out_path)

        color_map = self.cem.layer_values_map[self.test_layer]
        self.assertDictEqual(dict, color_map, 'Error when reading a color-map from disk: \n\tReceived: {}\n\tExpected: {}'.format(color_map, dict))

    def test_cem_reads_file_and_abb_from_disk_into_color_entry(self):
        path = sys.path[0]
        out_path = os.path.join(path, self.test_layer + '.txt')
        abbreviation = '01TestLy'

        color_dict = {'RGBa(0, 0, 255, 255)': ('name1', 120, 11)}
        color_dict['RGBa(0, 0, 255, 255)'] = ('name1', 131,28)
        color_dict['RGBa(123, 21, 255, 255)'] = ('name1', 2,8)
        color_dict['RGBa(2, 33, 25, 2)'] = ('name1', 1,4)
        color_dict['RGBa(170, 12, 17, 36)'] = ('name1', 12,238)

        out_dict = {'Abbreviation': abbreviation, 'Legend': color_dict}
        try:
            with io.open(out_path, 'w', encoding='utf-8') as json_outfile:
                json_string = json.dumps(out_dict, ensure_ascii=False)
                json_outfile.write(str(json_string))
        except (IOError, OSError) as Error:
            self.fail('Could not write test-data due to error: ' + Error)

        self.cem.read_color_map_from_disk(out_path)

        color_map = self.cem.layer_values_map[self.test_layer]
        self.assertDictEqual(color_dict, color_map, 'Error when reading a color-map from disk: \n\tReceived: {}\n\tExpected: {}'.format(color_map, color_dict))
        self.assertEqual(self.cem.layer_abbreviation_map[self.test_layer], abbreviation)

    def test_dict_can_be_removed_from_layer_entry(self):
        self.cem.add_layer(self.test_layer)
        self.cem.set_color_map_of_layer(self.test_dict, self.test_layer)
        deleted_entry = 'RGBa(0, 0, 255, 255)'
        self.cem.remove_color_entry_from_layer(deleted_entry, self.test_layer)
        self.assertNotIn(deleted_entry, self.cem.layer_values_map[self.test_layer])
        self.assertIn('RGBa(0, 0, 220, 255)', self.cem.layer_values_map[self.test_layer])


class MunicipalInformationParserAndTreeTestCase(unittest.TestCase):

    def setUp(self):
        self.mip = MunicipalInformationParser()
        self.mit = MunicipalInformationTree()

    def test_municipal_json_file_can_be_found(self):
        self.assertTrue(os.path.exists(self.mip.municipal_json_file))

    def test_municipal_is_found_if_in_first_rows(self):
        json_content = {"NAME":"Flensburg, Stadt","POP_DENS":1575,"POSTCODE":24937,"GEO_L":9.43751,"GEO_W":54.78252,"AVG_YOC":1954}
        self.mip.parse_municipal(24937)
        self.assertDictContainsSubset(json_content, self.mip.municipal[0])

        json_content = {"NAME":"Lübeck, Hansestadt","POP_DENS":983,"POSTCODE":23539,"GEO_L":10.68393,"GEO_W":53.86627,"AVG_YOC":1944}
        self.mip.parse_municipal(23539)
        self.assertDictContainsSubset(json_content, self.mip.municipal[0])

    def test_municipal_is_found_if_in_row_10001(self):
        json_content = {"NAME":"Gunderath","POP_DENS":95,"POSTCODE":56767,"GEO_L":6.97902,"GEO_W":50.25468,"AVG_YOC":1964}
        self.mip.parse_municipal(56767)
        self.assertDictContainsSubset(json_content, self.mip.municipal[0])

    def test_keys_on_first_level(self):
        keys = self.mit.find_keys_on_level(0)
        self.assertNotEqual(keys, {})

    def test_keys_on_second_level(self):
        keys = self.mit.find_keys_on_level(1)
        self.assertNotEqual(keys, {})

    def test_data_tree_contains_first_row(self):
        self.mit.split_data_to_tree_model()
        tree = self.mit.tree
        self.assertNotEqual(tree, {})
        first_row = {"NAME":"Flensburg, Stadt","POP_DENS":1575,"POSTCODE":24937,"GEO_L":9.43751,"GEO_W":54.78252,"AVG_YOC":1954}
        self.assertDictContainsSubset(first_row, tree['2']['4']['937'][0])

    def test_data_tree_contains_last_row(self):
        self.mit.split_data_to_tree_model()
        tree = self.mit.tree
        self.assertNotEqual(tree, {})
        last_row = {"NAME":"Ponitz","POP_DENS":97,"POSTCODE":4639,"GEO_L":12.42338,"GEO_W":50.8562,"AVG_YOC":1912}
        self.assertDictContainsSubset(last_row, tree['4']['6']['39'][1])


if __name__ == '__main__':
    unittest.main()
