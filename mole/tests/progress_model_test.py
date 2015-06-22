from PyQt4.QtGui import QApplication

import unittest
import sys
import shutil

from mole.model.progress_model import *


class ProgressItemsModel_test(unittest.TestCase):

    def setUp(self):
        self._sections = ['Project Basics', 'Source Definition', 'Analysis']
        self._steps0 = ['ol_plugin_installed', 'pst_plugin_installed', 'real_centroid_plugin_installed', 'project_created']
        self._steps1 = ['osm_layer_loaded', 'investigation_area_selected', 'housing_layer_loaded', 'building_coordinates_loaded', 'raster_loaded', 'legend_created']
        self._steps2 = ['information_sampled', 'building_calculations']

        self.app = QApplication(sys.argv)
        self.pim = ProgressItemsModel()

    def tearDown(self):
        if self.app is not None:
            del(self.app)

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
        prereq_of_first_section_item = self.pim.check_prerequisites_for(step_name)
        self.assertEqual(prereq_of_first_section_item.accessibleText(), step_name)

        step_name = self._steps0[-1]
        last_step_first_section_fails_due_to_first = self.pim.check_prerequisites_for(step_name)
        self.assertEqual(last_step_first_section_fails_due_to_first.accessibleText(), self._steps0[0])

        section_model = self.pim.section_views[0].model()
        end = len(self._steps0) - 1
        self.set_prerequisites(section_model, 0, end)
        last_step_first_section = self.pim.check_prerequisites_for(step_name)
        self.assertEqual(last_step_first_section.accessibleText(), step_name)

        step_name = self._steps1[0]
        self.set_prerequisites(section_model, 0, len(self._steps0))
        first_step_second_section = self.pim.check_prerequisites_for(step_name)
        self.assertEqual(first_step_second_section.accessibleText(), step_name)

        section_model = self.pim.section_views[1].model()
        self.set_prerequisites(section_model, 0, len(self._steps1))
        section_model = self.pim.section_views[2].model()
        self.set_prerequisites(section_model, 0, 1)

        step_name = self._steps2[1]
        second_step_third_section = self.pim.check_prerequisites_for(step_name)
        self.assertEqual(second_step_third_section.accessibleText(), step_name)

        self.set_prerequisites(section_model, 0, 1, 0)
        second_step_third_section_fails_due_to_first = self.pim.check_prerequisites_for(step_name)
        self.assertEqual(second_step_third_section_fails_due_to_first.accessibleText(), self._steps2[0])

    def test_if_progress_is_saved_correctly(self):
        section_model0 = self.pim.section_views[0].model()
        section_model1 = self.pim.section_views[1].model()
        section_model2 = self.pim.section_views[2].model()
        self.set_prerequisites(section_model0, 0, len(self._steps0))
        self.set_prerequisites(section_model1, 0, 1)
        self.set_prerequisites(section_model1, 1, 3, 1)

        path = os.path.join('.', 'oeq_progress.oeq')
        try:
            self.pim.save_section_models()

            self.set_prerequisites(section_model0, 0, len(self._steps0), 0)
            self.set_prerequisites(section_model1, 0, len(self._steps1), 0)
            self.set_prerequisites(section_model2, 0, len(self._steps2), 0)

            self.pim.load_section_models(path)
        except OSError, FileError:
            print(self.__module__, FileError)
        finally:
            try:
                os.remove(path)
            except OSError, FileError:
                print(self.__module__, FileError)

        last_step_first_section = self._steps0[-1]
        self.assertEqual(self.pim.check_prerequisites_for(last_step_first_section).accessibleText(), last_step_first_section)

        last_step = self._steps2[-1]
        last_completed = self._steps1[1]
        self.assertEqual(self.pim.check_prerequisites_for(last_step).accessibleText(), last_completed)


if __name__ == '__main__':
    unittest.main()