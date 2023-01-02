from enum import Enum

from logic.libs.variables.variables import Config, get_var, setup


class Vars(Enum):
    VERSION = 'VERSION'
    PYTHON_HOST = 'PYTHON_HOST'
    PYTHON_PORT = 'PYTHON_PORT'
    LOGS_LEVEL = 'LOGS_LEVEL'
    LOGS_BACKUPS = 'LOGS_BACKUPS'
    WORKINGDIR_PATH = 'WORKINGDIR_PATH'
    AGENTS_HTTPS = 'AGENTS_HTTPS'


def setup_vars():
    setup(Config(
        file_path='logic/resources/variables.yaml',
        hiden_vars=[],
        enum_vars=Vars)
    )
