from typing import List

from sqlalchemy import or_

from logic.apps.servers.entity import ServerEntity
from logic.apps.servers.model import Server
from logic.libs.sqliteAlchemy import sqliteAlchemy


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Server]:

    s = sqliteAlchemy.make_session()
    result = s.query(ServerEntity)

    if filter:
        filter = f'%{filter}%'
        result = result.filter(or_(
            ServerEntity.name.like(filter),
            ServerEntity.host.like(filter),
            ServerEntity.port.like(filter),
            ServerEntity.user.like(filter),
            ServerEntity.password.like(filter),
        ))

    if order:
        result = result.order_by(order)

    if page and size:
        result = result.limit(size).offset(size * (page-1))

    result = result.all()
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
