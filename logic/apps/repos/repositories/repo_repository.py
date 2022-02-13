from typing import List

from logic.apps.clusters.models.cluster_model import Cluster
from logic.libs.sqliteAlchemy import sqliteAlchemy

from logic.apps.repos.repositories.entities.repo_entity import RepoGitEntity


def get_all() -> List[Cluster]:

    s = sqliteAlchemy.make_session()
    result = s.query(RepoGitEntity).all()
    s.close()

    return [r.to_model() for r in result]


def get(name: str) -> Cluster:

    s = sqliteAlchemy.make_session()
    result = s.query(RepoGitEntity).get({'name': name})
    s.close()

    return result.to_model()


def add(m: Cluster):

    s = sqliteAlchemy.make_session()

    e = RepoGitEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(name: str):

    s = sqliteAlchemy.make_session()

    e = s.query(RepoGitEntity).get({'name': name})
    s.delete(e)

    s.commit()
    s.flush()


def exist(name: str) -> bool:

    s = sqliteAlchemy.make_session()
    if s.query(RepoGitEntity).filter_by(name=name).count() == 0:
        return False

    return True
