from typing import List

from logic.apps.clusters.model import Cluster
from logic.libs.sqliteAlchemy import sqliteAlchemy

from .entity import ClusterEntity


def get_all() -> List[Cluster]:

    s = sqliteAlchemy.make_session()
    result = s.query(ClusterEntity).all()
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
