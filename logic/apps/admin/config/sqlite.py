from pathlib import Path

from logic.libs.sqliteAlchemy.sqliteAlchemy import Config, setup


def setup_sqlite():

    setup(
        Config(
            url=f'{Path.home()}/.jaime/db/sqlite.db',
            echo=True,
            path='logic/apps/*/repositories/entities'
        )
    )
