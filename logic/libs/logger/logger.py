"""
Logger
-------
2.0.0

Crea logs de la aplicacion
"""
import logging
from dataclasses import dataclass

from logic.libs.logger.src.file import make_logger


@dataclass
class Config():
    """
    Objeto de configuracion
    """
    path: str = '/tmp/logs/app.log'
    level: str = 'INFO'
    file_backup_count: int = 3


log: logging.Logger = None


def setup(con: Config):
    """
    Configura las opciones PREDEFINIDAS del logger para el proyecto, en caso del handler, 
    el que viene rota los logs con un archivo por dia hasta hasta un maximo de 7 archivos.
    """
    global log
    log = make_logger(con)
