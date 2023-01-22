from typing import List

from logic.apps.clusters.entity import ClusterEntity
from logic.apps.clusters.model import Cluster
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import or_


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Cluster]:

    s = sqliteAlchemy.make_session()
    result = s.query(ClusterEntity)

    if filter:
        filter = f'%{filter}%'
        result = result.filter(or_(
            ClusterEntity.name.like(filter),
            ClusterEntity.url.like(filter),
            ClusterEntity.token.like(filter),
            ClusterEntity.type.like(filter),
            ClusterEntity.version.like(filter),
        ))

    if order:
        result = result.order_by(order)

    if page and size:
        result = result.limit(size).offset(size * (page-1))

    result = result.all()
    s.close()

    return [r.to_model() for r in result]


def get(name: str) -> Cluster:

    s = sqliteAlchemy.make_session()
    result = s.query(ClusterEntity).get({'name': name})
    s.close()

    return result.to_model()


def add(m: Cluster):

    s = sqliteAlchemy.make_session()

    e = ClusterEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(name: str):

    s = sqliteAlchemy.make_session()

    e = s.query(ClusterEntity).get({'name': name})
    s.delete(e)

    s.commit()
    s.flush()


def exist(name: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(ClusterEntity).filter_by(name=name).count() == 0:
        result = False

    s.close()
    return result
