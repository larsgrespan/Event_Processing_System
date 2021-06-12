"""
@author: Adrian Haaga
"""

import yaml


class YamlHandler:
    """
    A class used to handle YAML-file input.
    """

    def __init__(self, path):
        """
        Constructor for class YamlHandler.

        Parameters
        ----------
        path : str
            Path to the YAML-file
        """
        self.file = self.readYaml(path)
        self.overlap = False
        self.validateInputYaml(self.file)
        self.dataConfig = self.file.get('data')
        self.relationsConfig = self.file.get('relations')

    def readYaml(self, path):
        """
        Reads in a YAML-file and returns a config dict for the data generator.

        Parameters
        ----------
        path : str
            Path to the YAML-file

        Returns
        ------
        dict
            Returns a dict with config for the data generator
        """
        with open(path) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def validateInputYaml(self, yamlFile):
        """
        Validates the given YAML-file.

        Parameters
        ----------
        yamlFile : dict
            Config dict from YAML-file
        """
        # TODO
        if 'data' in yamlFile:
            True

        if 'params' in yamlFile:
            params = yamlFile['params']
            for key, value in params.items():
                if key == 'overlap':
                    if isinstance(value, bool):
                        self.overlap = value
                    else:
                        raise Exception('overlap has to be a boolean value')

        if 'relations' in yamlFile:
            relations = yamlFile['relations']
            for key, value in relations.items():
                try:
                    value['target']
                except:
                    print('No target-key found in ', key)
                try:
                    value['if']
                except:
                    print('No if-key found in ', key)
                try:
                    value['then']
                except:
                    print('No then-key found in ', key)
                try:
                    value['proportion']
                except:
                    print('No proportion-key found in ', key)

    def getDataConfig(self):
        return self.dataConfig

    def getRelationsConfig(self):
        return self.relationsConfig
