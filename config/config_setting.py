import os
import sys

try:
    sys.path.append(os.environ['PROJECT_PATH'])
except:
    print('please add PROJECT_PATH to your environment')
    sys.exit(1)

import logging
import logging.config
import yaml
from datetime import datetime

class ConfigSetting:
    def __init__(self):
        pass

    def set_logger(self, name, log_dir):
        """
        set_logger: parser the yaml file.
        @params
        name: The project name of log.
        log_dir: The path of log storage.

        @returns
        logger: The logger setting variable.
        """
        log_dir = os.path.join(os.environ['PROJECT_PATH'], log_dir)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        config_filepath = os.path.join(
            os.environ['PROJECT_PATH'], 'config/yaml/logger_config.yml')
        if os.path.exists(config_filepath):
            with open(config_filepath, 'r') as f:
                now_time = datetime.strftime(
                    datetime.now(), '%Y%m%d')
                config = yaml.safe_load(f.read())
                config["handlers"]["file"]["filename"] = os.path.join(
                    log_dir, 'projectlog.log'+'.'+now_time)
            logging.config.dictConfig(config)
            logging.getLogger(name)

        else:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(module)s | %(funcName)s | %(levelname)s | %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S', stream=sys.stdout)

        return logging
    
    def yaml_parser(self, path=None):
        """
        yaml_parser: parser the yaml file.

        @returns
        data: yaml parameter(See the project_config.yml file.)
        """
        if path is None:
            path = os.path.join(os.path.realpath(
                os.environ['PROJECT_PATH']), 'config/yaml/project_config.yml')
        with open(path, 'r', encoding='utf-8') as stream:
            data = yaml.load(stream, Loader=yaml.Loader)
        return data
