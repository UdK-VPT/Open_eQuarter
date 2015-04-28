import os

import config


class OpenEQuarterProject():

    def __init__(self, project_info_path='', progress_path='', conifg_path=''):

        self.project_info = ''
        if self.load_project_info(project_info_path):
            self.project_info = project_info_path

        self.progress = ''
        if self.load_progress(progress_path):
            self.progress = progress_path

        self.config = conifg_path
        if self.load_config(conifg_path):
            self.config = conifg_path

    def load_project_info(self, path_to_file):
        pass

    def load_progress(self, path_to_file):
        pass

    def load_config(self, path_to_file):
        pass