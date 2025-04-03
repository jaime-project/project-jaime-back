import os
import sys

import pg8000
import pymssql
import pymysql
from gunicorn import glogging
from gunicorn.workers import gthread


def setup_pyinstaller_binary():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
