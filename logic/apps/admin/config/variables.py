from enum import Enum

from logic.libs.variables.variables import Config, setup


class Vars(Enum):
    VERSION = 'VERSION'
    PYTHON_HOST = 'PYTHON_HOST'
    PYTHON_PORT = 'PYTHON_PORT'
    LOGS_LEVEL = 'LOGS_LEVEL'
    LOGS_BACKUPS = 'LOGS_BACKUPS'


def setup_vars():
    setup([
        Config(
            file_path='variables.env',
            hiden_vars=[],
            enum_vars=Vars)
    ])
