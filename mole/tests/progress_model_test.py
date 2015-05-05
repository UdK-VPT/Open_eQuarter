from PyQt4.QtGui import QApplication

import unittest
import sys

from mole.model.progress_model import *


class ProgressModel_test(unittest.TestCase):

    def setUp(self):
        self._pages = ['project_basics', 'investigation_area', 'building_shapes', 'real_estate_cadaster', 'sampling_points']
        self._steps0 = ['ol_plugin_installed', 'pst_plugin_installed', 'project_created', 'osm_layer_loaded']
        self._steps1 = ['temp_shapefile_created', 'editing_temp_shapefile_started', 'investigation_area_selected', 'editing_temp_shapefile_stopped']
        self._steps2 = ['housing_layer_loaded', 'building_coordinates_loaded']
        self._steps3 = ['raster_loaded', 'extent_clipped', 'legend_created']
        self._steps4 = ['temp_pointlayer_created', 'editing_temp_pointlayer_started', 'points_of_interest_defined', 'editing_temp_pointlayer_stopped', 'information_sampled']
        self._prog_model = ProgressModel()

    def test_if_the_whole_progress_can_be_updated(self):

        for step in self._steps0:
            self._prog_model.update_progress(self._pages[0], step, True)

        last_step = len(self._steps0) - 1
        self.assertEqual(self._prog_model.last_step_executed, last_step)

        for step in self._steps1:
            self._prog_model.update_progress(self._pages[1], step, True)

        last_step += len(self._steps1)
        self.assertEqual(self._prog_model.last_step_executed, last_step)

        for step in self._steps2:
            self._prog_model.update_progress(self._pages[2], step, True)

        last_step += len(self._steps2)
        self.assertEqual(self._prog_model.last_step_executed, last_step)

        for step in self._steps3:
            self._prog_model.update_progress(self._pages[3], step, True)

        last_step += len(self._steps3)
        self.assertEqual(self._prog_model.last_step_executed, last_step)
        self.assertRaises(KeyError, self._prog_model.update_progress(self._steps0[1], self._pages[1], False))
        self.assertEqual(self._prog_model.last_step_executed, last_step)

    def test_prerequisites_when_nothing_is_true(self):
        self.assertFalse(self._prog_model.prerequisites_are_given('information_sampled'))

    def test_if_prerequisites_of_first_step_are_true(self):
        self.assertTrue(self._prog_model.prerequisites_are_given(self._steps0[0]))

    def test_if_prerequisites_of_second_step_are_false(self):
        self.assertFalse(self._prog_model.prerequisites_are_given(self._steps0[1]))

    def test_prerequisites_when_each_predecessor_is_true(self):
        self._prog_model.update_progress(self._pages[0], self._steps0[0], True)
        self._prog_model.update_progress(self._pages[0], self._steps0[1], True)
        self._prog_model.update_progress(self._pages[0], self._steps0[2], True)

        self.assertTrue(self._prog_model.prerequisites_are_given(self._steps0[3]))
    #
    # def test_prerequsites_when_only_some_predecessors_are_true(self):
    #     self._prog_model.update_progress(self._pages[0], self._steps0[1], True)
    #     self.assertFalse(self._prog_model.prerequisites_are_given(self._steps0[3]))

    def test_position_of_first_element(self):
        index = 0
        position = self._prog_model.get_position_of_step(self._steps0[index])
        self.assertEqual(position, index, 'Expected position of "{}" is {}, received: {}.'.format(self._steps0[index],index, position))

    def test_position_in_first_section(self):
        index = 2
        position = self._prog_model.get_position_of_step(self._steps0[index])
        self.assertEqual(position, index, 'Expected position of "{}" is {}, received: {}.'.format(self._steps0[index], index, position))

    def test_position_of_last_element(self):
        index = len(self._steps3)-1
        position = self._prog_model.get_position_of_step(self._steps3[index])
        # sum the number of steps and subtract one, since the enumeration starts with 0
        expected = len(self._steps0) + len(self._steps1) + len(self._steps2) + len(self._steps3) - 1
        self.assertEqual(position, expected, 'Expected position of "{}" is {}, received: {}.'.format(self._steps3[index], expected, position))

    def test_position_of_invalid_element(self):
        position = self._prog_model.get_position_of_step('this string will not be found')
        self.assertIsNone(position)

        position = self._prog_model.get_position_of_step('')
        self.assertIsNone(position)

        position = self._prog_model.get_position_of_step(None)
        self.assertIsNone(position)

    def test_if_open_section_is_marked_as_open(self):
        section = self._pages[0]
        self.assertFalse(self._prog_model.is_section_done(section))

        section = self._pages[1]
        self.assertFalse(self._prog_model.is_section_done(section))

        section = self._pages[2]
        self.assertFalse(self._prog_model.is_section_done(section))

    def test_if_first_section_is_marked_as_done(self):
        section = self._pages[0]

        for step in self._steps0:
            self._prog_model.update_progress(section, step, True)

        self.assertTrue(self._prog_model.is_section_done(section))

    def test_open_section_if_previous_section_is_done(self):
        prev_section = self._pages[0]
        section = self._pages[1]

        for step in self._steps0:
            self._prog_model.update_progress(prev_section, step, True)

        self.assertFalse(self._prog_model.is_section_done(section))

    def test_if_section_is_marked_as_done_if_previous_section_is_open(self):
        prev_section = self._pages[0]
        section = self._pages[1]

        for step in self._steps1:
            self._prog_model.update_progress(section, step, True)

        self.assertTrue(self._prog_model.is_section_done(section))

    def test_if_section_is_done_if_three_of_four_steps_are_completed(self):
        section = self._pages[0]
        for step in self._steps0[:-1]:
            self._prog_model.update_progress(section, step, True)

        self.assertFalse(self._prog_model.is_section_done(section))

    def test_if_first_step_is_done(self):
        section = self._pages[0]
        step = self._steps0[0]
        self._prog_model.update_progress(section, step, True)
        self.assertTrue(self._prog_model.is_step_done(step))

    def test_if_step_is_done(self):
        section = self._pages[1]
        step = self._steps1[2]
        self._prog_model.update_progress(section, step, True)
        self.assertTrue(self._prog_model.is_step_done(step))

    def test_if_step_is_not_done(self):
        step = self._steps1[2]
        self.assertFalse(self._prog_model.is_step_done(step))

    def test_if_step_list_contains_every_step(self):
        step_list = set(self._prog_model.get_step_list())

        self.assertEqual(step_list.intersection(set(self._steps0)), set(self._steps0))
        self.assertEqual(step_list.intersection(set(self._steps1)), set(self._steps1))
        self.assertEqual(step_list.intersection(set(self._steps2)), set(self._steps2))
        self.assertEqual(step_list.intersection(set(self._steps3)), set(self._steps3))


