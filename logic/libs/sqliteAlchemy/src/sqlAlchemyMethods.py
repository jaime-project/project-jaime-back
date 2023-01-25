import os
from pathlib import Path

import sqlalchemy


def create_engine(url: str, echo: bool = False) -> sqlalchemy.engine.Engine:
    """
    Crea un engine usando el metodo create_engine() de sqlAlchemy y las configuraciones cargadas en el setup()
    """
    if 'sqlite' in url:
        _create_subdirectories(url)

    return sqlalchemy.create_engine(url, echo=echo)


def _create_subdirectories(url: str):
    """
    Crea los subdirectorios en caso de que no existan
    """
    path_file = url.replace('sqlite:///', '')

    if not os.path.exists(path_file):
        Path(os.path.dirname(path_file)).mkdir(parents=True, exist_ok=True)
