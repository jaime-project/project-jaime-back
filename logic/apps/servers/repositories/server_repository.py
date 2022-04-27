from typing import List

from logic.apps.servers.models.server_model import Server
from logic.libs.sqliteAlchemy import sqliteAlchemy

from .entities.server_entity import ServerEntity


def get_all() -> List[Server]:

    s = sqliteAlchemy.make_session()
    result = s.query(ServerEntity).all()
    s.close()

    return [r.to_model() for r in result]


def get(name: str) -> Server:

    s = sqliteAlchemy.make_session()
    result = s.query(ServerEntity).get({'name': name})
    s.close()

    return result.to_model()


def add(m: Server):

    s = sqliteAlchemy.make_session()

    e = ServerEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(name: str):

    s = sqliteAlchemy.make_session()

    e = s.query(ServerEntity).get({'name': name})
    s.delete(e)

    s.commit()
    s.flush()


def exist(name: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(ServerEntity).filter_by(name=name).count() == 0:
        result = False

    s.close()
    return result