class ProgressItemsModel_test(unittest.TestCase):

    def setUp(self):
        self._sections = ['Project Basics', 'Investigation Area', 'Building Shapes', 'Real Estate Cadaster', 'Sampling Points']
        self._steps0 = ['ol_plugin_installed', 'pst_plugin_installed', 'project_created', 'osm_layer_loaded']
        self._steps1 = ['temp_shapefile_created', 'editing_temp_shapefile_started', 'investigation_area_selected', 'editing_temp_shapefile_stopped']
        self._steps2 = ['housing_layer_loaded', 'building_coordinates_loaded']
        self._steps3 = ['raster_loaded', 'extent_clipped', 'legend_created']
        self._steps4 = ['temp_pointlayer_created', 'editing_temp_pointlayer_started', 'points_of_interest_defined', 'editing_temp_pointlayer_stopped', 'information_sampled']

        self.app = QApplication(sys.argv)
        self.pim = ProgressItemsModel()

    def set_prerequisites(self, section, start, end, value=2):
        i = start
        while section.item(i) and i < end:
            section.item(i).setCheckState(value)
            i += 1


    def test_if_pim_was_initialised_according_json_file(self):
            self.assertEqual(len(self.pim.section_views), len(self._sections))

            for index, section in enumerate(self.pim.section_views):
                self.assertEqual(section.accessibleName(), self._sections[index])

                handle = '_steps{}'.format(index)
                steps = getattr(self, handle)
                self.assertEqual(section.model().rowCount(), len(steps))

    def test_if_prerequisites_are_checked_correctly(self):
        step_name = self._steps0[0]
        prereq_of_first_section = self.pim.check_prerequisites_of(step_name)
        self.assertEqual(prereq_of_first_section, step_name)

        step_name = self._steps0[-1]
        last_step_first_section_fails_due_to_first = self.pim.check_prerequisites_of(step_name)
        self.assertEqual(last_step_first_section_fails_due_to_first, self._steps0[0])

        section_model = self.pim.section_views[0].model()
        end = len(self._steps0) - 1
        self.set_prerequisites(section_model, 0, end)
        last_step_first_section = self.pim.check_prerequisites_of(step_name)
        self.assertEqual(last_step_first_section, step_name)

        step_name = self._steps1[0]
        self.set_prerequisites(section_model, 0, len(self._steps0))
        first_step_second_section = self.pim.check_prerequisites_of(step_name)
        self.assertEqual(first_step_second_section, step_name)

        section_model = self.pim.section_views[1].model()
        self.set_prerequisites(section_model, 0, len(self._steps1))
        section_model = self.pim.section_views[2].model()
        self.set_prerequisites(section_model, 0, 1)

        step_name = self._steps2[1]
        second_step_third_section = self.pim.check_prerequisites_of(step_name)
        self.assertEqual(second_step_third_section, step_name)

        self.set_prerequisites(section_model, 0, 1, 0)
        second_step_third_section_fails_due_to_first = self.pim.check_prerequisites_of(step_name)
        self.assertEqual(second_step_third_section_fails_due_to_first, self._steps2[0])


if __name__ == '__main__':
    unittest.main()