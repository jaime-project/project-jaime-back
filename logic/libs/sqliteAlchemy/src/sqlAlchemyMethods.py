import os
from pathlib import Path

import sqlalchemy
from logic.libs.sqliteAlchemy.src import config


def create_engine(url: str) -> sqlalchemy.engine.Engine:
    """
    Crea un engine usando el metodo create_engine() de sqlAlchemy y las configuraciones cargadas en el setup()
    """

    if 'sqlite' in url:
        _create_subdirectories(url)

    return sqlalchemy.create_engine(url, echo=config.ECHO)


def _create_subdirectories(path_file: str):
    """
    Crea los subdirectorios en caso de que no existan
    """
    path_file = path_file.replace('sqlite:///', '')
    if not os.path.exists(path_file):
        Path(os.path.dirname(path_file)).mkdir(parents=True, exist_ok=True)
