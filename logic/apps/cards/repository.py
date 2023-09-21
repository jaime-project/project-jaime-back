from typing import List

from sqlalchemy import or_

from logic.apps.cards.entity import CardEntity
from logic.apps.cards.model import Card
from logic.libs.sqliteAlchemy import sqliteAlchemy


def get_all(filter: str = None) -> List[Card]:

    s = sqliteAlchemy.make_session()
    result = s.query(CardEntity)

    if filter:
        filter = f'%{filter}%'
        result = result.filter(or_(
            CardEntity.name.like(filter),
            CardEntity.description.like(filter),
            CardEntity.creation_date.like(filter),
            CardEntity.job_module_repo.like(filter),
            CardEntity.job_module_name.like(filter),
            CardEntity.job_agent_type.like(filter),
        ))

    result = result.all()
    s.close()

    return [r.to_model() for r in result]


def get(id: str) -> Card:

    s = sqliteAlchemy.make_session()
    result = s.query(CardEntity).get({'id': id})
    s.close()

    if result:
        return result.to_model()

    return None


def add(m: Card):

    s = sqliteAlchemy.make_session()

    e = CardEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()
    s.close()


def delete(id: str):

    s = sqliteAlchemy.make_session()
    e = s.query(CardEntity).get({'id': id})
    s.delete(e)

    s.commit()
    s.flush()
    s.close()


def exist(id: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(CardEntity).filter_by(id=id).count() == 0:
        result = False

    s.close()
    return result
