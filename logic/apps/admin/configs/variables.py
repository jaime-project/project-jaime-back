from enum import Enum

from logic.libs.variables.variables import Config, get_var, setup


class Vars(Enum):
    VERSION = 'VERSION'
    PYTHON_HOST = 'PYTHON_HOST'
    PYTHON_PORT = 'PYTHON_PORT'
    LOGS_LEVEL = 'LOGS_LEVEL'
    LOGS_BACKUPS = 'LOGS_BACKUPS'
    WORKINGDIR_PATH = 'WORKINGDIR_PATH'
    JAIME_HOME_PATH = 'JAIME_HOME_PATH'
    STORAGE_PATH = 'STORAGE_PATH'
    AGENTS_HTTPS = 'AGENTS_HTTPS'
    DB_URL = 'DB_URL'
    JAIME_USER = 'JAIME_USER'
    JAIME_PASS = 'JAIME_PASS'
    DELETE_OLD_JOBS_MINUTES = 'DELETE_OLD_JOBS_MINUTES'
    GUNICORN_WORKERS = 'GUNICORN_WORKERS'
    GUNICORN_THREADS = 'GUNICORN_THREADS'
    GUNICORN_TIMEOUT = 'GUNICORN_TIMEOUT'


def setup_vars():
    setup(Config(
        file_path='logic/resources/variables.yaml',
        hiden_vars=['JAIME_PASS']
    ))
