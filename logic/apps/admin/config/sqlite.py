from pathlib import Path

from logic.libs.sqliteAlchemy.sqliteAlchemy import Config, setup


def setup_sqlite():

    setup(
        Config(
            url=f'sqlite:///{Path.home()}/.jaime/db/sqlite.db?check_same_thread=False',
            echo=False,
            path='logic/apps/*/repositories/entities'
        )
    )
