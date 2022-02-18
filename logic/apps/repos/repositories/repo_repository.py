from typing import List

from logic.apps.repos.errors.repo_error import RepoError
from logic.apps.repos.models.repo_model import Repo, RepoType
from logic.apps.repos.repositories.entities.repo_entity import (
    Entity, RepoGitEntity, RepoLocalEntity)
from logic.libs.exception.exception import AppException
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import null


def get_all() -> List[Repo]:

    s = sqliteAlchemy.make_session()

    result = []
    result += s.query(RepoGitEntity).all()
    result += s.query(RepoLocalEntity).all()

    s.close()

    return [r.to_model() for r in result]


def get(name: str) -> Repo:

    s = sqliteAlchemy.make_session()

    result = None

    if result == None:
        result = s.query(RepoLocalEntity).get({'name': name})

    if result == None:
        result = s.query(RepoGitEntity).get({'name': name})

    s.close()

    if result != None:
        return result.to_model()

    return None


def add(m: Repo):

    s = sqliteAlchemy.make_session()

    repo_class = _get_entity_class_by_type(m.type)
    e = repo_class.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(name: str):

    s = sqliteAlchemy.make_session()

    e = get(name)
    if e == None:
        msj = f'El repo con nombre {name} no existe'
        raise AppException(RepoError.REPO_NOT_EXISTS_ERROR, msj)

    entity_class = _get_entity_class_by_type(e.type)
    e = s.query(entity_class).get({'name': name})
    s.delete(e)

    s.commit()
    s.flush()


def exist(name: str) -> bool:

    if get(name) == None:
        return False

    return True


def _get_entity_class_by_type(type: RepoType) -> Entity:

    if type == type.GIT:
        return RepoGitEntity

    if type == type.LOCAL:
        return RepoLocalEntity
