import multiprocessing

from flask.app import Flask
from gunicorn.app.base import BaseApplication

from logic.apps.admin.configs.app import (setup_directories, setup_repos,
                                          start_threads)
from logic.apps.admin.configs.db import setup_db
from logic.apps.admin.configs.logger import setup_loggers
from logic.apps.admin.configs.pyinstaller import setup_pyinstaller_binary
from logic.apps.admin.configs.rest import setup_rest, setup_token
from logic.apps.admin.configs.variables import Vars, get_var, setup_vars
from logic.libs.logger import logger
from logic.libs.variables.variables import get_var

# setup_pyinstaller_binary()

app = Flask(__name__)

setup_vars()
setup_loggers()
setup_rest(app)
setup_token(app)

setup_directories()
setup_db()
setup_repos()
start_threads()

with open('logic/resources/banner.txt', 'r') as f:
    logger.log.info(f.read())

logger.log.info("> Jaimeeehhhh...!!!")
logger.log.info("> ¿Si, señora?")

# if __name__ == "__main__":

#     class AppGunicorn(BaseApplication):

#         def load_config(self):
#             s = self.cfg.set
#             s('bind', f"{get_var(Vars.PYTHON_HOST)}:{get_var(Vars.PYTHON_PORT)}")
#             s('workers', multiprocessing.cpu_count() * 2 + 1)
#             s('threads', get_var(Vars.GUNICORN_THREADS))
#             s('timeout', get_var(Vars.GUNICORN_TIMEOUT))

#         def load(self):
#             return app

#     AppGunicorn().run()

if __name__ == "__main__":
    app.run(
        host=get_var(Vars.PYTHON_HOST),
        port=get_var(Vars.PYTHON_PORT),
    )
