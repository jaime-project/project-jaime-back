from typing import List

from sqlalchemy import or_

from logic.apps.messages.entity import MessageEntity
from logic.apps.messages.model import Message, Status
from logic.libs.sqliteAlchemy import sqliteAlchemy


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Message]:

    s = sqliteAlchemy.make_session()
    result = s.query(MessageEntity)

    if filter:
        filter = f'%{filter}%'
        result = result.filter(or_(
            MessageEntity.id.like(filter),
            MessageEntity.title.like(filter),
            MessageEntity.subject.like(filter),
            MessageEntity.body.like(filter),
            MessageEntity.files.like(filter),
            MessageEntity.status.like(filter),
        ))

    if order:
        result = result.order_by(order)

    if page and size:
        result = result.limit(size).offset(size * (page-1))

    result = result.all()
    s.close()

    return [r.to_model() for r in result]


def get(id: str) -> Message:

    s = sqliteAlchemy.make_session()
    result = s.query(MessageEntity).get({'id': id})
    s.close()

    return result.to_model()


def add(m: Message):

    s = sqliteAlchemy.make_session()

    e = MessageEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(id: str):

    s = sqliteAlchemy.make_session()

    e = s.query(MessageEntity).get({'id': id})
    s.delete(e)

    s.commit()
    s.flush()


def exist(id: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(MessageEntity).filter_by(id=id).count() == 0:
        result = False

    s.close()
    return result


def get_all_by_status(status: Status) -> List[Message]:

    s = sqliteAlchemy.make_session()
    result = s.query(MessageEntity).filter_by(status=status.value).all()
    s.close()

    return [r.to_model() for r in result]
