from typing import List

from sqlalchemy import or_

from logic.apps.libraries.entity import LibraryEntity
from logic.apps.libraries.model import Library
from logic.libs.sqliteAlchemy import sqliteAlchemy


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Library]:

    s = sqliteAlchemy.make_session()
    result = s.query(LibraryEntity)

    if filter:
        filter = f'%{filter}%'
        result = result.filter(or_(
            LibraryEntity.name.like(filter),
            LibraryEntity.description.like(filter),
            LibraryEntity.repo.like(filter),
            LibraryEntity.user.like(filter),
        ))

    if order:
        result = result.order_by(order)

    if page and size:
        result = result.limit(size).offset(size * (page-1))

    result = result.all()
    s.close()

    return [r.to_model() for r in result]


def get(name: str) -> Library:

    s = sqliteAlchemy.make_session()
    result = s.query(LibraryEntity).get({'name': name})
    s.close()

    return result.to_model()


def add(m: Library):

    s = sqliteAlchemy.make_session()

    e = LibraryEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(name: str):

    s = sqliteAlchemy.make_session()

    e = s.query(LibraryEntity).get({'name': name})
    s.delete(e)

    s.commit()
    s.flush()


def exist(name: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(LibraryEntity).filter_by(name=name).count() == 0:
        result = False

    s.close()
    return result
