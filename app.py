#!env/bin/python
import os
import sys

from flask.app import Flask

from logic.apps.admin.configs.app import setup_repos, start_threads
from logic.apps.admin.configs.logger import setup_loggers
from logic.apps.admin.configs.rest import setup_rest, setup_token
from logic.apps.admin.configs.sqlite import setup_sqlite
from logic.apps.admin.configs.variables import Vars, get_var, setup_vars
from logic.libs.logger import logger
from logic.libs.variables.variables import get_var

# pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

app = Flask(__name__)

setup_vars()
setup_loggers()
setup_rest(app)
setup_token(app)

setup_sqlite()
setup_repos()
start_threads()

with open('logic/resources/banner.txt', 'r') as f:
    logger.log.info(f.read())

logger.log.info("> Jaimeeehhhh...!!!")
logger.log.info("> ¿Si, señora?")

if __name__ == "__main__":
    flask_host = get_var(Vars.PYTHON_HOST)
    flask_port = int(get_var(Vars.PYTHON_PORT))

    app.run(host=flask_host, port=flask_port, debug=False)
