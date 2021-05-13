from yaml.error import YAMLError
from schuaro.error import *

import yaml

def read_local_configuration(conf_file: str = "config/config.yml"):
    """
        Loads the local configuration file.
    """

    try:
        with open(conf_file) as f:
            try:
                return yaml.load(f, Loader=yaml.FullLoader)
            except YAMLError:
                raise ConfigurationInvalidError(f"Configuration file '{conf_file}' is invalidly formatted")
    except IOError:
        raise ConfigurationInvalidError(f"Unable to find or read from configuration file '{conf_file}'")