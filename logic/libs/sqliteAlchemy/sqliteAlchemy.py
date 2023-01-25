"""
SQLiteAlchemy
---------
1.0.0

Utiliza sqlAlchemy para establecer una uncia conexion con un sqlite local, es para uso simple sin tanta configuracion.
Requiere de la libreria de Reflection
"""
import time
from dataclasses import dataclass
from typing import Any

from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from logic.libs.logger import logger
from logic.libs.reflection import reflection
from logic.libs.sqliteAlchemy.src.sqlAlchemyMethods import create_engine

_ENGINE: Engine = None


@dataclass
class Config():
    """
    Objeto de configuracion
    """
    url: str = ''
    echo: bool = False
    entities_path: str = ''


def setup(conf: Config):
    """
    Configura la util, se debe usar antes de usar cualquier otro metodo
    """
    global _ENGINE
    _ENGINE = create_engine(conf.url, conf.echo)

    conected_db = False
    while not conected_db:
        try:
            make_session().execute('select 1')
            conected_db = True

        except Exception as _:
            logger.log.warn('DB conection error -> waiting to try again')
            time.sleep(3)

    for module_type in reflection.load_modules_by_regex_path(conf.entities_path):
        module_type.Entity.metadata.create_all(_ENGINE)


def make_session() -> Session:
    """
    Crea una nueva session para conectarse a la BD
    """
    return sessionmaker(_ENGINE)()


def get_entity_class() -> Any:
    """
    Crea la clase Entity del que deben heredar todos los entities
    """
    return declarative_base()
