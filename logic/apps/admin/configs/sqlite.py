from pathlib import Path

from logic.libs.sqliteAlchemy.sqliteAlchemy import Config, setup
from logic.apps.admin.configs.variables import Vars, get_var


URL_SQLITE = f'sqlite:///{Path.home()}/.jaime/db/sqlite.db?check_same_thread=False'


def setup_sqlite():

    url = URL_SQLITE

    if (get_var(Vars.DB_URL)):
        url = get_var(Vars.DB_URL)

    setup(
        Config(
            url=url,
            echo=False,
            entities_path='logic/apps/*/entity.*'
        )
    )
