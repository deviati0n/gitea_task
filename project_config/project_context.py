from os import path

import yaml

import project_config.data_classes as dc


class ProjectContext:

    def __init__(self):
        self.project_path = path.dirname(path.realpath(__file__))
        config_path = path.join(self.project_path, '../project_config/config.yaml')

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        gitea = self.config['gitea_options']
        self.gitea_config = dc.GiteaOptions(**gitea)

        test = self.config['test_options']
        self.test_config = dc.TestOptions(**test)
