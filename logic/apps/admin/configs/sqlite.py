from pathlib import Path

from logic.libs.sqliteAlchemy.sqliteAlchemy import Config, setup
from logic.apps.admin.configs.variables import Vars, get_var


def setup_sqlite():

    url = f'sqlite:///{get_var(Vars.JAIME_HOME_PATH)}/db/sqlite.db?check_same_thread=False'

    if (get_var(Vars.DB_URL)):
        url = get_var(Vars.DB_URL)

    setup(
        Config(
            url=url,
            echo=False,
            entities_path='logic/apps/*/entity.*'
        )
    )
